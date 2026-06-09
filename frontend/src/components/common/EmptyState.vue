<template>
  <div class="empty-state">
    <strong>{{ title }}</strong>
    <span>{{ description }}</span>
    <slot />
  </div>
</template>

<script setup lang="ts">
defineProps<{
  title: string
  description: string
}>()
</script>
