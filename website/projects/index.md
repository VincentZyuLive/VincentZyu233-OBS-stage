---
title: 项目
description: OBS Stage 与 Bili Live Danmaku
---

<script setup>
import { projects } from '../data/projects.ts'
</script>

# 📦 项目

两个项目分别负责舞台视觉和直播弹幕，通过 OBS Browser Source 组合成最终直播画面。

<div class="project-grid">
  <ProjectCard v-for="project in projects" :key="project.name" :project="project" />
</div>
