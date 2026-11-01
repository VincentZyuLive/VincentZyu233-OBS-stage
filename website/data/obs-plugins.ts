import type { ObsLayerItem, ObsPlugin } from "./types";

const obsStudioRepo = "https://github.com/obsproject/obs-studio";
const obsStageRepo = "https://github.com/VincentZyuLive/VincentZyu233-OBS-stage";
const splayerOverlayRepo = "https://github.com/VincentZyuLive/splayer-status-html-overlay-for-obs";
const goMusicfoxRepo = "https://github.com/VincentZyuLive/go-musicfox-vincentzyu-fork";
const biliDanmakuRepo = "https://github.com/VincentZyuLive/bili-live-danmaku";

export const obsUpdatedAt = "2026-10-31";

export const obsPlugins: ObsPlugin[] = [
  {
    name: "OBS Browser",
    version: "32.2.1",
    source: "OBS 内置",
    purpose: "运行 OBS Stage 前景层、SPlayer OBS HTML Overlay 与 Bili Live Danmaku 透明弹幕层。",
    url: "https://github.com/obsproject/obs-browser",
  },
  {
    name: "OBS WebSocket",
    version: "内置 v5",
    source: "OBS 内置",
    purpose: "供可选的一键舞台层创建、真实场景截图与外部控制使用。",
    url: "https://github.com/obsproject/obs-websocket",
  },
  {
    name: "NVENC",
    version: "32.2.1",
    source: "OBS 内置",
    purpose: "在 RTX 3060 上使用硬件编码，降低直播编码 CPU 压力。",
    url: obsStudioRepo,
  },
  {
    name: "FFmpeg / Win Capture",
    version: "32.2.1",
    source: "OBS 内置",
    purpose: "媒体处理、显示器与窗口采集。",
    url: obsStudioRepo,
  },
  {
    name: "Move Transition",
    version: "3.2.1",
    source: "第三方",
    purpose: "为场景切换与来源移动提供过渡动画。",
    url: "https://github.com/exeldro/obs-move-transition",
  },
];

export const obsLayerStack: ObsLayerItem[] = [
  {
    segments: [
      { text: "Stage BG [scene]", url: obsStageRepo },
      { text: " · 舞台背景图片" },
    ],
  },
  {
    segments: [
      { text: "显示器采集 / 窗口采集", url: obsStudioRepo },
      { text: " / " },
      { text: "go-musicfox", url: goMusicfoxRepo },
      { text: "（或 " },
      { text: "SPlayer", url: "https://github.com/SPlayer-Dev/SPlayer-Next" },
      { text: "）· 真实内容源" },
    ],
  },
  {
    segments: [
      { text: "Stage Frame [scene]", url: obsStageRepo },
      { text: " · 透明前景浏览器源" },
    ],
  },
  {
    segments: [
      { text: "splayer-overlay", url: splayerOverlayRepo },
      { text: " · 歌曲封面与歌词 HTML Overlay" },
    ],
  },
  {
    segments: [
      { text: "danmaku", url: biliDanmakuRepo },
      { text: " · B站弹幕浏览器源" },
    ],
  },
  {
    segments: [
      { text: "LXGW WenKai", url: "https://github.com/lxgw/LxgwWenKai" },
      { text: " · 弹幕与 Overlay 字体资源" },
    ],
  },
  {
    segments: [{ text: "通知、字幕等临时层" }],
  },
];
