<template>
  <div class="flex min-h-screen bg-transparent">
    <Sidebar />
    <div class="relative flex-1">
      <div
        class="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(14,116,144,0.12),_transparent_55%)]"
      ></div>
      <main class="relative flex min-h-screen flex-col p-6">
        <header class="flex flex-wrap items-center justify-between gap-4">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-2xl bg-white shadow-sm">
              <div class="h-5 w-5 rounded-md bg-gradient-to-br from-sky-500 to-cyan-500"></div>
            </div>
            <div>
              <p class="text-xs uppercase tracking-wide text-gray-400">
                UI/UX Moderasi Komentar YouTube
              </p>
              <p class="text-base font-semibold text-gray-900">{{ pageTitle }}</p>
            </div>
          </div>
          <div class="flex flex-wrap items-center gap-3">
            <span
              class="inline-flex items-center gap-2 rounded-full border bg-white px-3 py-1 text-xs text-gray-600"
            >
              <span
                :class="[
                  'h-2 w-2 rounded-full',
                  oauthStatus.connected ? 'bg-green-500' : 'bg-gray-400',
                ]"
              ></span>
              {{ oauthStatus.connected ? "Terhubung" : "Belum Terhubung" }}
            </span>
            <div class="flex items-center gap-3 rounded-full border bg-white px-3 py-2 shadow-sm">
              <div class="h-9 w-9 rounded-full bg-gradient-to-br from-sky-400 to-cyan-400"></div>
              <div class="text-sm">
                <p class="font-medium text-gray-900">{{ channelName }}</p>
                <p class="text-xs text-gray-500">{{ channelHandle }}</p>
              </div>
            </div>
          </div>
        </header>
        <div class="mt-4">
          <slot />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import Sidebar from "~/components/Sidebar.vue"
import { useModerationStore } from "~/stores/moderation"

const route = useRoute()
const store = useModerationStore()
const { oauthStatus } = storeToRefs(store)

const pageTitleMap = {
  "/": "Beranda",
  "/comments": "Antrian Moderasi",
  "/borderline": "Review Borderline",
  "/settings": "Preferensi",
  "/audit": "Riwayat",
}

const pageTitle = computed(() => {
  if (route.path.startsWith("/comments/")) return "Detail Komentar"
  return pageTitleMap[route.path] || "Moderasi"
})

const channelName = computed(() =>
  oauthStatus.value.channelName ? oauthStatus.value.channelName : "Kanal belum dipilih"
)

const channelHandle = computed(() =>
  oauthStatus.value.channelHandle
    ? oauthStatus.value.channelHandle
    : oauthStatus.value.accountEmail || "Belum terhubung"
)
</script>
