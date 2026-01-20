<template>
  <div class="w-full max-w-2xl space-y-6">
    <div class="text-center">
      <div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-2xl bg-white shadow-sm">
        <div class="h-6 w-6 rounded-lg bg-sky-500"></div>
      </div>
      <h1 class="text-2xl font-semibold text-gray-900">Setup Moderasi Komentar</h1>
      <p class="text-sm text-gray-500">
        Ikuti langkah singkat untuk menghubungkan akun dan memilih kanal yang akan dimoderasi.
      </p>
    </div>

    <div class="rounded-2xl border bg-white p-6 shadow-sm animate-float-in">
      <div v-if="currentStep === 1" class="space-y-6">
        <div class="text-center">
          <div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-sky-100 text-sky-600">
            <svg
              class="h-6 w-6"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M15 10l4.5 2.6v4.8L15 20" />
              <path d="M9 10l-4.5 2.6v4.8L9 20" />
              <path d="M12 12v8" />
              <path d="M7 6h10" />
            </svg>
          </div>
          <p class="text-base font-semibold text-gray-900">Selamat Datang di Moderasi YouTube</p>
          <p class="text-sm text-gray-500">
            Kelola komentar kanal YouTube Anda dengan lebih efisien dan aman.
          </p>
        </div>

        <div class="grid gap-3 md:grid-cols-3">
          <div class="rounded-xl border bg-gray-50 p-3 text-center">
            <p class="text-sm font-semibold text-gray-800">Moderasi Otomatis</p>
            <p class="text-xs text-gray-500">Tinjau komentar dengan cepat.</p>
          </div>
          <div class="rounded-xl border bg-gray-50 p-3 text-center">
            <p class="text-sm font-semibold text-gray-800">Keputusan Cepat</p>
            <p class="text-xs text-gray-500">Tahan, tolak, atau terbitkan.</p>
          </div>
          <div class="rounded-xl border bg-gray-50 p-3 text-center">
            <p class="text-sm font-semibold text-gray-800">Riwayat Lengkap</p>
            <p class="text-xs text-gray-500">Lacak semua tindakan moderasi.</p>
          </div>
        </div>

        <div class="rounded-lg border bg-gray-50 p-3 text-xs text-gray-600">
          Anda akan diminta memberikan izin moderasi komentar. Data Anda aman dan tidak dibagikan.
        </div>

        <button
          type="button"
          class="w-full rounded-lg border px-3 py-2 text-sm bg-sky-600 text-white border-sky-600 hover:bg-sky-700"
          @click="handleLogin"
        >
          {{ oauthStatus.connected ? "Lanjutkan" : "Masuk dengan Google" }}
        </button>
      </div>

      <div v-else-if="currentStep === 2" class="space-y-6">
        <div class="text-center">
          <div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
            <svg
              class="h-6 w-6"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M20 6L9 17l-5-5" />
            </svg>
          </div>
          <p class="text-base font-semibold text-gray-900">Pilih Kanal YouTube</p>
          <p class="text-sm text-gray-500">Pilih kanal yang ingin Anda kelola komentarnya.</p>
        </div>

        <div class="space-y-3">
          <button
            v-for="option in channelOptions"
            :key="option.id"
            type="button"
            class="w-full rounded-xl border p-3 text-left transition hover:border-sky-300 hover:bg-sky-50"
            :class="selectedChannelId === option.channelId ? 'border-sky-400 bg-sky-50' : ''"
            @click="selectChannel(option.id)"
          >
            <div class="flex items-center gap-3">
              <div class="h-10 w-10 rounded-full bg-gradient-to-br from-sky-400 to-cyan-400"></div>
              <div class="flex-1">
                <p class="text-sm font-semibold text-gray-900">{{ option.name }}</p>
                <p class="text-xs text-gray-500">
                  {{ option.handle }} - {{ option.subscribers }} subscriber
                </p>
              </div>
              <svg
                class="h-4 w-4 text-gray-400"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="1.8"
                stroke-linecap="round"
                stroke-linejoin="round"
              >
                <path d="M9 18l6-6-6-6" />
              </svg>
            </div>
            <p class="mt-2 text-xs text-gray-500">{{ option.url }}</p>
          </button>
        </div>

        <div class="flex items-center justify-between gap-3">
          <button
            type="button"
            class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50"
            @click="prevStep"
          >
            Kembali
          </button>
          <button
            type="button"
            class="rounded-lg border px-3 py-2 text-sm bg-sky-600 text-white border-sky-600 hover:bg-sky-700"
            :class="!hasChannel ? 'opacity-50 cursor-not-allowed' : ''"
            :disabled="!hasChannel"
            @click="nextStep"
          >
            Lanjut
          </button>
        </div>
      </div>

      <div v-else class="space-y-6">
        <div class="text-center">
          <div class="mx-auto mb-3 flex h-12 w-12 items-center justify-center rounded-full bg-purple-100 text-purple-600">
            <svg
              class="h-6 w-6"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.8"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M12 3l7 4v5c0 4.5-3 8-7 9-4-1-7-4.5-7-9V7z" />
              <path d="M9 12l2 2 4-4" />
            </svg>
          </div>
          <p class="text-base font-semibold text-gray-900">Berikan Izin Moderasi</p>
          <p class="text-sm text-gray-500">Izin diperlukan untuk membaca dan mengelola komentar.</p>
        </div>

        <div class="rounded-xl border bg-gray-50 p-4 text-sm text-gray-700 space-y-2">
          <p class="text-sm font-semibold text-gray-800">Izin yang dibutuhkan:</p>
          <div class="flex items-center gap-2">
            <span class="h-4 w-4 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center">
              <svg class="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 6L9 17l-5-5" />
              </svg>
            </span>
            <span>Membaca komentar dari video Anda</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="h-4 w-4 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center">
              <svg class="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 6L9 17l-5-5" />
              </svg>
            </span>
            <span>Menahan atau menolak komentar</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="h-4 w-4 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center">
              <svg class="h-3 w-3" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M20 6L9 17l-5-5" />
              </svg>
            </span>
            <span>Menerbitkan komentar yang ditahan</span>
          </div>
        </div>

        <div class="rounded-lg border bg-gray-50 p-3 text-xs text-gray-600">
          Anda dapat mencabut izin kapan saja di halaman Preferensi.
        </div>

        <div class="flex items-center justify-between gap-3">
          <button
            type="button"
            class="rounded-lg border px-3 py-2 text-sm hover:bg-gray-50"
            @click="prevStep"
          >
            Kembali
          </button>
          <button
            type="button"
            class="rounded-lg border px-3 py-2 text-sm bg-sky-600 text-white border-sky-600 hover:bg-sky-700"
            @click="grantAccess"
          >
            Berikan Izin
          </button>
        </div>
      </div>
    </div>

    <div class="flex items-center justify-center gap-2">
      <span
        v-for="step in steps"
        :key="step"
        class="h-2 w-2 rounded-full"
        :class="currentStep === step ? 'bg-sky-500' : 'bg-gray-200'"
      ></span>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { storeToRefs } from "pinia"
import { useModerationStore } from "~/stores/moderation"

definePageMeta({ layout: "setup" })

const store = useModerationStore()
const { setupState, oauthStatus, channelOptions } = storeToRefs(store)

const steps = [1, 2, 3]
const currentStep = computed(() => setupState.value.step)

const selectedChannelId = computed(() => oauthStatus.value.channelId)
const hasChannel = computed(() => Boolean(oauthStatus.value.channelId))

const handleLogin = () => {
  if (!oauthStatus.value.connected) {
    store.updateOAuthStatus({ connected: true }, "admin", "OAuth connected via setup")
    store.refreshSync("system")
  }
  store.nextSetupStep()
}

const selectChannel = (optionId) => {
  store.selectChannel(optionId)
}

const nextStep = () => {
  if (!hasChannel.value) return
  store.nextSetupStep()
}

const prevStep = () => {
  store.prevSetupStep()
}

const grantAccess = () => {
  store.grantPermissions("admin")
  store.completeSetup("admin")
  navigateTo("/")
}
</script>
