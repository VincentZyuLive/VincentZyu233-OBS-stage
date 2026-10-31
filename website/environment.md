---
title: 本机环境
description: VincentZyu 的直播电脑硬件与系统配置
---

<script setup>
import {
  diskSummary,
  environmentNotes,
  environmentUpdatedAt,
  hardware,
} from './.vitepress/data/environment.ts'
</script>

# 🖥️ 本机环境

这是日常直播、开发和测试共用的 Windows 主机。公开硬件配置与系统版本，但隐藏机器名和局域网地址。

> 环境快照：{{ environmentUpdatedAt }}

<div class="hardware-grid">
  <HardwareCard
    v-for="item in hardware"
    :key="item.label"
    :icon="item.icon"
    :label="item.label"
    :value="item.value"
    :detail="item.detail"
  />
</div>

## 💽 磁盘布局

<table>
  <thead><tr><th>盘符</th><th>容量</th><th>用途</th></tr></thead>
  <tbody>
    <tr v-for="item in diskSummary" :key="item.drive">
      <td>{{ item.drive }}</td>
      <td>{{ item.capacity }}</td>
      <td>{{ item.role }}</td>
    </tr>
  </tbody>
</table>

## 🔐 展示边界

<ul>
  <li v-for="note in environmentNotes" :key="note">{{ note }}</li>
</ul>
