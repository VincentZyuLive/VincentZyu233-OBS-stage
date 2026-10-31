---
title: 软件栈
description: 直播、开发和站点构建软件版本
---

<script setup>
import { software, softwareUpdatedAt } from './data/software.ts'
</script>

# 🧰 软件栈

当前直播与开发工具版本快照，最后核对时间：**{{ softwareUpdatedAt }}**。

<VersionTable :items="software" />
