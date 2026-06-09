<template>
  <div v-if="visible" class="selection-toolbar" :style="style" role="toolbar" aria-label="选中文本工具栏">
    <button data-action="yellow" title="黄色高亮" @click="$emit('highlight', 'yellow')">黄</button>
    <button data-action="blue" title="蓝色高亮" @click="$emit('highlight', 'blue')">蓝</button>
    <button data-action="green" title="绿色高亮" @click="$emit('highlight', 'green')">绿</button>
    <button data-action="underline" title="红色下划线" @click="$emit('underline')">下划线</button>
    <button data-action="note" title="添加批注" @click="$emit('note')">批注</button>
    <button data-action="excerpt" title="摘录到笔记" @click="$emit('excerpt')">摘录</button>
    <button data-action="explain" title="AI 解释" @click="$emit('explain')">AI</button>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { AnnotationColor } from '@/types/annotation'

const props = defineProps<{
  visible: boolean
  x: number
  y: number
}>()

defineEmits<{
  highlight: [color: Exclude<AnnotationColor, 'red'>]
  underline: []
  note: []
  excerpt: []
  explain: []
}>()

const style = computed(() => ({
  left: `${props.x}px`,
  top: `${props.y}px`,
}))
</script>
