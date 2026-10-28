#!/usr/bin/env python3
"""Verify catalog paths, generation records, and checksums using the standard library."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    result = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            result.update(chunk)
    return result.hexdigest()


def asset_path(relative):
    path = (ROOT / relative).resolve()
    if not path.is_relative_to(ROOT / 'assets'):
        raise ValueError(f'Asset path escapes assets directory: {relative}')
    if not path.is_file() or not path.stat().st_size:
        raise ValueError(f'Missing or empty asset: {relative}')
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write-checksums', action='store_true', help='Refresh checksums after intentional asset changes')
    args = parser.parse_args()
    catalog = json.loads((ROOT / 'catalog.json').read_text())
    manifest = json.loads((ROOT / 'generation-manifest.json').read_text())
    required = {'source_image', 'image', 'portrait', 'video', 'source_video', 'image_prompt', 'motion_prompt'}
    referenced = set()
    profiles = {}
    for commander in catalog['commanders']:
        identifier = commander['id']
        if identifier in profiles:
            raise ValueError(f'Duplicate commander: {identifier}')
        profiles[identifier] = commander
        if set(commander['assets']) != required:
            raise ValueError(f'Incomplete asset roles for {identifier}')
        for relative in commander['assets'].values():
            asset_path(relative)
            referenced.add(relative)
    if set(profiles) != {video['id'] for video in manifest['videos']}:
        raise ValueError('Catalog and generation manifest commander IDs differ')
    for video in manifest['videos']:
        assets = profiles[video['id']]['assets']
        for key, role in {'source_image': 'source_image', 'prompt': 'motion_prompt', 'website_video': 'video', 'native_source_local': 'source_video'}.items():
            if video[key] != assets[role]:
                raise ValueError(f'Manifest/catalog path mismatch: {video["id"]}/{key}')
            asset_path(video[key])
        for key, hash_key in [('source_image', 'source_image_sha256'), ('website_video', 'website_sha256')]:
            if digest(asset_path(video[key])) != video[hash_key]:
                raise ValueError(f'Generation hash mismatch: {video[key]}')
        for key, size_key in [('website_video', 'website_bytes'), ('native_source_local', 'native_source_bytes')]:
            if asset_path(video[key]).stat().st_size != video[size_key]:
                raise ValueError(f'Generation size mismatch: {video[key]}')
    actual = {path.relative_to(ROOT).as_posix() for path in (ROOT / 'assets').rglob('*') if path.is_file()}
    if actual != referenced:
        raise ValueError(f'Uncatalogued or missing assets: {sorted(actual ^ referenced)}')
    hashes = {relative: digest(asset_path(relative)) for relative in sorted(actual)}
    checksum_file = ROOT / 'checksums.sha256'
    if args.write_checksums:
        checksum_file.write_text(''.join(f'{value}  {relative}\n' for relative, value in hashes.items()))
    expected = {}
    for line in checksum_file.read_text().splitlines():
        value, relative = line.split('  ', 1)
        if relative in expected:
            raise ValueError(f'Duplicate checksum path: {relative}')
        expected[relative] = value
    if expected != hashes:
        raise ValueError('checksums.sha256 differs from current assets')
    total = sum(asset_path(relative).stat().st_size for relative in actual)
    print(f'OK: {len(profiles)} commanders, {len(actual)} assets/prompts, {total:,} bytes; paths, generation records and SHA-256 verified.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f'ERROR: {error}', file=sys.stderr)
        sys.exit(1)
