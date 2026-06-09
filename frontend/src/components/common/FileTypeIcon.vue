<template>
  <span class="file-badge" :class="type">{{ label }}</span>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { DocumentType } from '@/types/document'

const props = defineProps<{
  type: DocumentType
}>()

const label = computed(() => props.type.toUpperCase())
</script>
