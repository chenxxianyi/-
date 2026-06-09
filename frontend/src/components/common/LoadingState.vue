<template>
  <div class="loading-state" role="status" aria-live="polite">
    <span class="loading-dot" />
    <span>{{ text }}</span>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    text?: string
  }>(),
  {
    text: '正在加载...',
  },
)
</script>
