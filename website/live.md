---
title: B站直播间
description: VincentZyu 的 Bilibili 直播入口
---

<script setup>
import { liveRoom } from './data/projects.ts'
</script>

# 📺 B站直播间

<BilibiliBadge />

日常直播使用 OBS Stage 水色雾蓝舞台与 Bili Live Danmaku 透明弹幕面板。

<div class="live-room-card">
  <span>直播间房间号</span>
  <strong>{{ liveRoom.roomId }}</strong>
  <a :href="liveRoom.url" target="_blank" rel="noopener noreferrer">打开 B站直播间 →</a>
</div>
