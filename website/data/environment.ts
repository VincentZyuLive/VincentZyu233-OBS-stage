import type { HardwareSpec } from "./types";

export const environmentUpdatedAt = "2026-10-31";

export const hardware: HardwareSpec[] = [
  {
    icon: "🪟",
    label: "操作系统",
    value: "Windows 11 IoT Enterprise LTSC 24H2",
    detail: "Build 26100.7171 · x86_64",
  },
  {
    icon: "🧠",
    label: "CPU",
    value: "Intel Core i5-12400F",
    detail: "6 核 12 线程 · 最高 4.40 GHz",
  },
  {
    icon: "🎮",
    label: "独立显卡",
    value: "NVIDIA GeForce RTX 3060",
    detail: "11.83 GiB 显存 · 2.12 GHz",
  },
  {
    icon: "🧩",
    label: "主板",
    value: "BATTLE-AX B660M-D",
  },
  {
    icon: "💾",
    label: "内存",
    value: "31.84 GiB",
    detail: "fastfetch 环境快照",
  },
  {
    icon: "🖥️",
    label: "主显示器",
    value: "AOC U34G2G4R3",
    detail: "3440×1440 · 144 Hz · 34 英寸",
  },
];

export const environmentNotes = [
  "桌面使用 3440×1440、144 Hz 超宽屏，直播画布保持 1920×1080 或 1600×900 的 16:9 输出。",
  "机器同时安装 Parsec、ToDesk、Oray、GameViewer 和 MuMu 的虚拟显示适配器，用于远程访问与模拟器场景。",
  "为保护隐私，本页不公开机器名、局域网 IP 和实时资源占用。",
];
