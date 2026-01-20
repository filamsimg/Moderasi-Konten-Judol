const pad2 = (n) => String(n).padStart(2, "0")

const toDate = (value) => {
  if (!value) return null
  if (value instanceof Date) return value
  if (typeof value !== "string") return null
  const normalized = value.replace(" ", "T")
  const date = new Date(normalized)
  if (Number.isNaN(date.getTime())) return null
  return date
}

export const formatDateTime = (value) => {
  const date = toDate(value)
  if (!date) return "-"
  const yyyy = date.getFullYear()
  const mm = pad2(date.getMonth() + 1)
  const dd = pad2(date.getDate())
  const hh = pad2(date.getHours())
  const min = pad2(date.getMinutes())
  return `${yyyy}-${mm}-${dd} ${hh}:${min}`
}

export const formatSubscriberCount = (value) => {
  const num = Number(value)
  if (!Number.isFinite(num)) return "-"
  if (num >= 1000000) {
    const digit = num >= 10000000 ? 0 : 1
    return `${(num / 1000000).toFixed(digit)}M`
  }
  if (num >= 1000) {
    const digit = num >= 100000 ? 0 : 1
    return `${(num / 1000).toFixed(digit)}K`
  }
  return String(num)
}

export const getInitials = (name = "") => {
  const parts = String(name).trim().split(/\s+/).filter(Boolean)
  if (!parts.length) return ""
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return `${parts[0][0]}${parts[1][0]}`.toUpperCase()
}

export const mapComment = (item) => ({
  id: item.id,
  createdAt: formatDateTime(item.published_at || item.fetched_at || new Date().toISOString()),
  videoTitle: item.video_title || "-",
  text: item.text_raw || "",
  author: item.author_name || "",
  authorInitials: getInitials(item.author_name || ""),
  score: typeof item.score === "number" ? item.score : 0,
  decision: item.decision || "PUBLISHED",
  ytStatus: item.yt_status || "published",
})

export const mapAuditLog = (item) => ({
  id: item.id,
  at: formatDateTime(item.at),
  action: item.action,
  commentId: item.comment_id || null,
  score: item.score,
  fromDecision: item.from_decision || null,
  toDecision: item.to_decision || null,
  actor: item.actor,
  result: item.result,
  note: item.note || "",
})

export const mapSettings = (item) => ({
  thresholdLow: item.threshold_low ?? 0.4,
  thresholdHigh: item.threshold_high ?? 0.7,
  borderlineEnabled: item.borderline_enabled ?? true,
  monitoredVideos: item.monitored_videos ?? [],
  language: item.language ?? "id",
  theme: item.theme ?? "light",
  density: item.density ?? "standard",
  notifyNewComments: item.notify_new_comments ?? true,
  autoHoldSuspicious: item.auto_hold_suspicious ?? true,
})

export const mapOAuthStatus = (item) => ({
  connected: Boolean(item.connected),
  permissionGranted: Boolean(item.permission_granted),
  accountEmail: item.account_email || "",
  channelName: item.channel_name || "",
  channelId: item.channel_id || "",
  channelHandle: item.channel_handle || "",
  channelUrl: item.channel_url || "",
  lastSync: formatDateTime(item.last_sync),
  tokenExpiry: formatDateTime(item.token_expiry),
  scopes: Array.isArray(item.scopes) ? item.scopes : [],
})

export const mapChannelOption = (item) => ({
  id: item.id,
  channelId: item.id,
  name: item.name || "",
  handle: item.handle || "",
  subscribers: formatSubscriberCount(item.subscriber_count),
  url: item.url || "",
  thumbnailUrl: item.thumbnail_url || "",
})

export const mapMonitoringTarget = (item) => ({
  id: item.id,
  type: item.type,
  label: item.label,
  target: item.target,
  filter: item.filter || "",
  active: Boolean(item.active),
})

export const mapModelMetrics = (item) => ({
  modelName: item.model_name || "Unknown",
  version: item.version || "-",
  precision: item.precision ?? 0,
  recall: item.recall ?? 0,
  f1: item.f1 ?? 0,
  prAuc: item.pr_auc ?? 0,
  avgLatencyMs: item.avg_latency_ms ?? 0,
  updatedAt: formatDateTime(item.updated_at),
})

export const mapPipelineStatus = (item) => ({
  status: item.status || "PAUSED",
  lastFetch: formatDateTime(item.last_fetch),
  avgLatencySec: item.avg_latency_sec ?? 0,
  queueSize: item.queue_size ?? 0,
  processedLastHour: item.processed_last_hour ?? 0,
  errorRate: item.error_rate ?? 0,
})

export const settingsToApi = (patch) => {
  const payload = {}
  if ("thresholdLow" in patch) payload.threshold_low = patch.thresholdLow
  if ("thresholdHigh" in patch) payload.threshold_high = patch.thresholdHigh
  if ("borderlineEnabled" in patch) payload.borderline_enabled = patch.borderlineEnabled
  if ("monitoredVideos" in patch) payload.monitored_videos = patch.monitoredVideos
  if ("language" in patch) payload.language = patch.language
  if ("theme" in patch) payload.theme = patch.theme
  if ("density" in patch) payload.density = patch.density
  if ("notifyNewComments" in patch) payload.notify_new_comments = patch.notifyNewComments
  if ("autoHoldSuspicious" in patch) payload.auto_hold_suspicious = patch.autoHoldSuspicious
  return payload
}

export const oauthToApi = (patch) => {
  const payload = {}
  if ("connected" in patch) payload.connected = patch.connected
  if ("permissionGranted" in patch) payload.permission_granted = patch.permissionGranted
  if ("accountEmail" in patch) payload.account_email = patch.accountEmail
  if ("channelName" in patch) payload.channel_name = patch.channelName
  if ("channelId" in patch) payload.channel_id = patch.channelId
  if ("channelHandle" in patch) payload.channel_handle = patch.channelHandle
  if ("channelUrl" in patch) payload.channel_url = patch.channelUrl
  if ("lastSync" in patch) payload.last_sync = patch.lastSync
  if ("tokenExpiry" in patch) payload.token_expiry = patch.tokenExpiry
  if ("scopes" in patch) payload.scopes = patch.scopes
  return payload
}

export const pipelineToApi = (patch) => {
  const payload = {}
  if ("status" in patch) payload.status = patch.status
  if ("lastFetch" in patch) payload.last_fetch = patch.lastFetch
  if ("avgLatencySec" in patch) payload.avg_latency_sec = patch.avgLatencySec
  if ("queueSize" in patch) payload.queue_size = patch.queueSize
  if ("processedLastHour" in patch) payload.processed_last_hour = patch.processedLastHour
  if ("errorRate" in patch) payload.error_rate = patch.errorRate
  return payload
}
