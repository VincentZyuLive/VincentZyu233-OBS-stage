<script setup lang="ts">
import { withBase } from "vitepress";
import type { ProjectCardData } from "../../data/types.ts";

const props = defineProps<{ project: ProjectCardData }>();
</script>

<template>
  <article class="project-card" :style="{ '--project-accent': props.project.accent }">
    <img :src="withBase(props.project.preview)" :alt="`${props.project.name} 预览`" loading="lazy" />
    <div class="project-card-body">
      <div class="project-card-head">
        <h3>{{ props.project.name }}</h3>
        <code>v{{ props.project.version }}</code>
      </div>
      <p>{{ props.project.description }}</p>
      <div class="project-tags">
        <span v-for="tag in props.project.tags" :key="tag">{{ tag }}</span>
      </div>
      <a :href="props.project.repo" target="_blank" rel="noopener noreferrer">查看 GitHub 仓库 →</a>
    </div>
  </article>
</template>
