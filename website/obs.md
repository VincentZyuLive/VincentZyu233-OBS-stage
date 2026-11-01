---
title: OBS 与插件
description: OBS Studio 版本、插件和舞台分层
---

<script setup>
import { obsLayerStack, obsPlugins, obsUpdatedAt } from './data/obs-plugins.ts'
</script>

# 🎛️ OBS 与插件

当前使用 **[OBS Studio 32.2.1](https://github.com/obsproject/obs-studio)**。版本快照：{{ obsUpdatedAt }}。

## 🧱 舞台分层

从下到上的推荐层级与字体资源：

<div class="layer-stack">
  <code v-for="(item, index) in obsLayerStack" :key="index">
    {{ index + 1 }}.
    <template v-for="(segment, segmentIndex) in item.segments" :key="segmentIndex">
      <a v-if="segment.url" :href="segment.url" target="_blank" rel="noopener noreferrer">{{ segment.text }}</a>
      <span v-else>{{ segment.text }}</span>
    </template>
  </code>
</div>

## 🧩 插件与能力

<table>
  <thead><tr><th>名称</th><th>版本</th><th>来源</th><th>用途</th></tr></thead>
  <tbody>
    <tr v-for="item in obsPlugins" :key="item.name">
      <td>
        <a v-if="item.url" :href="item.url" target="_blank" rel="noopener noreferrer">{{ item.name }}</a>
        <span v-else>{{ item.name }}</span>
      </td>
      <td>{{ item.version }}</td>
      <td>{{ item.source }}</td>
      <td>{{ item.purpose }}</td>
    </tr>
  </tbody>
</table>

## 🔌 WebSocket

[OBS WebSocket](https://github.com/obsproject/obs-websocket) 是内置能力，[OBS Stage](https://github.com/VincentZyuLive/VincentZyu233-OBS-stage) 只在用户主动启用并填写密码后使用。默认不修改现有场景和内容源。
