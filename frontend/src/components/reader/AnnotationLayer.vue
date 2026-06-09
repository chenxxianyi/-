<template>
  <div class="annotation-layer" aria-hidden="true">
    <span v-for="item in annotations" :key="item.id" class="annotation-layer-mark" :class="[item.color, { active: item.id === activeId }]" />
  </div>
</template>

<script setup lang="ts">
import type { AnnotationItem } from '@/types/annotation'

defineProps<{
  annotations: AnnotationItem[]
  activeId: number | null
}>()
</script>
