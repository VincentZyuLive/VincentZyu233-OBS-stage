<script setup lang="ts">
defineProps<{
  icon: string;
  label: string;
  value: string;
  detail?: string;
}>();
</script>

<template>
  <article class="hardware-card">
    <span class="hardware-icon" aria-hidden="true">{{ icon }}</span>
    <div>
      <p class="hardware-label">{{ label }}</p>
      <h3>{{ value }}</h3>
      <p v-if="detail" class="hardware-detail">{{ detail }}</p>
    </div>
  </article>
</template>
