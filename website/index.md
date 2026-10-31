---
layout: home

hero:
  name: "VincentZyu Live Lab"
  text: "水色雾蓝直播环境"
  tagline: 硬件、OBS、舞台、播放器与弹幕工具，把直播环境做成一套可维护的系统。
  image:
    src: /brand/obs-stage-avatar.png
    alt: VincentZyu Live Lab
  actions:
    - theme: brand
      text: 进入 B站直播间
      link: https://live.bilibili.com/5861873
    - theme: alt
      text: 查看本机环境
      link: /environment

features:
  - icon: 🎛️
    title: OBS 舞台
    details: 1600×900 水色雾蓝舞台、三场景布局与可选 OBS WebSocket 自动套用。
  - icon: 💬
    title: B站弹幕
    details: 透明弹幕面板、礼物与 SC、历史记录、LXGW 字体与 Cookie 助手。
  - icon: 🪟
    title: HTML Overlay
    details: 透明毛玻璃歌词挂件，在 OBS 中展示封面、歌曲信息、进度与三行歌词。
  - icon: 🦊
    title: Musicfox 外部 API
    details: go-musicfox fork 提供 SPlayer-Next 兼容 HTTP/WS API，为 OBS 输出歌曲、封面和歌词。
  - icon: 🧰
    title: 可复现环境
    details: 硬件、系统、OBS 插件和开发工具版本集中记录，便于迁移和排障。
---

<script setup>
import { liveRoom, projects } from './data/projects.ts'
</script>

<div class="home-live-entry">
  <div class="home-live-copy">
    <p class="home-live-kicker">LIVE ON BILIBILI</p>
    <h2>B站直播间</h2>
    <p>直播时会使用 OBS Stage 舞台、go-musicfox 数据、SPlayer OBS HTML Overlay 与 Bili Live Danmaku 弹幕面板。</p>
  </div>
  <BilibiliBadge />
</div>

## 🚀 四个直播工具

<div class="project-grid">
  <ProjectCard v-for="project in projects" :key="project.name" :project="project" />
</div>
