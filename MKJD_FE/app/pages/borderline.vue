<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-xl font-semibold">Review Borderline</h1>
      <p class="text-sm text-gray-500">Komentar yang berada di area abu-abu.</p>
    </div>

    <EmptyState
      v-if="!borderlineComments.length"
      title="Tidak ada antrean borderline"
      description="Semua komentar sudah memiliki keputusan final."
    />

    <div v-else class="grid gap-4 lg:grid-cols-3">
      <div class="rounded-xl border bg-white p-0">
        <button
          v-for="comment in borderlineComments"
          :key="comment.id"
          type="button"
          :class="[
            'w-full border-b p-4 text-left hover:bg-gray-50 last:border-b-0',
            comment.id === selectedId ? 'bg-gray-50' : '',
          ]"
          @click="selectedId = comment.id"
        >
          <div class="flex items-center justify-between">
            <p class="text-sm font-medium text-gray-900">{{ comment.author || "Anonim" }}</p>
            <span class="text-xs text-gray-400">{{ comment.createdAt }}</span>
          </div>
          <p class="mt-2 max-w-[220px] truncate text-sm text-gray-600">
            {{ comment.text }}
          </p>
          <p class="mt-2 text-xs text-gray-500">{{ comment.videoTitle }}</p>
        </button>
      </div>

      <div class="rounded-xl border bg-white p-4 lg:col-span-2">
        <div v-if="selectedComment" class="space-y-4">
          <div class="flex items-center gap-3">
            <div
              class="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-sky-400 to-cyan-400 text-xs font-semibold text-white"
            >
              {{ selectedComment.authorInitials || "NA" }}
            </div>
            <div>
              <p class="text-sm font-medium text-gray-900">{{ selectedComment.author || "Anonim" }}</p>
              <p class="text-xs text-gray-500">{{ selectedComment.videoTitle }}</p>
            </div>
          </div>

          <div>
            <p class="text-sm text-gray-500">Komentar</p>
            <p class="mt-2 text-sm text-gray-800">{{ selectedComment.text }}</p>
          </div>

          <div class="flex flex-wrap items-center gap-2 text-xs text-gray-500">
            <span>ID: {{ selectedComment.id }}</span>
            <span class="text-gray-300">|</span>
            <span>Skor: {{ selectedComment.score.toFixed(2) }}</span>
            <span class="text-gray-300">|</span>
            <DecisionBadge :decision="selectedComment.decision" />
          </div>

          <div class="flex flex-wrap items-center gap-2">
            <button
              class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50 text-green-700"
              type="button"
              @click="store.updateDecision(selectedComment.id, 'PUBLISHED')"
            >
              Publish
            </button>
            <button
              class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50 text-yellow-700"
              type="button"
              @click="store.updateDecision(selectedComment.id, 'HELD')"
            >
              Hold
            </button>
            <button
              class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50 text-red-600"
              type="button"
              @click="store.updateDecision(selectedComment.id, 'REJECTED')"
            >
              Reject
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watchEffect } from "vue"
import { storeToRefs } from "pinia"
import DecisionBadge from "~/components/DecisionBadge.vue"
import EmptyState from "~/components/EmptyState.vue"
import { useModerationStore } from "~/stores/moderation"

const store = useModerationStore()
const { comments } = storeToRefs(store)

const borderlineComments = computed(() =>
  comments.value.filter((comment) => comment.decision === "BORDERLINE")
)

const selectedId = ref("")

watchEffect(() => {
  if (!borderlineComments.value.length) {
    selectedId.value = ""
    return
  }
  const exists = borderlineComments.value.some((comment) => comment.id === selectedId.value)
  if (!exists) {
    selectedId.value = borderlineComments.value[0].id
  }
})

const selectedComment = computed(() =>
  borderlineComments.value.find((comment) => comment.id === selectedId.value)
)
</script>
