export const apiFetch = (path, options = {}) => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase || "http://localhost:8000"
  return $fetch(path, { baseURL, ...options })
}
