<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-xl font-semibold">Ringkasan Moderasi</h1>
      <p class="text-sm text-gray-500">Pantau aktivitas komentar dan metrik moderasi Anda.</p>
    </div>

    <div class="rounded-xl border bg-white p-4 shadow-sm">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p class="text-sm text-gray-500">Status Sistem</p>
          <p class="text-lg font-semibold text-gray-900">{{ systemTitle }}</p>
          <p class="text-xs text-gray-500">Kanal: {{ channelName }}</p>
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <span :class="[statusBadgeBase, connectionBadgeClass]">
            OAuth {{ oauthStatus.connected ? "Connected" : "Disconnected" }}
          </span>
          <span :class="[statusBadgeBase, pipelineBadgeClass]">
            Pipeline {{ pipelineStatusLabel }}
          </span>
          <span class="inline-flex rounded-full bg-sky-100 px-2 py-1 text-xs font-medium text-sky-700">
            {{ modelMetrics.modelName }} {{ modelMetrics.version }}
          </span>
        </div>
      </div>
      <div class="mt-3 flex flex-wrap items-center gap-3 text-xs text-gray-500">
        <span>Last Sync: {{ oauthStatus.lastSync }}</span>
        <span class="text-gray-300">|</span>
        <span>Last Fetch: {{ pipelineStatus.lastFetch }}</span>
        <button
          type="button"
          class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50"
          @click="refreshSync"
        >
          Refresh Sync
        </button>
      </div>
    </div>

    <div class="grid gap-4 md:grid-cols-3 lg:grid-cols-6">
      <StatCard title="Komentar Baru" :value="totalCount" :trend="`${recentCount} dalam 24 jam terakhir`">
        <template #icon>
          <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M4 7h16v8H7l-3 3z" />
          </svg>
        </template>
      </StatCard>
      <StatCard title="Diterbitkan" :value="publishedCount" :trend="`${publishedToday} diterbitkan hari ini`">
        <template #icon>
          <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M20 6L9 17l-5-5" />
          </svg>
        </template>
      </StatCard>
      <StatCard title="Tertahan" :value="heldCount" :trend="heldRate">
        <template #icon>
          <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <circle cx="12" cy="12" r="9" />
            <path d="M12 7v5l3 3" />
          </svg>
        </template>
      </StatCard>
      <StatCard title="Ditolak" :value="rejectedCount" trend="Spam terdeteksi">
        <template #icon>
          <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M6 6l12 12" />
            <path d="M18 6l-12 12" />
          </svg>
        </template>
      </StatCard>
      <StatCard title="Menunggu" :value="borderlineCount" trend="Perlu review manual">
        <template #icon>
          <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M12 3l9 16H3z" />
          </svg>
        </template>
      </StatCard>
      <StatCard title="Median Score" :value="medianScore" trend="Median skor model">
        <template #icon>
          <svg class="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8">
            <path d="M4 17l4-5 4 3 6-8" />
          </svg>
        </template>
      </StatCard>
    </div>

    <div class="rounded-xl border bg-white p-4">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm font-medium">Volume Komentar</p>
          <p class="text-xs text-gray-500">Distribusi komentar dalam 24 jam terakhir</p>
        </div>
        <span class="text-xs text-gray-400">Chart placeholder</span>
      </div>
      <div class="mt-4 h-32 rounded-lg bg-gradient-to-r from-sky-100 via-white to-cyan-100"></div>
      <div class="mt-3 flex justify-between text-xs text-gray-400">
        <span>00:00</span>
        <span>04:00</span>
        <span>08:00</span>
        <span>12:00</span>
        <span>16:00</span>
        <span>20:00</span>
      </div>
    </div>

    <div class="grid gap-4 lg:grid-cols-3">
      <div class="rounded-xl border bg-white p-4">
        <p class="text-sm font-medium">Tugas Cepat</p>
        <p class="text-xs text-gray-500">Akses fitur utama dengan cepat</p>
        <div class="mt-3 space-y-2">
          <NuxtLink
            to="/comments"
            class="flex items-center justify-between rounded-lg border bg-gray-50 px-3 py-2 text-sm hover:bg-gray-100"
          >
            <span>Tinjau Antrian ({{ pendingCount }} menunggu)</span>
            <span class="text-xs text-gray-400">Buka</span>
          </NuxtLink>
          <NuxtLink
            to="/borderline"
            class="flex items-center justify-between rounded-lg border bg-gray-50 px-3 py-2 text-sm hover:bg-gray-100"
          >
            <span>Review Borderline</span>
            <span class="text-xs text-gray-400">Buka</span>
          </NuxtLink>
          <NuxtLink
            to="/audit"
            class="flex items-center justify-between rounded-lg border bg-gray-50 px-3 py-2 text-sm hover:bg-gray-100"
          >
            <span>Lihat Riwayat</span>
            <span class="text-xs text-gray-400">Buka</span>
          </NuxtLink>
        </div>
      </div>

      <div class="rounded-xl border bg-white p-4 lg:col-span-2">
        <p class="text-sm font-medium">Video Terbaru</p>
        <p class="text-xs text-gray-500">Video dengan aktivitas komentar tertinggi</p>
        <div class="mt-3 space-y-2">
          <div
            v-for="video in topVideos"
            :key="video.title"
            class="flex items-center justify-between rounded-lg border bg-gray-50 px-3 py-2"
          >
            <div class="flex items-center gap-3">
              <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-white shadow-sm">
                <div class="h-4 w-4 rounded bg-gray-200"></div>
              </div>
              <div>
                <p class="text-sm font-medium text-gray-900">{{ video.title }}</p>
                <p class="text-xs text-gray-500">{{ video.total }} komentar</p>
              </div>
            </div>
            <span class="text-xs text-red-500">{{ video.pending }} menunggu</span>
          </div>
        </div>
      </div>
    </div>

    <div class="rounded-xl border bg-white">
      <div class="border-b p-3">
        <p class="text-sm font-medium">Aktivitas Terbaru</p>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-left">
            <tr>
              <th class="p-3">Waktu</th>
              <th class="p-3">Aksi</th>
              <th class="p-3">Target</th>
              <th class="p-3">Actor</th>
              <th class="p-3">Result</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in latestLogs" :key="log.id" class="border-t hover:bg-gray-50">
              <td class="p-3">{{ log.at }}</td>
              <td class="p-3">{{ log.action }}</td>
              <td class="p-3">{{ log.commentId || log.note }}</td>
              <td class="p-3">{{ log.actor }}</td>
              <td class="p-3">
                <span
                  :class="log.result === 'OK' ? 'text-green-700' : 'text-red-600'"
                  class="text-xs font-semibold"
                >
                  {{ log.result }}
                </span>
              </td>
            </tr>
            <tr v-if="!latestLogs.length" class="border-t">
              <td class="p-3 text-center text-sm text-gray-500" colspan="5">
                Belum ada aktivitas.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import StatCard from "~/components/StatCard.vue"
import { useModerationStore } from "~/stores/moderation"

const store = useModerationStore()
const { comments, auditLogs, oauthStatus, modelMetrics, pipelineStatus } = storeToRefs(store)

const totalCount = computed(() => comments.value.length)
const publishedCount = computed(
  () => comments.value.filter((comment) => comment.decision === "PUBLISHED").length
)
const heldCount = computed(
  () => comments.value.filter((comment) => comment.decision === "HELD").length
)
const rejectedCount = computed(
  () => comments.value.filter((comment) => comment.decision === "REJECTED").length
)
const borderlineCount = computed(
  () => comments.value.filter((comment) => comment.decision === "BORDERLINE").length
)

const medianScore = computed(() => {
  const scores = comments.value.map((comment) => comment.score).sort((a, b) => a - b)
  if (!scores.length) return "0.00"
  const mid = Math.floor(scores.length / 2)
  const median = scores.length % 2 === 0 ? (scores[mid - 1] + scores[mid]) / 2 : scores[mid]
  return median.toFixed(2)
})

const parseDate = (value) => new Date(value.replace(" ", "T"))

const latestDate = computed(() => {
  if (!comments.value.length) return new Date()
  const max = Math.max(...comments.value.map((comment) => parseDate(comment.createdAt).getTime()))
  return new Date(max)
})

const recentCount = computed(() => {
  const latest = latestDate.value.getTime()
  const dayMs = 1000 * 60 * 60 * 24
  return comments.value.filter((comment) => {
    const time = parseDate(comment.createdAt).getTime()
    return latest - time <= dayMs
  }).length
})

const publishedToday = computed(() => {
  const latest = latestDate.value.getTime()
  const dayMs = 1000 * 60 * 60 * 24
  return comments.value.filter((comment) => {
    if (comment.decision !== "PUBLISHED") return false
    const time = parseDate(comment.createdAt).getTime()
    return latest - time <= dayMs
  }).length
})

const heldRate = computed(() => {
  if (!totalCount.value) return "0% ditahan"
  const held = heldCount.value + borderlineCount.value
  const rate = ((held / totalCount.value) * 100).toFixed(1)
  return `${rate}% ditahan`
})

const pendingCount = computed(() =>
  comments.value.filter((comment) => comment.decision !== "PUBLISHED").length
)

const latestLogs = computed(() => auditLogs.value.slice(0, 5))

const topVideos = computed(() => {
  const map = new Map()
  comments.value.forEach((comment) => {
    if (!map.has(comment.videoTitle)) {
      map.set(comment.videoTitle, { title: comment.videoTitle, total: 0, pending: 0 })
    }
    const entry = map.get(comment.videoTitle)
    entry.total += 1
    if (comment.decision !== "PUBLISHED") entry.pending += 1
  })
  return Array.from(map.values()).sort((a, b) => b.pending - a.pending).slice(0, 3)
})

const statusBadgeBase = "inline-flex rounded-full px-2 py-1 text-xs font-medium"

const connectionBadgeClass = computed(() =>
  oauthStatus.value.connected ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
)

const pipelineStatusLabel = computed(() => {
  if (pipelineStatus.value.status === "RUNNING") return "Running"
  if (pipelineStatus.value.status === "PAUSED") return "Paused"
  return "Error"
})

const pipelineBadgeClass = computed(() => {
  if (pipelineStatus.value.status === "RUNNING") return "bg-green-100 text-green-700"
  if (pipelineStatus.value.status === "PAUSED") return "bg-yellow-100 text-yellow-800"
  return "bg-red-100 text-red-700"
})

const systemTitle = computed(() => {
  if (oauthStatus.value.connected && pipelineStatus.value.status === "RUNNING") {
    return "Moderasi Proaktif Aktif"
  }
  if (!oauthStatus.value.connected) return "Perlu Validasi OAuth"
  return "Pipeline Perlu Dicek"
})

const channelName = computed(() =>
  oauthStatus.value.channelName ? oauthStatus.value.channelName : "Kanal belum dipilih"
)

const refreshSync = () => {
  store.refreshSync("system")
}
</script>
