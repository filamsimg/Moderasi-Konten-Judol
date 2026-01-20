<template>
  <div class="rounded-xl border bg-white p-4 shadow-sm transition hover:shadow-md">
    <div class="flex items-start justify-between gap-3">
      <div>
        <p class="text-sm text-gray-500">{{ title }}</p>
        <p class="text-2xl font-semibold">{{ value }}</p>
        <p v-if="subtitle" class="text-xs text-gray-500">{{ subtitle }}</p>
      </div>
      <div
        v-if="$slots.icon"
        class="flex h-9 w-9 items-center justify-center rounded-xl bg-sky-50 text-sky-700"
      >
        <slot name="icon" />
      </div>
    </div>
    <p v-if="trend" class="mt-3 text-xs text-gray-500">{{ trend }}</p>
  </div>
</template>

<script setup>
defineProps({
  title: { type: String, required: true },
  value: { type: [String, Number], required: true },
  subtitle: { type: String, default: "" },
  trend: { type: String, default: "" },
})
</script>
