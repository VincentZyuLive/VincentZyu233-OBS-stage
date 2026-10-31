import type { ObsPlugin } from "./types";

export const obsUpdatedAt = "2026-10-31";

export const obsPlugins: ObsPlugin[] = [
  {
    name: "OBS Browser",
    version: "32.2.1",
    source: "OBS 内置",
    purpose: "运行 OBS Stage 前景层、SPlayer OBS HTML Overlay 与 Bili Live Danmaku 透明弹幕层。",
  },
  {
    name: "OBS WebSocket",
    version: "内置 v5",
    source: "OBS 内置",
    purpose: "供可选的一键舞台层创建、真实场景截图与外部控制使用。",
  },
  {
    name: "NVENC",
    version: "32.2.1",
    source: "OBS 内置",
    purpose: "在 RTX 3060 上使用硬件编码，降低直播编码 CPU 压力。",
  },
  {
    name: "FFmpeg / Win Capture",
    version: "32.2.1",
    source: "OBS 内置",
    purpose: "媒体处理、显示器与窗口采集。",
  },
  {
    name: "Move Transition",
    version: "3.2.1",
    source: "第三方",
    purpose: "为场景切换与来源移动提供过渡动画。",
  },
];

export const obsLayerStack = [
  "Stage BG [scene] · 舞台背景图片",
  "显示器采集 / 窗口采集 / go-musicfox（或 SPlayer）· 真实内容源",
  "Stage Frame [scene] · 透明前景浏览器源",
  "splayer-overlay · 歌曲封面与歌词 HTML Overlay",
  "danmaku · B站弹幕浏览器源",
  "通知、字幕等临时层",
];
