---
title: go-musicfox (VincentZyu Fork)
description: SPlayer-Next 兼容的 CLI 播放器与 OBS 数据 API
---

# 🦊 go-musicfox (VincentZyu Fork)

go-musicfox 是使用 Go 和 Bubble Tea 编写的网易云音乐命令行客户端。这个个人 fork 在保留上游
TUI 和播放能力的基础上，新增了面向 OBS 和直播工具链的 SPlayer-Next 兼容外部 API。

## ✨ 核心能力

- 与 SPlayer-Next 对齐的 HTTP API：`/api/info`、`/api/status`、`/api/now-playing`、`/api/lyrics`
- `/ws` 实时推送歌曲、歌词和播放状态，并支持播放、暂停、切歌、跳转与音量控制
- 为 OBS Overlay 提供歌曲标题、歌手、专辑、封面、LRC/YRC 歌词和逐字时间
- 支持本地文件页面 Origin，适配 OBS Browser Source
- HTTP 轮询兜底，WebSocket 暂时不可用时仍可更新封面、歌名和歌词
- Windows 桌面快捷方式，默认通过 `127.0.0.1:14558` 暴露本地 API
- 个人 fork 与上游 PR 双线维护：fork 保留头像品牌，上游分支保持原始视觉

## 🔌 OBS 数据链路

```text
go-musicfox → HTTP / WebSocket :14558 → OBS HTML Overlay → OBS Browser Source
```

HTTP 与 WebSocket 共用 `14558` 端口。服务默认只监听本机，不开放局域网访问，也不包含身份鉴权。

## 🖼️ 实机预览

![go-musicfox 与 OBS HTML Overlay 实机效果](/images/preview.musicfox.png)

<BilibiliBadge />

## 🔗 相关链接

- [go-musicfox fork 仓库](https://github.com/VincentZyuLive/go-musicfox-vincentzyu-fork)
- [上游 go-musicfox](https://github.com/go-musicfox/go-musicfox)
- [上游 PR #690](https://github.com/go-musicfox/go-musicfox/pull/690)
- [SPlayer OBS HTML Overlay 项目页](/projects/splayer-obs-html-overlay)
- [SPlayer-Next OBS Overlay](https://github.com/VincentZyuLive/splayer-status-html-overlay-for-obs)

