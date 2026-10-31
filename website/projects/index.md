---
title: 项目
description: OBS Stage、SPlayer OBS HTML Overlay、go-musicfox 与 Bili Live Danmaku
---

<script setup>
import { projects } from '../data/projects.ts'
</script>

# 📦 项目

四个项目分别负责舞台视觉、歌曲可视化、播放器数据与直播弹幕，通过 OBS Browser Source 组合成最终直播画面。

<div class="project-grid">
  <ProjectCard v-for="project in projects" :key="project.name" :project="project" />
</div>
