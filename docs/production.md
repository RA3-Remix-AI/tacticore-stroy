# 指挥官物料制作记录

首批资产制作于 2026-10-28，整理自 `RA3-Remix/remix-website`。本资源工程按人物集中保存素材与提示词；整理过程未重新生成、缩放或转码媒体。

## 人物概念图

三张原图由 Codex 内置 ImageGen 分别生成，实际输出均为 **1672 × 941 PNG**，接近 16:9。提示词申请更高分辨率，实际输出未上采样。人物位于右中部，左侧预留标题区域，采用军事科幻写实概念美术。

| 人物 | 色彩与性格方向 | 图片提示词 |
| --- | --- | --- |
| 铁锤 | 暗红；主动侦察、集中突破，保留必要防空与经济 | [image-prompt.txt](../assets/commanders/hammer/image-prompt.txt) |
| 堡垒 | 冷蓝；稳固资源与防线、保留预备力量，依据已侦察威胁支援 | [image-prompt.txt](../assets/commanders/bastion/image-prompt.txt) |
| 幽灵 | 琥珀；侦察侧翼与撤退路线，以机动与协同建立局部优势 | [image-prompt.txt](../assets/commanders/ghost/image-prompt.txt) |

原工程使用以下参数导出网页版本，现有导出文件原样收录。以下命令在各人物资源目录执行，需要另行安装 `cwebp`：

```sh
cwebp -q 86 -m 6 source.png -o image.webp
cwebp -q 88 -m 6 -crop 750 0 600 750 -resize 384 480 source.png -o portrait.webp
```

横图单张约 171–211 KiB，头像为同图裁切，未重绘人物或修改颜色。

## 轻动作视频

通过 oiioii CLI 调用 **MiniMax-H3**（模型 ID `45`，variant `minimax-h3`），以各人物原始 PNG 为单图参考。服务端使用 `generate_video_minimax_h3` / `omni2Video`。

- 请求参数：`2k`、`16:9`、每条 6 秒。
- 实际原生输出：**2560 × 1440、24 fps、158 帧、约 6.583 秒**。
- 三条均成功生成，各扣 66 积分，共 198 积分；本批没有付费重试。
- `motion-source.mp4` 为带生成音轨的原始下载。
- `motion.mp4` 保留原生 H.264 / yuv420p 视频流，仅移除音轨并将 MP4 索引前置，未缩放或重新编码画面。

| 人物 | 动作方向 | 视频提示词 |
| --- | --- | --- |
| 铁锤 | 轻抬头、调整重心，保持手扶战术桌的稳定姿态 | [motion-prompt.txt](../assets/commanders/hammer/motion-prompt.txt) |
| 堡垒 | 低头查看终端，随后沉着回望战场 | [motion-prompt.txt](../assets/commanders/bastion/motion-prompt.txt) |
| 幽灵 | 轻微侧头观察侧翼，头发与披风轻动 | [motion-prompt.txt](../assets/commanders/ghost/motion-prompt.txt) |

[生成清单](../generation-manifest.json) 保留原任务 ID、参考资源标识、模型参数、实际扣费、尺寸、时长、文件大小和已有 SHA-256；其中本地文件路径已适配本资源工程。字段 `website_video` 表示本仓库的无音轨成片，`native_source_local` 表示本仓库原始视频。清单不包含 API Key、授权请求头或临时签名下载地址。

## 使用与维护

官网原有播放逻辑在 `remix-website` 项目维护，本仓库只维护媒体资源。视频可用于静音循环背景；静态横图可用于加载、减少动态效果偏好或播放失败时的回退。

新增人物时沿用 `assets/commanders/{id}/` 结构，将角色资料和全部资源路径登记到 `catalog.json`。变更生成参数或成片时同步更新 `generation-manifest.json` 的文件大小、校验值和处理说明，再更新 `checksums.sha256` 并执行校验。
