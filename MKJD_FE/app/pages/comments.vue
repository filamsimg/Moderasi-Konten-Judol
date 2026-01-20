<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-xl font-semibold">Antrian Moderasi</h1>
      <p class="text-sm text-gray-500">Kelola komentar yang membutuhkan tindakan moderasi.</p>
    </div>

    <div class="rounded-xl border bg-white">
      <div class="border-b p-3">
        <FilterBar
          :keyword="keyword"
          :decision-filter="decisionFilter"
          :video-filter="videoFilter"
          :video-options="videoOptions"
          @update:keyword="keyword = $event"
          @update:decisionFilter="decisionFilter = $event"
          @update:videoFilter="videoFilter = $event"
        />
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-left">
            <tr>
              <th class="p-3">Pengguna</th>
              <th class="p-3">Komentar</th>
              <th class="p-3">Video</th>
              <th class="p-3">Status</th>
              <th class="p-3">Waktu</th>
              <th class="p-3">Tindakan</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="comment in filteredComments"
              :key="comment.id"
              :class="[
                'border-t hover:bg-gray-50',
                isFlagged(comment) ? 'bg-red-50/40' : '',
              ]"
            >
              <td class="p-3">
                <div class="flex items-center gap-3">
                  <div
                    class="flex h-9 w-9 items-center justify-center rounded-full bg-gradient-to-br from-sky-400 to-cyan-400 text-xs font-semibold text-white"
                  >
                    {{ comment.authorInitials || "NA" }}
                  </div>
                  <div>
                    <p class="text-sm font-medium text-gray-900">{{ comment.author || "Anonim" }}</p>
                    <p class="text-xs text-gray-500">ID: {{ comment.id }}</p>
                  </div>
                </div>
              </td>
              <td class="p-3">
                <p class="max-w-xl truncate text-gray-700">{{ comment.text }}</p>
                <p class="mt-1 text-xs text-gray-400">Skor: {{ comment.score.toFixed(2) }}</p>
                <p v-if="isFlagged(comment)" class="mt-1 text-xs text-red-600">
                  Pola mencurigakan terdeteksi
                </p>
              </td>
              <td class="p-3">
                <div class="flex items-center gap-2 text-sm text-gray-700">
                  <span class="flex h-7 w-7 items-center justify-center rounded-md bg-gray-100">
                    <span class="h-3 w-3 rounded bg-gray-300"></span>
                  </span>
                  <span>{{ comment.videoTitle }}</span>
                </div>
              </td>
              <td class="p-3">
                <DecisionBadge :decision="comment.decision" />
              </td>
              <td class="p-3 text-gray-600">{{ getRelativeTime(comment.createdAt) }}</td>
              <td class="p-3">
                <div class="flex flex-wrap items-center gap-2">
                  <NuxtLink
                    :to="`/comments/${comment.id}`"
                    class="text-sky-600 hover:underline"
                  >
                    Detail
                  </NuxtLink>
                  <button
                    class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50 text-green-700"
                    type="button"
                    @click="store.updateDecision(comment.id, 'PUBLISHED')"
                  >
                    Publish
                  </button>
                  <button
                    class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50 text-yellow-700"
                    type="button"
                    @click="store.updateDecision(comment.id, 'HELD')"
                  >
                    Hold
                  </button>
                  <button
                    class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50 text-red-600"
                    type="button"
                    @click="store.updateDecision(comment.id, 'REJECTED')"
                  >
                    Reject
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="!filteredComments.length" class="border-t">
              <td class="p-6 text-center text-sm text-gray-500" colspan="6">
                Tidak ada komentar yang sesuai filter.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="flex items-center justify-between border-t p-3 text-sm text-gray-500">
        <span>Menampilkan {{ filteredComments.length }} komentar</span>
        <span>Page 1 of 1</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import { storeToRefs } from "pinia"
import DecisionBadge from "~/components/DecisionBadge.vue"
import FilterBar from "~/components/FilterBar.vue"
import { useModerationStore } from "~/stores/moderation"

const store = useModerationStore()
const { comments, settings } = storeToRefs(store)

const keyword = ref("")
const decisionFilter = ref("ALL")
const videoFilter = ref("ALL")

const videoOptions = computed(() => {
  const unique = new Set(comments.value.map((comment) => comment.videoTitle))
  return Array.from(unique)
})

const parseDate = (value) => new Date(value.replace(" ", "T"))

const latestDate = computed(() => {
  if (!comments.value.length) return new Date()
  const max = Math.max(...comments.value.map((comment) => parseDate(comment.createdAt).getTime()))
  return new Date(max)
})

const getRelativeTime = (value) => {
  const diffMs = latestDate.value.getTime() - parseDate(value).getTime()
  const minutes = Math.max(Math.floor(diffMs / 60000), 0)
  if (minutes < 60) return `${minutes} menit yang lalu`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours} jam yang lalu`
  const days = Math.floor(hours / 24)
  return `${days} hari yang lalu`
}

const isFlagged = (comment) =>
  comment.score >= settings.value.thresholdHigh || comment.decision === "REJECTED"

const filteredComments = computed(() => {
  const term = keyword.value.trim().toLowerCase()
  return comments.value.filter((comment) => {
    const matchesKeyword =
      !term ||
      comment.text.toLowerCase().includes(term) ||
      comment.videoTitle.toLowerCase().includes(term) ||
      String(comment.author || "").toLowerCase().includes(term)
    const matchesDecision =
      decisionFilter.value === "ALL" || comment.decision === decisionFilter.value
    const matchesVideo = videoFilter.value === "ALL" || comment.videoTitle === videoFilter.value
    return matchesKeyword && matchesDecision && matchesVideo
  })
})
</script>
