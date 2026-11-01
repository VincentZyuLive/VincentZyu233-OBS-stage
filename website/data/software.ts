import type { SoftwareItem } from "./types";

export const softwareUpdatedAt = "2026-10-31";

export const software: SoftwareItem[] = [
  {
    name: "OBS Studio",
    version: "32.2.1",
    category: "直播与合成",
    note: "Windows x64 便携版，浏览器源、OBS WebSocket 与 NVENC 可用。",
    url: "https://obsproject.com/",
  },
  {
    name: "SPlayer-Next",
    version: "1.2.0",
    category: "播放器",
    note: "直播中的歌曲信息、封面和歌词视觉来源。",
    url: "https://github.com/SPlayer-Dev/SPlayer-Next",
  },
  {
    name: "go-musicfox (VincentZyu Fork)",
    version: "5.1.0-fork",
    category: "播放器",
    note: "个人维护的 Go CLI 播放器，提供 SPlayer-Next 兼容的 HTTP/WS API 与 OBS 歌曲 Overlay 数据。",
    url: "https://github.com/VincentZyuLive/go-musicfox-vincentzyu-fork",
  },
  {
    name: "uv",
    version: "0.9.28",
    category: "Python 工具链",
    note: "管理 OBS Stage 与 Bili Live Danmaku 的依赖和命令入口。",
    url: "https://docs.astral.sh/uv/",
  },
  {
    name: "Python",
    version: "3.13.11",
    category: "运行时",
    note: "当前 uv 环境实际版本；项目声明支持 Python 3.12+。",
    url: "https://www.python.org/",
  },
  {
    name: "Node.js",
    version: "22.17.0",
    category: "前端工具链",
    note: "用于构建本地 WebUI 和 VitePress 环境站。",
    url: "https://nodejs.org/",
  },
  {
    name: "npm",
    version: "10.9.2",
    category: "包管理",
    note: "安装并构建 VitePress 站点。",
    url: "https://www.npmjs.com/",
  },
  {
    name: "Git",
    version: "2.50.0",
    category: "版本控制",
    note: "Windows 版 Git for Windows。",
    url: "https://git-scm.com/",
  },
  {
    name: "Windows Terminal",
    version: "1.24.12741",
    category: "终端",
    note: "PowerShell 5.1 与本地开发工具的日常入口。",
    url: "https://github.com/microsoft/terminal",
  },
];
