---
title: SPlayer OBS HTML Overlay
description: OBS 透明毛玻璃音乐与歌词挂件
---

# 🎵 SPlayer OBS HTML Overlay

SPlayer OBS HTML Overlay 是一个直接运行在 OBS Browser Source 中的透明 HTML 挂件，用来展示
当前歌曲的封面、标题、歌手、播放进度和三行歌词。它使用 SPlayer-Next 兼容的外部 API，也可以
直接连接 go-musicfox 个人 fork。

## ✨ 核心能力

- 展示封面、歌曲信息、播放进度、时间戳和播放状态
- 原文、中文翻译、罗马音三行歌词，纯中文歌自动隐藏多余行
- 透明毛玻璃卡片，适配亮色和暗色游戏画面
- WebSocket 实时更新，断线后自动重连
- 支持 LXGW WenKai 字体下载、自定义字体和系统字体
- `configure.py` 可修改 API host、端口和字体路径
- 以本地 `index.html` 加载，不需要额外运行网页服务器
- 与 SPlayer-Next、go-musicfox 外部 API 共用 `127.0.0.1:14558`

## 🔌 OBS 数据链路

```mermaid
flowchart LR
  A["go-musicfox / SPlayer-Next"] -->|"HTTP / WebSocket :14558"| B["index.html"]
  B --> C["OBS Browser Source"]

  classDef client fill:#14243b,stroke:#7fa8e8,color:#f4f7ff
  classDef bridge fill:#101c30,stroke:#a7c8ff,color:#f4f7ff
  classDef obs fill:#17253a,stroke:#f4c6d7,color:#f4f7ff
  class A client
  class B bridge
  class C obs
```

## ⚙️ 快速配置

1. 克隆 Overlay 仓库，按需运行 `download_font.py` 下载 LXGW WenKai。
2. 使用 `configure.py` 确认 `apiHost=127.0.0.1`、`apiPort=14558` 和字体路径。
3. 在 OBS 添加“浏览器”来源，勾选“本地文件”，选择 `index.html`。
4. 推荐尺寸 `1080×240`，自定义帧率优先使用 `60 FPS`。
5. 保持该来源位于游戏画面之上、B站弹幕层之下。

## 🖼️ 预览

> ↓ 透明浮层效果：独立展示歌曲封面、歌名、歌词、播放进度与时间。

![透明浮层效果](/images/preview.splayer-obs-html-overlay.overlay-only.png)

> ↓ OBS 端效果：浏览器源 `splayer-overlay` 叠加在 OBS 中的实际效果。

![SPlayer OBS HTML Overlay 在 OBS 中的效果](/images/preview.splayer-obs-html-overlay.png)

> ↓ B站手机客户端效果：同一套歌词挂件在手机直播间的观看效果。

![SPlayer OBS HTML Overlay 在 B站手机端的观看效果](/images/preview.splayer-obs-html-overlay.phone.png)

<BilibiliBadge />

## 🔗 相关链接

- [SPlayer OBS HTML Overlay 仓库](https://github.com/VincentZyuLive/splayer-status-html-overlay-for-obs)
- [go-musicfox (VincentZyu Fork) 项目页](/projects/musicfox)
- [SPlayer-Next](https://github.com/SPlayer-Dev/SPlayer-Next)
- [LXGW WenKai](https://github.com/lxgw/LxgwWenKai)

