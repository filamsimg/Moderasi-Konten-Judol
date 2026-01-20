<template>
  <div class="flex flex-wrap items-center gap-3">
    <div class="relative flex-1 min-w-[220px]">
      <span class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
        <svg
          class="h-4 w-4"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <circle cx="11" cy="11" r="7" />
          <path d="M20 20l-3.5-3.5" />
        </svg>
      </span>
      <input
        :class="[inputClass, 'pl-9']"
        type="text"
        :value="keyword"
        placeholder="Cari komentar atau pengguna"
        @input="$emit('update:keyword', $event.target.value)"
      />
    </div>
    <select
      :class="inputClass"
      :value="decisionFilter"
      @change="$emit('update:decisionFilter', $event.target.value)"
    >
      <option value="ALL">Semua Status</option>
      <option value="PUBLISHED">Diterbitkan</option>
      <option value="HELD">Tertahan</option>
      <option value="REJECTED">Ditolak</option>
      <option value="BORDERLINE">Menunggu</option>
    </select>
    <select
      :class="inputClass"
      :value="videoFilter"
      @change="$emit('update:videoFilter', $event.target.value)"
    >
      <option value="ALL">Semua Video</option>
      <option v-for="video in videoOptions" :key="video" :value="video">
        {{ video }}
      </option>
    </select>
  </div>
</template>

<script setup>
defineProps({
  keyword: { type: String, default: "" },
  decisionFilter: { type: String, default: "ALL" },
  videoFilter: { type: String, default: "ALL" },
  videoOptions: { type: Array, default: () => [] },
})

defineEmits(["update:keyword", "update:decisionFilter", "update:videoFilter"])

const inputClass =
  "w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-200 md:w-auto"
</script>
