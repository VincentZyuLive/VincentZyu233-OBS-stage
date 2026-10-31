---
title: OBS 与插件
description: OBS Studio 版本、插件和舞台分层
---

<script setup>
import { obsLayerStack, obsPlugins, obsUpdatedAt } from './data/obs-plugins.ts'
</script>

# 🎛️ OBS 与插件

当前使用 **OBS Studio 32.2.1**。版本快照：{{ obsUpdatedAt }}。

## 🧱 舞台分层

从下到上的推荐层级：

<div class="layer-stack">
  <code v-for="(item, index) in obsLayerStack" :key="item">{{ index + 1 }}. {{ item }}</code>
</div>

## 🧩 插件与能力

<table>
  <thead><tr><th>名称</th><th>版本</th><th>来源</th><th>用途</th></tr></thead>
  <tbody>
    <tr v-for="item in obsPlugins" :key="item.name">
      <td>{{ item.name }}</td>
      <td>{{ item.version }}</td>
      <td>{{ item.source }}</td>
      <td>{{ item.purpose }}</td>
    </tr>
  </tbody>
</table>

## 🔌 WebSocket

OBS WebSocket 是内置能力，OBS Stage 只在用户主动启用并填写密码后使用。默认不修改现有场景和内容源。
