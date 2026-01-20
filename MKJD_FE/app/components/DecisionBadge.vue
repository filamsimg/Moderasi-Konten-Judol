<template>
  <span :class="[baseClass, toneClass]">{{ label }}</span>
</template>

<script setup>
import { computed } from "vue"

const props = defineProps({
  decision: { type: String, required: true },
})

const baseClass = "inline-flex rounded-full px-2 py-1 text-xs font-medium"

const label = computed(() => {
  switch (props.decision) {
    case "PUBLISHED":
      return "Diterbitkan"
    case "HELD":
      return "Tertahan"
    case "REJECTED":
      return "Ditolak"
    case "BORDERLINE":
      return "Menunggu"
    default:
      return props.decision
  }
})

const toneClass = computed(() => {
  switch (props.decision) {
    case "PUBLISHED":
      return "bg-green-100 text-green-700"
    case "HELD":
      return "bg-yellow-100 text-yellow-800"
    case "REJECTED":
      return "bg-red-100 text-red-700"
    case "BORDERLINE":
      return "bg-purple-100 text-purple-700"
    default:
      return "bg-gray-100 text-gray-700"
  }
})
</script>
