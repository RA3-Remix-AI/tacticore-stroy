# tacticore-stroy

弈核（Tacticore）的视频资源项目，集中保存指挥官人物原图、网页图片、动作视频、生成提示词与制作记录。首批收录铁锤、堡垒、幽灵三位指挥官，供视频制作、官网展示和后续视觉延展使用。

| 指挥官 | 风格 | 原图 | 动作成片 |
| --- | --- | --- | --- |
| 铁锤 / HAMMER | 主动施压、集中突破 | [source.png](assets/commanders/hammer/source.png) | [motion.mp4](assets/commanders/hammer/motion.mp4) |
| 堡垒 / BASTION | 稳健经营、纵深防线 | [source.png](assets/commanders/bastion/source.png) | [motion.mp4](assets/commanders/bastion/motion.mp4) |
| 幽灵 / GHOST | 侧翼侦察、机动协同 | [source.png](assets/commanders/ghost/source.png) | [motion.mp4](assets/commanders/ghost/motion.mp4) |

## 目录

```text
assets/commanders/{hammer,bastion,ghost}/
  source.png          原始人物概念图，1672 × 941
  image.webp          网页横图
  portrait.webp       人物头像，384 × 480
  motion.mp4          无音轨成片，2560 × 1440 / 24 fps / 约 6.583 秒
  motion-source.mp4   带生成音轨的原始视频下载
  image-prompt.txt    原始图片生成提示词
  motion-prompt.txt   原始视频生成提示词
catalog.json          人物文案与全部资源路径
generation-manifest.json  视频生成参数、任务记录、处理信息
checksums.sha256      assets 下全部文件的 SHA-256
scripts/verify_assets.py   资源路径与完整性检查
docs/production.md   制作说明
```

所有清单路径均相对于仓库根目录。消费方可以读取 [catalog.json](catalog.json) 按人物 ID 定位资产。网页展示优先使用 `image.webp`、`portrait.webp` 和无音轨 `motion.mp4`；剪辑需要原始音轨时使用 `motion-source.mp4`。

## 校验

仅需 Python 3，无需安装第三方依赖。在仓库根目录运行：

```sh
python3 scripts/verify_assets.py
```

主动新增或替换资产并核实来源后，更新校验清单：

```sh
python3 scripts/verify_assets.py --write-checksums
python3 scripts/verify_assets.py
```

当前资源体积较小，直接由 Git 管理，未配置 Git LFS。

## 来源

首批物料于 2026-10-28 从 `RA3-Remix/remix-website` 整理而来，保留原始文件字节和提示词。人物文案来自该项目的 `src/content/commanders.ts`，其性格方向依据弈核桌面项目 `Tacticore/desktop-ui/src/state/settings.ts` 中的 `defaultSettings.commanders`。

图片由 Codex 内置 ImageGen 生成，动作视频由 MiniMax-H3 生成。它们是人物概念视觉，不代表游戏实机、真实人物或已验收的作战效果；人格不绑定固定阵营。生成和导出细节见 [制作说明](docs/production.md)。
