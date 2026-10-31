<script setup lang="ts">
import type { SoftwareItem } from "../../../data/types.ts";

defineProps<{ items: SoftwareItem[] }>();
</script>

<template>
  <div class="version-table">
    <article v-for="item in items" :key="item.name" class="version-row">
      <div class="version-main">
        <div class="version-title">
          <a v-if="item.url" :href="item.url" target="_blank" rel="noopener noreferrer">{{ item.name }}</a>
          <span v-else>{{ item.name }}</span>
          <code>{{ item.version }}</code>
        </div>
        <span class="version-category">{{ item.category }}</span>
      </div>
      <p>{{ item.note }}</p>
    </article>
  </div>
</template>
