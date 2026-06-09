<template>
  <div class="tab-pane active ai-pane">
    <div class="ai-actions">
      <button class="button secondary" @click="$emit('summary')">总结当前文档</button>
      <button class="button secondary" @click="$emit('explain')">解释选中文本</button>
      <button class="button secondary" @click="$emit('translate')">翻译选中文本</button>
    </div>
    <label class="ai-question">
      <span>基于文档提问</span>
      <textarea v-model="question" rows="3" placeholder="这篇文档主要讲了什么？" />
    </label>
    <button class="button primary full" @click="$emit('ask', question || '这篇文档主要讲了什么？')">提问</button>
    <div class="ai-answer">
      <strong>{{ answer.title }}</strong>
      <p>{{ answer.text }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  answer: { title: string; text: string }
}>()

defineEmits<{
  summary: []
  explain: []
  translate: []
  ask: [question: string]
}>()

const question = ref('')
</script>
