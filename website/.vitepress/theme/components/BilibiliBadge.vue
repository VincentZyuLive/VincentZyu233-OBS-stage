<script setup lang="ts">
import { liveRoom } from "../../../data/projects.ts";
</script>

<template>
  <a class="bili-live-badge" :href="liveRoom.url" target="_blank" rel="noopener noreferrer">
    <img :src="liveRoom.badge" alt="Bilibili 直播间 5861873" />
  </a>
</template>
