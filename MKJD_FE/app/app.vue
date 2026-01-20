<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup>
import { onMounted } from "vue"
import { useModerationStore } from "~/stores/moderation"

const store = useModerationStore()

onMounted(() => {
  store.fetchAll()
})
</script>
