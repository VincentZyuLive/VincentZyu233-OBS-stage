import type { ProjectCardData } from "./types";

export const projects: ProjectCardData[] = [
  {
    name: "OBS Stage",
    version: "0.1.0",
    description: "可编辑的水色雾蓝舞台背景、前景装饰与 OBS WebSocket 管理工具。",
    repo: "https://github.com/VincentZyu233/VincentZyu233-OBS-stage",
    preview: "/images/preview.webui.png",
    accent: "#7FA8E8",
    tags: ["OBS", "WebUI", "Watercolor"],
  },
  {
    name: "go-musicfox (VincentZyu Fork)",
    version: "5.1.0-fork",
    description: "基于 go-musicfox 的 CLI 播放器 fork，新增 SPlayer-Next 兼容 HTTP/WebSocket API，为 OBS 提供歌曲、封面与歌词数据。",
    repo: "https://github.com/VincentZyu233/go-musicfox-vincentzyu-fork",
    preview: "/images/preview.musicfox.card.png",
    accent: "#E36229",
    tags: ["Go", "CLI", "OBS", "WebSocket"],
  },
  {
    name: "Bili Live Danmaku",
    version: "0.1.0",
    description: "透明 B站弹幕面板，支持礼物、入场、SC、历史、自定义字体与 Cookie 助手。",
    repo: "https://github.com/VincentZyu233/bili-live-danmaku",
    preview: "/images/preview.obs.png",
    accent: "#F4C6D7",
    tags: ["Bilibili", "Danmaku", "Obs"],
  },
];

export const liveRoom = {
  platform: "Bilibili Live",
  roomId: "5861873",
  url: "https://live.bilibili.com/5861873",
  badge:
    "https://img.shields.io/badge/Bilibili-5861873-00A1D6?style=for-the-badge&logo=bilibili&logoColor=white",
};
