---
title: 本机环境
description: VincentZyu 的直播电脑硬件与系统配置
---

<script setup>
import {
  environmentNotes,
  environmentUpdatedAt,
  hardware,
} from './data/environment.ts'
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

## 🔐 展示边界

<ul>
  <li v-for="note in environmentNotes" :key="note">{{ note }}</li>
</ul>
