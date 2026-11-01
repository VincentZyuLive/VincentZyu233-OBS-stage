---
title: Bili Live Danmaku
description: B站透明弹幕 OBS 浮层
---

# 💬 Bili Live Danmaku

Bili Live Danmaku 是直播中的透明弹幕面板，负责把 B站直播事件渲染成 OBS Browser Source 画面。

## ✨ 核心能力

- 普通弹幕、表情、头像、礼物、入场、点赞、SC 和舰长
- 礼物与入场合并、历史弹幕恢复
- 可配置整块圆角面板、字体、字号和颜色
- 内置 LXGW WenKai Mono
- Cookie 助手与匿名连接提示
- 与 OBS Stage 分开运行，默认端口 `6161`

<BilibiliBadge />

![Bili Live Danmaku 在 OBS 中的效果](/images/preview.bili-live-danmaku.png)

## 🎵 相关歌曲视觉链路

go-musicfox 提供 SPlayer-Next 兼容歌曲数据，SPlayer OBS HTML Overlay 负责在 OBS 中渲染
封面与歌词，再与本弹幕层组合成完整直播画面。

[查看 SPlayer OBS HTML Overlay →](/projects/splayer-obs-html-overlay)
[查看 go-musicfox (VincentZyu Fork) →](/projects/musicfox)

[查看 Bili Live Danmaku GitHub 仓库](https://github.com/VincentZyuLive/bili-live-danmaku)
