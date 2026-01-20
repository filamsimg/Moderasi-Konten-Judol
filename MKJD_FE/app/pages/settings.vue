<template>
  <div class="space-y-4">
    <div>
      <h1 class="text-xl font-semibold">Preferensi & Pengaturan</h1>
      <p class="text-sm text-gray-500">Sesuaikan pengalaman moderasi Anda.</p>
    </div>

    <div
      v-if="toastMessage"
      class="inline-flex rounded-full bg-green-100 px-2 py-1 text-xs font-medium text-green-700"
    >
      {{ toastMessage }}
    </div>

    <div class="grid gap-4 lg:grid-cols-2">
      <div class="rounded-xl border bg-white">
        <div class="border-b p-3 flex items-center justify-between">
          <p class="text-sm font-medium">Status Koneksi</p>
          <span :class="[statusBadgeBase, connectionBadgeClass]">
            {{ oauthStatus.connected ? "Izin Aktif" : "Belum Terhubung" }}
          </span>
        </div>
        <div class="p-4 space-y-3 text-sm text-gray-600">
          <div class="flex items-center justify-between">
            <span>Channel</span>
            <span class="font-medium text-gray-800">
              {{ oauthStatus.channelName || "Belum dipilih" }}
            </span>
          </div>
          <div class="flex items-center justify-between">
            <span>Channel ID</span>
            <span class="font-medium text-gray-800">{{ oauthStatus.channelId || "-" }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span>Channel URL</span>
            <a
              v-if="oauthStatus.channelUrl"
              class="text-sky-600 hover:underline"
              :href="oauthStatus.channelUrl"
              target="_blank"
              rel="noopener noreferrer"
            >
              Lihat
            </a>
            <span v-else class="text-gray-400">-</span>
          </div>
          <div class="flex items-center justify-between">
            <span>Last Sync</span>
            <span class="font-medium text-gray-800">{{ oauthStatus.lastSync }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span>Token Expiry</span>
            <span class="font-medium text-gray-800">{{ oauthStatus.tokenExpiry }}</span>
          </div>
          <div class="flex items-start justify-between gap-4">
            <span>Scopes</span>
            <span class="font-medium text-gray-800 text-right">
              {{ scopeList || "Belum ada" }}
            </span>
          </div>
          <div class="flex flex-wrap items-center gap-2 pt-2">
            <button
              class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50"
              :class="oauthStatus.connected ? 'text-red-600' : 'text-green-700'"
              type="button"
              @click="toggleOAuth"
            >
              {{ oauthStatus.connected ? "Putuskan" : "Hubungkan" }}
            </button>
            <button
              class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50"
              type="button"
              @click="refreshSync"
            >
              Refresh Sync
            </button>
          </div>
        </div>
      </div>

      <div class="rounded-xl border bg-white">
        <div class="border-b p-3">
          <p class="text-sm font-medium">Model & Evaluasi</p>
        </div>
        <div class="p-4 space-y-3 text-sm text-gray-600">
          <div class="flex items-center justify-between">
            <span>Model</span>
            <span class="font-medium text-gray-800">
              {{ modelMetrics.modelName }} ({{ modelMetrics.version }})
            </span>
          </div>
          <div class="flex items-center justify-between">
            <span>Updated</span>
            <span class="font-medium text-gray-800">{{ modelMetrics.updatedAt }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span>Precision</span>
            <span class="font-medium text-gray-800">{{ modelMetrics.precision.toFixed(2) }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span>Recall</span>
            <span class="font-medium text-gray-800">{{ modelMetrics.recall.toFixed(2) }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span>F1 Score</span>
            <span class="font-medium text-gray-800">{{ modelMetrics.f1.toFixed(2) }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span>PR-AUC</span>
            <span class="font-medium text-gray-800">{{ modelMetrics.prAuc.toFixed(2) }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span>Latency</span>
            <span class="font-medium text-gray-800">{{ modelMetrics.avgLatencyMs }} ms</span>
          </div>
        </div>
      </div>
    </div>

    <div class="grid gap-4 lg:grid-cols-2">
      <div class="rounded-xl border bg-white">
        <div class="border-b p-3">
          <p class="text-sm font-medium">Tampilan</p>
        </div>
        <div class="p-4 space-y-4">
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Bahasa Antarmuka</label>
            <select v-model="language" :class="inputClass">
              <option value="id">Bahasa Indonesia</option>
              <option value="en">English</option>
            </select>
          </div>
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Tema Warna</label>
            <select v-model="theme" :class="inputClass">
              <option value="light">Terang</option>
              <option value="dark">Gelap</option>
            </select>
          </div>
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Kepadatan Tampilan</label>
            <select v-model="density" :class="inputClass">
              <option value="compact">Ringkas</option>
              <option value="standard">Standar</option>
              <option value="comfortable">Lapang</option>
            </select>
          </div>
        </div>
      </div>

      <div class="rounded-xl border bg-white">
        <div class="border-b p-3">
          <p class="text-sm font-medium">Notifikasi & Otomasi</p>
        </div>
        <div class="p-4 space-y-4">
          <label class="flex items-center justify-between rounded-lg border bg-gray-50 px-3 py-2 text-sm">
            <span>Notifikasi Komentar Baru</span>
            <input v-model="notifyNewComments" type="checkbox" class="h-4 w-4 rounded border-gray-300" />
          </label>
          <label class="flex items-center justify-between rounded-lg border bg-gray-50 px-3 py-2 text-sm">
            <span>Tahan Otomatis Komentar Mencurigakan</span>
            <input v-model="autoHoldSuspicious" type="checkbox" class="h-4 w-4 rounded border-gray-300" />
          </label>
        </div>
      </div>
    </div>

    <div class="rounded-xl border bg-white">
      <div class="border-b p-3">
        <p class="text-sm font-medium">Target Pemantauan</p>
      </div>
      <div class="p-4 space-y-4">
        <div class="grid gap-3 md:grid-cols-4">
          <select v-model="targetForm.type" :class="inputClass">
            <option value="CHANNEL">Channel</option>
            <option value="VIDEO">Video</option>
          </select>
          <input v-model="targetForm.label" :class="inputClass" type="text" placeholder="Label target" />
          <input
            v-model="targetForm.target"
            :class="inputClass"
            type="text"
            placeholder="Channel ID / Video ID"
          />
          <input
            v-model="targetForm.filter"
            :class="inputClass"
            type="text"
            placeholder="Filter kata kunci"
          />
        </div>
        <div class="flex flex-wrap items-center justify-between gap-3">
          <label class="flex items-center gap-2 text-sm text-gray-700">
            <input v-model="targetForm.active" type="checkbox" class="h-4 w-4 rounded border-gray-300" />
            Aktif saat dibuat
          </label>
          <button
            type="button"
            class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50"
            :class="!isTargetValid ? 'opacity-50 cursor-not-allowed' : ''"
            :disabled="!isTargetValid"
            @click="addTarget"
          >
            Tambah Target
          </button>
        </div>
      </div>
      <div class="overflow-x-auto">
        <table class="w-full text-sm">
          <thead class="bg-gray-50 text-left">
            <tr>
              <th class="p-3">Type</th>
              <th class="p-3">Target</th>
              <th class="p-3">Filter</th>
              <th class="p-3">Status</th>
              <th class="p-3">Aksi</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="target in monitoringTargets" :key="target.id" class="border-t hover:bg-gray-50">
              <td class="p-3">{{ target.type }}</td>
              <td class="p-3">
                <p class="font-medium text-gray-800">{{ target.label }}</p>
                <p class="text-xs text-gray-500">{{ target.target }}</p>
              </td>
              <td class="p-3">{{ target.filter || "-" }}</td>
              <td class="p-3">
                <span
                  :class="[
                    statusBadgeBase,
                    target.active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-700',
                  ]"
                >
                  {{ target.active ? "Active" : "Paused" }}
                </span>
              </td>
              <td class="p-3">
                <div class="flex flex-wrap items-center gap-2">
                  <button
                    class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50"
                    :class="target.active ? 'text-yellow-700' : 'text-green-700'"
                    type="button"
                    @click="toggleTarget(target.id)"
                  >
                    {{ target.active ? "Pause" : "Activate" }}
                  </button>
                  <button
                    class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50 text-red-600"
                    type="button"
                    @click="removeTarget(target.id)"
                  >
                    Hapus
                  </button>
                </div>
              </td>
            </tr>
            <tr v-if="!monitoringTargets.length" class="border-t">
              <td class="p-3 text-center text-sm text-gray-500" colspan="5">
                Target pemantauan belum ditambahkan.
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="rounded-xl border bg-white">
      <div class="border-b p-3">
        <p class="text-sm font-medium">Threshold & Policy</p>
      </div>
      <div class="p-4 space-y-4">
        <div class="grid gap-3 md:grid-cols-2">
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Threshold Low</label>
            <input
              v-model.number="thresholdLow"
              type="number"
              step="0.01"
              min="0"
              max="1"
              :class="inputClass"
            />
          </div>
          <div class="space-y-2">
            <label class="text-sm font-medium text-gray-700">Threshold High</label>
            <input
              v-model.number="thresholdHigh"
              type="number"
              step="0.01"
              min="0"
              max="1"
              :class="inputClass"
            />
          </div>
        </div>

        <div class="flex items-center gap-2">
          <input
            id="borderlineEnabled"
            v-model="borderlineEnabled"
            type="checkbox"
            class="h-4 w-4 rounded border-gray-300"
          />
          <label for="borderlineEnabled" class="text-sm text-gray-700">
            Aktifkan review borderline
          </label>
        </div>

        <div class="space-y-2">
          <p class="text-sm font-medium text-gray-700">Video yang dipantau</p>
          <div class="grid gap-2 sm:grid-cols-2">
            <label
              v-for="video in videoOptions"
              :key="video"
              class="flex items-center gap-2 text-sm text-gray-700"
            >
              <input v-model="monitoredVideos" type="checkbox" :value="video" class="h-4 w-4 rounded border-gray-300" />
              <span>{{ video }}</span>
            </label>
          </div>
        </div>

        <p v-if="!isValid" class="text-xs text-red-600">
          Threshold low harus lebih kecil dari threshold high.
        </p>

        <div>
          <button
            type="button"
            class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50"
            :class="!isValid ? 'opacity-50 cursor-not-allowed' : ''"
            :disabled="!isValid"
            @click="saveSettings"
          >
            Simpan Preferensi
          </button>
        </div>
      </div>
    </div>

    <div class="rounded-xl border bg-white p-4">
      <p class="text-sm font-medium">Pusat Bantuan</p>
      <div class="mt-3 grid gap-2 text-sm text-gray-600">
        <div class="flex items-center justify-between rounded-lg border bg-gray-50 px-3 py-2">
          <span>Pedoman Moderasi</span>
          <span class="text-xs text-gray-400">Lihat</span>
        </div>
        <div class="flex items-center justify-between rounded-lg border bg-gray-50 px-3 py-2">
          <span>Contoh Komentar Abu-abu</span>
          <span class="text-xs text-gray-400">Lihat</span>
        </div>
        <div class="flex items-center justify-between rounded-lg border bg-gray-50 px-3 py-2">
          <span>Kebijakan Privasi & Keamanan</span>
          <span class="text-xs text-gray-400">Lihat</span>
        </div>
        <div class="flex items-center justify-between rounded-lg border bg-gray-50 px-3 py-2">
          <span>Tips Moderasi Efisien</span>
          <span class="text-xs text-gray-400">Lihat</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, reactive, ref } from "vue"
import { storeToRefs } from "pinia"
import { useModerationStore } from "~/stores/moderation"

const store = useModerationStore()
const { settings, comments, oauthStatus, monitoringTargets, modelMetrics } = storeToRefs(store)

const thresholdLow = ref(settings.value.thresholdLow)
const thresholdHigh = ref(settings.value.thresholdHigh)
const borderlineEnabled = ref(settings.value.borderlineEnabled)
const monitoredVideos = ref([...settings.value.monitoredVideos])
const language = ref(settings.value.language)
const theme = ref(settings.value.theme)
const density = ref(settings.value.density)
const notifyNewComments = ref(settings.value.notifyNewComments)
const autoHoldSuspicious = ref(settings.value.autoHoldSuspicious)

const toastMessage = ref("")
let toastTimer = null

const targetForm = reactive({
  type: "VIDEO",
  label: "",
  target: "",
  filter: "",
  active: true,
})

const inputClass =
  "w-full rounded-lg border px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-sky-200"

const statusBadgeBase = "inline-flex rounded-full px-2 py-1 text-xs font-medium"

const connectionBadgeClass = computed(() =>
  oauthStatus.value.connected ? "bg-green-100 text-green-700" : "bg-red-100 text-red-700"
)

const scopeList = computed(() => oauthStatus.value.scopes.join(", "))

const videoOptions = computed(() => {
  const unique = new Set(comments.value.map((comment) => comment.videoTitle))
  return Array.from(unique)
})

const isValid = computed(() => thresholdLow.value < thresholdHigh.value)

const isTargetValid = computed(
  () => targetForm.label.trim().length > 0 && targetForm.target.trim().length > 0
)

const showToast = (message) => {
  toastMessage.value = message
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => {
    toastMessage.value = ""
  }, 2000)
}

const saveSettings = () => {
  if (!isValid.value) return
  store.updateSettings({
    thresholdLow: thresholdLow.value,
    thresholdHigh: thresholdHigh.value,
    borderlineEnabled: borderlineEnabled.value,
    monitoredVideos: monitoredVideos.value,
    language: language.value,
    theme: theme.value,
    density: density.value,
    notifyNewComments: notifyNewComments.value,
    autoHoldSuspicious: autoHoldSuspicious.value,
  })

  showToast("Tersimpan")
}

const toggleOAuth = () => {
  const nextStatus = !oauthStatus.value.connected
  store.updateOAuthStatus(
    { connected: nextStatus },
    "admin",
    nextStatus ? "OAuth connected" : "OAuth disconnected"
  )
  if (nextStatus) {
    store.refreshSync("system")
  }
  showToast(nextStatus ? "OAuth terhubung" : "OAuth terputus")
}

const refreshSync = () => {
  store.refreshSync("system")
  showToast("Sync diperbarui")
}

const addTarget = () => {
  const success = store.addMonitoringTarget({
    type: targetForm.type,
    label: targetForm.label.trim(),
    target: targetForm.target.trim(),
    filter: targetForm.filter.trim(),
    active: targetForm.active,
  })

  if (!success) return

  targetForm.label = ""
  targetForm.target = ""
  targetForm.filter = ""
  showToast("Target ditambahkan")
}

const toggleTarget = (id) => {
  const success = store.toggleMonitoringTarget(id)
  if (success) showToast("Status target diperbarui")
}

const removeTarget = (id) => {
  const success = store.removeMonitoringTarget(id)
  if (success) showToast("Target dihapus")
}

onBeforeUnmount(() => {
  if (toastTimer) clearTimeout(toastTimer)
})
</script>
