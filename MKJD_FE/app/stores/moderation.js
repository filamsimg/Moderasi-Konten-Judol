import { defineStore } from "pinia"
import { ref } from "vue"
import {
  seedAuditLogs,
  seedComments,
  seedSettings,
  seedOAuthStatus,
  seedChannelOptions,
  seedMonitoringTargets,
  seedModelMetrics,
  seedPipelineStatus,
  seedSetupState,
} from "~/lib/mockData"

export const useModerationStore = defineStore("moderation", () => {
  const comments = ref(structuredClone(seedComments))
  const auditLogs = ref(structuredClone(seedAuditLogs))
  const settings = ref(structuredClone(seedSettings))
  const oauthStatus = ref(structuredClone(seedOAuthStatus))
  const channelOptions = ref(structuredClone(seedChannelOptions))
  const monitoringTargets = ref(structuredClone(seedMonitoringTargets))
  const modelMetrics = ref(structuredClone(seedModelMetrics))
  const pipelineStatus = ref(structuredClone(seedPipelineStatus))
  const setupState = ref(structuredClone(seedSetupState))

  const pad2 = (n) => String(n).padStart(2, "0")

  const formatDate = (date) => {
    const yyyy = date.getFullYear()
    const mm = pad2(date.getMonth() + 1)
    const dd = pad2(date.getDate())
    const hh = pad2(date.getHours())
    const min = pad2(date.getMinutes())
    return `${yyyy}-${mm}-${dd} ${hh}:${min}`
  }

  const formatNow = () => formatDate(new Date())

  const toYTStatus = (decision) => {
    if (decision === "PUBLISHED") return "published"
    if (decision === "REJECTED") return "rejected"
    return "heldForReview"
  }

  const pushAuditLog = ({
    action = "SETTINGS_UPDATE",
    commentId = null,
    score = null,
    fromDecision = null,
    toDecision = null,
    actor = "admin",
    result = "OK",
    note = "",
  }) => {
    auditLogs.value.unshift({
      id: `log_${Math.random().toString(16).slice(2)}`,
      at: formatNow(),
      action,
      commentId,
      score,
      fromDecision,
      toDecision,
      actor,
      result,
      note,
    })
  }

  const getCommentById = (id) => comments.value.find((comment) => comment.id === id)

  const getAuditByCommentId = (id) =>
    auditLogs.value.filter((log) => log.commentId === id)

  const updateDecision = (commentId, toDecision, actor = "admin") => {
    const comment = getCommentById(commentId)
    if (!comment) return false

    const fromDecision = comment.decision
    comment.decision = toDecision
    comment.ytStatus = toYTStatus(toDecision)

    pushAuditLog({
      action: "DECISION_UPDATE",
      commentId,
      score: comment.score,
      fromDecision,
      toDecision,
      actor,
      note: `Decision updated to ${toDecision}`,
    })

    return true
  }

  const updateSettings = (patch, actor = "admin") => {
    Object.assign(settings.value, patch)

    pushAuditLog({
      action: "SETTINGS_UPDATE",
      actor,
      note: "Settings updated",
    })
  }

  const updateOAuthStatus = (patch, actor = "admin", note = "OAuth status updated") => {
    Object.assign(oauthStatus.value, patch)
    if (Object.prototype.hasOwnProperty.call(patch, "connected")) {
      pipelineStatus.value.status = patch.connected ? "RUNNING" : "PAUSED"
      if (!patch.connected) {
        pipelineStatus.value.lastFetch = "-"
      }
    }
    if (Object.prototype.hasOwnProperty.call(patch, "scopes")) {
      oauthStatus.value.permissionGranted = patch.scopes.length > 0
    }

    pushAuditLog({
      action: "SETTINGS_UPDATE",
      actor,
      note,
    })
  }

  const refreshSync = (actor = "system") => {
    const now = formatNow()
    oauthStatus.value.lastSync = now
    pipelineStatus.value.lastFetch = now

    pushAuditLog({
      action: "SETTINGS_UPDATE",
      actor,
      note: "Sync refreshed",
    })
  }

  const addMonitoringTarget = (target, actor = "admin") => {
    if (!target || !target.type || !target.label || !target.target) return false

    const newTarget = {
      id: target.id || `target_${Math.random().toString(16).slice(2)}`,
      type: target.type,
      label: target.label,
      target: target.target,
      filter: target.filter || "",
      active: target.active !== false,
    }

    monitoringTargets.value.unshift(newTarget)

    pushAuditLog({
      action: "SETTINGS_UPDATE",
      actor,
      note: `Target added: ${newTarget.label}`,
    })

    return true
  }

  const toggleMonitoringTarget = (id, actor = "admin") => {
    const target = monitoringTargets.value.find((item) => item.id === id)
    if (!target) return false

    target.active = !target.active

    pushAuditLog({
      action: "SETTINGS_UPDATE",
      actor,
      note: `Target ${target.active ? "activated" : "paused"}: ${target.label}`,
    })

    return true
  }

  const removeMonitoringTarget = (id, actor = "admin") => {
    const index = monitoringTargets.value.findIndex((item) => item.id === id)
    if (index === -1) return false

    const removed = monitoringTargets.value.splice(index, 1)[0]

    pushAuditLog({
      action: "SETTINGS_UPDATE",
      actor,
      note: `Target removed: ${removed.label}`,
    })

    return true
  }

  const updateModelMetrics = (patch, actor = "admin") => {
    Object.assign(modelMetrics.value, patch)

    pushAuditLog({
      action: "SETTINGS_UPDATE",
      actor,
      note: "Model metrics updated",
    })
  }

  const selectChannel = (optionId, actor = "admin") => {
    const option = channelOptions.value.find((item) => item.id === optionId)
    if (!option) return false

    oauthStatus.value.channelName = option.name
    oauthStatus.value.channelId = option.channelId
    oauthStatus.value.channelHandle = option.handle
    oauthStatus.value.channelUrl = option.url

    const channelTarget = monitoringTargets.value.find((item) => item.type === "CHANNEL")
    if (channelTarget) {
      channelTarget.label = option.name
      channelTarget.target = option.channelId
      channelTarget.active = true
    } else {
      monitoringTargets.value.unshift({
        id: `target_${Math.random().toString(16).slice(2)}`,
        type: "CHANNEL",
        label: option.name,
        target: option.channelId,
        filter: "",
        active: true,
      })
    }

    pushAuditLog({
      action: "SETTINGS_UPDATE",
      actor,
      note: `Channel selected: ${option.name}`,
    })

    return true
  }

  const grantPermissions = (actor = "admin") => {
    const now = new Date()
    const expiry = new Date(now.getTime() + 1000 * 60 * 60 * 24 * 30)

    oauthStatus.value.connected = true
    oauthStatus.value.permissionGranted = true
    oauthStatus.value.scopes = [
      "youtube.readonly",
      "youtube.force-ssl",
      "youtube.manage-comments",
    ]
    oauthStatus.value.lastSync = formatDate(now)
    oauthStatus.value.tokenExpiry = formatDate(expiry)

    pipelineStatus.value.status = "RUNNING"
    pipelineStatus.value.lastFetch = formatDate(now)

    pushAuditLog({
      action: "SETTINGS_UPDATE",
      actor,
      note: "Permissions granted",
    })
  }

  const setSetupStep = (step) => {
    if (typeof step !== "number") return
    setupState.value.step = Math.min(Math.max(step, 1), 3)
  }

  const nextSetupStep = () => {
    setSetupStep(setupState.value.step + 1)
  }

  const prevSetupStep = () => {
    setSetupStep(setupState.value.step - 1)
  }

  const completeSetup = (actor = "admin") => {
    setupState.value.completed = true
    setupState.value.step = 3

    pushAuditLog({
      action: "SETTINGS_UPDATE",
      actor,
      note: "Setup completed",
    })
  }

  const resetSetup = (actor = "admin") => {
    setupState.value.completed = false
    setupState.value.step = 1

    pushAuditLog({
      action: "SETTINGS_UPDATE",
      actor,
      note: "Setup reset",
    })
  }

  return {
    comments,
    auditLogs,
    settings,
    oauthStatus,
    channelOptions,
    monitoringTargets,
    modelMetrics,
    pipelineStatus,
    setupState,
    pad2,
    formatDate,
    formatNow,
    toYTStatus,
    updateDecision,
    updateSettings,
    updateOAuthStatus,
    refreshSync,
    addMonitoringTarget,
    toggleMonitoringTarget,
    removeMonitoringTarget,
    updateModelMetrics,
    selectChannel,
    grantPermissions,
    setSetupStep,
    nextSetupStep,
    prevSetupStep,
    completeSetup,
    resetSetup,
    getCommentById,
    getAuditByCommentId,
  }
})
