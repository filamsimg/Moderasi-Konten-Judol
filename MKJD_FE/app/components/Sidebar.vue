<template>
  <aside class="flex w-[260px] flex-col border-r border-slate-200/70 bg-white/90 backdrop-blur p-4">
    <div class="mb-6 flex items-center gap-3">
      <div class="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-sky-500 to-cyan-500 text-white">
        <svg
          class="h-5 w-5"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.8"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M4 5h16v10H4z" />
          <path d="M8 19h8" />
          <path d="M12 15v4" />
        </svg>
      </div>
      <div>
        <p class="text-sm font-semibold text-gray-800">Moderasi YouTube</p>
        <p class="text-xs text-gray-500">Kelola komentar</p>
      </div>
    </div>

    <nav class="space-y-1">
      <NuxtLink
        v-for="item in items"
        :key="item.to"
        :to="item.to"
        :class="[
          baseClass,
          isActive(item.to) ? activeClass : '',
          item.badge ? 'justify-between' : '',
        ]"
      >
        <span class="flex items-center gap-3">
          <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-sky-50 text-sky-700">
            <svg
              class="h-4 w-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path :d="item.icon" />
            </svg>
          </span>
          <span>{{ item.label }}</span>
        </span>
        <span
          v-if="item.badge"
          class="inline-flex h-5 min-w-[20px] items-center justify-center rounded-full bg-sky-100 px-1 text-xs font-semibold text-sky-700"
        >
          {{ item.badge }}
        </span>
      </NuxtLink>
    </nav>

    <div class="mt-auto space-y-3 pt-6">
      <div class="rounded-xl border bg-white p-3">
        <div class="flex items-center gap-2 text-sm">
          <span
            :class="[
              'h-2 w-2 rounded-full',
              oauthStatus.connected ? 'bg-green-500' : 'bg-gray-400',
            ]"
          ></span>
          <span class="font-medium text-gray-700">
            {{ oauthStatus.connected ? "Terhubung" : "Belum Terhubung" }}
          </span>
        </div>
        <p class="mt-1 text-xs text-gray-500">Sync terakhir {{ oauthStatus.lastSync }}</p>
      </div>

      <div class="flex items-center justify-between rounded-xl border bg-white px-3 py-2">
        <span class="text-xs font-medium text-gray-600">Mode Gelap</span>
        <button
          type="button"
          class="relative inline-flex h-5 w-9 items-center rounded-full transition"
          :class="isDark ? 'bg-gray-800' : 'bg-gray-200'"
          @click="toggleTheme"
        >
          <span
            class="inline-block h-4 w-4 translate-x-0 rounded-full bg-white shadow transition"
            :class="isDark ? 'translate-x-4' : 'translate-x-1'"
          ></span>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useModerationStore } from "~/stores/moderation"

const route = useRoute()
const store = useModerationStore()
const { comments, oauthStatus, settings } = storeToRefs(store)

const pendingCount = computed(
  () => comments.value.filter((comment) => comment.decision !== "PUBLISHED").length
)

const items = computed(() => [
  {
    label: "Beranda",
    to: "/",
    icon: "M4 11.5l8-6 8 6V20a1 1 0 0 1-1 1h-4v-6H9v6H5a1 1 0 0 1-1-1z",
  },
  {
    label: "Antrian Moderasi",
    to: "/comments",
    badge: pendingCount.value,
    icon: "M4 7h16v7H7l-3 3V7z",
  },
  {
    label: "Review Borderline",
    to: "/borderline",
    icon: "M12 3l9 16H3z",
  },
  {
    label: "Preferensi",
    to: "/settings",
    icon: "M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z",
  },
  {
    label: "Riwayat",
    to: "/audit",
    icon: "M5 4h14v16H5z",
  },
])

const baseClass = "block rounded-lg px-3 py-2 text-sm hover:bg-gray-100"
const activeClass = "bg-sky-50 text-sky-700 font-medium"

const isActive = (to) => {
  if (to === "/") return route.path === "/"
  return route.path.startsWith(to)
}

const isDark = computed(() => settings.value.theme === "dark")

const toggleTheme = () => {
  store.updateSettings({ theme: isDark.value ? "light" : "dark" })
}
</script>
