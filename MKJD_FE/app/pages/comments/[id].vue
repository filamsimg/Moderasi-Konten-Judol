<template>
  <div class="space-y-4">
    <div>
      <NuxtLink to="/comments" class="text-sky-600 hover:underline text-sm">
        &larr; Kembali
      </NuxtLink>
      <h1 class="text-xl font-semibold">Detail Komentar</h1>
      <p class="text-sm text-gray-500">Rincian komentar dan histori aksi.</p>
    </div>

    <EmptyState
      v-if="!comment"
      title="Komentar tidak ditemukan"
      description="Komentar yang kamu cari tidak tersedia di data dummy."
    />

    <div v-else class="space-y-4">
      <div class="grid gap-4 lg:grid-cols-3">
        <div class="rounded-xl border bg-white p-4 lg:col-span-2 space-y-4">
          <div class="flex items-center gap-3">
            <div
              class="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-sky-400 to-cyan-400 text-xs font-semibold text-white"
            >
              {{ comment.authorInitials || "NA" }}
            </div>
            <div>
              <p class="text-sm font-medium text-gray-900">{{ comment.author || "Anonim" }}</p>
              <p class="text-xs text-gray-500">{{ comment.videoTitle }}</p>
            </div>
          </div>

          <div>
            <p class="text-sm text-gray-500">Komentar</p>
            <p class="mt-2 text-sm text-gray-800">{{ comment.text }}</p>
          </div>
          <div class="flex flex-wrap items-center gap-2">
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
        </div>

        <div class="rounded-xl border bg-white p-4 space-y-3">
          <p class="text-sm font-medium">Metadata</p>
          <div class="space-y-2 text-sm">
            <div class="flex items-center justify-between">
              <span class="text-gray-500">ID</span>
              <span class="font-medium text-gray-800">{{ comment.id }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500">Waktu</span>
              <span class="font-medium text-gray-800">{{ comment.createdAt }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500">Video</span>
              <span class="font-medium text-gray-800">{{ comment.videoTitle }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500">Skor</span>
              <span class="font-medium text-gray-800">{{ comment.score.toFixed(2) }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500">Policy</span>
              <span :class="policyBadgeClass">{{ policyLabel }}</span>
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500">Keputusan</span>
              <DecisionBadge :decision="comment.decision" />
            </div>
            <div class="flex items-center justify-between">
              <span class="text-gray-500">YT Status</span>
              <span class="font-medium text-gray-800">{{ comment.ytStatus }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="rounded-xl border bg-white">
        <div class="border-b p-3">
          <p class="text-sm font-medium">Riwayat Aksi</p>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="bg-gray-50 text-left">
              <tr>
                <th class="p-3">Waktu</th>
                <th class="p-3">From -> To</th>
                <th class="p-3">Actor</th>
                <th class="p-3">Result</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in auditByComment" :key="log.id" class="border-t hover:bg-gray-50">
                <td class="p-3">{{ log.at }}</td>
                <td class="p-3">{{ log.fromDecision }} -> {{ log.toDecision }}</td>
                <td class="p-3">{{ log.actor }}</td>
                <td class="p-3">{{ log.result }}</td>
              </tr>
              <tr v-if="!auditByComment.length" class="border-t">
                <td class="p-3 text-center text-sm text-gray-500" colspan="4">
                  Tidak ada riwayat aksi.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import DecisionBadge from "~/components/DecisionBadge.vue"
import EmptyState from "~/components/EmptyState.vue"
import { useModerationStore } from "~/stores/moderation"

const route = useRoute()
const store = useModerationStore()
const { comments, settings } = storeToRefs(store)

const commentId = computed(() => String(route.params.id || ""))
const comment = computed(() => comments.value.find((item) => item.id === commentId.value))

const auditByComment = computed(() => {
  if (!comment.value) return []
  return store.getAuditByCommentId(comment.value.id)
})

const policyLabel = computed(() => {
  if (!comment.value) return "-"
  const score = comment.value.score
  if (score <= settings.value.thresholdLow) return "LOW"
  if (score >= settings.value.thresholdHigh) return "HIGH"
  return "BORDERLINE"
})

const policyBadgeClass = computed(() => {
  const base = "inline-flex rounded-full px-2 py-1 text-xs font-medium"
  if (policyLabel.value === "LOW") return `${base} bg-green-100 text-green-700`
  if (policyLabel.value === "HIGH") return `${base} bg-red-100 text-red-700`
  if (policyLabel.value === "BORDERLINE") return `${base} bg-yellow-100 text-yellow-800`
  return `${base} bg-gray-100 text-gray-700`
})
</script>
