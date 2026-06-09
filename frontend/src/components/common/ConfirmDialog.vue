<template>
  <n-modal :show="show" preset="dialog" :title="title" :positive-text="positiveText" negative-text="取消" @positive-click="$emit('confirm')" @negative-click="$emit('cancel')" @close="$emit('cancel')">
    {{ content }}
  </n-modal>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    show: boolean
    title: string
    content: string
    positiveText?: string
  }>(),
  {
    positiveText: '确认',
  },
)

defineEmits<{
  confirm: []
  cancel: []
}>()
</script>
