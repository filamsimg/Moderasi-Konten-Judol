<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-xl font-semibold">Riwayat Aktivitas</h1>
      <p class="text-sm text-gray-500">Riwayat membantu meninjau konsistensi keputusan moderasi.</p>
    </div>

    <div class="rounded-xl border bg-white">
      <div class="border-b p-3 flex flex-wrap items-center justify-between gap-3">
        <div class="flex flex-wrap items-center gap-3">
          <div class="relative">
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
              v-model="keyword"
              type="text"
              placeholder="Cari komentar, aksi, atau aktor"
              class="w-full rounded-lg border px-3 py-2 pl-9 text-sm focus:outline-none focus:ring-2 focus:ring-sky-200 md:w-auto"
            />
          </div>
          <select
            v-model="actionFilter"
            class="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-200 md:w-auto"
          >
            <option value="ALL">Semua Tindakan</option>
            <option value="DECISION_UPDATE">Decision Update</option>
            <option value="SETTINGS_UPDATE">Settings Update</option>
          </select>
          <input
            v-model="dateFilter"
            type="date"
            class="w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-200 md:w-auto"
          />
        </div>
        <button
          type="button"
          class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50"
          @click="exportCsv"
        >
          Ekspor
        </button>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-left">
            <tr>
              <th class="p-3">Waktu</th>
              <th class="p-3">Aksi</th>
              <th class="p-3">CommentId</th>
              <th class="p-3">Skor</th>
              <th class="p-3">Keputusan Sebelum -> Sesudah</th>
              <th class="p-3">Actor</th>
              <th class="p-3">Result</th>
              <th class="p-3">Note</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="log in filteredLogs" :key="log.id" class="border-t hover:bg-gray-50">
              <td class="p-3">{{ log.at }}</td>
              <td class="p-3">{{ log.action }}</td>
              <td class="p-3">{{ formatCommentId(log) }}</td>
              <td class="p-3">{{ formatScore(log) }}</td>
              <td class="p-3">{{ formatDecision(log) }}</td>
              <td class="p-3">{{ log.actor }}</td>
              <td class="p-3">
                <span
                  :class="log.result === 'OK' ? 'text-green-700' : 'text-red-600'"
                  class="text-xs font-semibold"
                >
                  {{ log.result }}
                </span>
              </td>
              <td class="p-3">{{ log.note }}</td>
            </tr>
            <tr v-if="!filteredLogs.length" class="border-t">
              <td class="p-6 text-center text-sm text-gray-500" colspan="8">
                Tidak ada audit log yang cocok.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="rounded-xl border bg-white p-4">
      <p class="text-sm font-medium">Statistik Riwayat</p>
      <div class="mt-3 grid gap-3 md:grid-cols-3">
        <div class="rounded-lg border bg-gray-50 p-3">
          <p class="text-xs text-gray-500">Total Diterbitkan</p>
          <p class="text-lg font-semibold text-gray-900">{{ publishedActions }}</p>
        </div>
        <div class="rounded-lg border bg-gray-50 p-3">
          <p class="text-xs text-gray-500">Total Ditahan</p>
          <p class="text-lg font-semibold text-gray-900">{{ heldActions }}</p>
        </div>
        <div class="rounded-lg border bg-gray-50 p-3">
          <p class="text-xs text-gray-500">Total Ditolak</p>
          <p class="text-lg font-semibold text-gray-900">{{ rejectedActions }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import { storeToRefs } from "pinia"
import { useModerationStore } from "~/stores/moderation"

const store = useModerationStore()
const { auditLogs } = storeToRefs(store)

const keyword = ref("")
const actionFilter = ref("ALL")
const dateFilter = ref("")

const filteredLogs = computed(() => {
  const term = keyword.value.trim().toLowerCase()
  return auditLogs.value.filter((log) => {
    const matchesTerm =
      !term ||
      String(log.commentId || "").toLowerCase().includes(term) ||
      String(log.action || "").toLowerCase().includes(term) ||
      String(log.note || "").toLowerCase().includes(term) ||
      String(log.actor || "").toLowerCase().includes(term)
    const matchesAction = actionFilter.value === "ALL" || log.action === actionFilter.value
    const matchesDate = !dateFilter.value || String(log.at || "").startsWith(dateFilter.value)
    return matchesTerm && matchesAction && matchesDate
  })
})

const publishedActions = computed(
  () => auditLogs.value.filter((log) => log.toDecision === "PUBLISHED").length
)
const heldActions = computed(() => auditLogs.value.filter((log) => log.toDecision === "HELD").length)
const rejectedActions = computed(
  () => auditLogs.value.filter((log) => log.toDecision === "REJECTED").length
)

const formatDecision = (log) => {
  if (log.action === "SETTINGS_UPDATE") return "-"
  return `${log.fromDecision || "-"} -> ${log.toDecision || "-"}`
}

const formatCommentId = (log) => {
  if (log.action === "SETTINGS_UPDATE") return ""
  return log.commentId || ""
}

const formatScore = (log) => {
  if (log.score === null || log.score === undefined) return "-"
  return Number(log.score).toFixed(2)
}

const exportCsv = () => {
  const rows = [
    ["Waktu", "Aksi", "CommentId", "Skor", "From", "To", "Actor", "Result", "Note"],
    ...filteredLogs.value.map((log) => [
      log.at,
      log.action,
      log.commentId || "",
      log.score ?? "",
      log.fromDecision || "",
      log.toDecision || "",
      log.actor,
      log.result,
      log.note,
    ]),
  ]
  const csv = rows
    .map((row) => row.map((cell) => `"${String(cell).replaceAll('"', '""')}"`).join(","))
    .join("\n")
  const blob = new Blob([csv], { type: "text/csv" })
  const url = URL.createObjectURL(blob)
  const link = document.createElement("a")
  link.href = url
  link.download = "audit-log.csv"
  link.click()
  URL.revokeObjectURL(url)
}
</script>
