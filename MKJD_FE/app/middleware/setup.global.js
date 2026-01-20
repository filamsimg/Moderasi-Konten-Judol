import { useModerationStore } from "~/stores/moderation"

export default defineNuxtRouteMiddleware((to) => {
  const store = useModerationStore()
  if (store.setupState.completed) return
  if (to.path === "/setup") return
  return navigateTo("/setup")
})
