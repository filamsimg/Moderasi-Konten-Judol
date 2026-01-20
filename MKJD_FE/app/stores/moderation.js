import { defineStore } from "pinia"
import { ref } from "vue"
import { apiFetch } from "~/lib/api"
import {
  formatDateTime,
  mapAuditLog,
  mapChannelOption,
  mapComment,
  mapModelMetrics,
  mapMonitoringTarget,
  mapOAuthStatus,
  mapPipelineStatus,
  mapSettings,
  oauthToApi,
  pipelineToApi,
  settingsToApi,
} from "~/lib/mappers"
import {
  seedAuditLogs,
  seedComments,
  seedModelMetrics,
  seedMonitoringTargets,
  seedOAuthStatus,
  seedPipelineStatus,
  seedSettings,
  seedSetupState,
} from "~/lib/mockData"

export const useModerationStore = defineStore("moderation", () => {
  const comments = ref(structuredClone(seedComments))
  const auditLogs = ref(structuredClone(seedAuditLogs))
  const settings = ref(structuredClone(seedSettings))
  const oauthStatus = ref(structuredClone(seedOAuthStatus))
  const channelOptions = ref([])
  const monitoringTargets = ref(structuredClone(seedMonitoringTargets))
  const modelMetrics = ref(structuredClone(seedModelMetrics))
  const pipelineStatus = ref(structuredClone(seedPipelineStatus))
  const setupState = ref(structuredClone(seedSetupState))

  const isLoading = ref(false)
  const hasLoaded = ref(false)

  const formatNow = () => formatDateTime(new Date().toISOString())

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

  const getAuditByCommentId = (id) => auditLogs.value.filter((log) => log.commentId === id)

  const upsertComment = (comment) => {
    const index = comments.value.findIndex((item) => item.id === comment.id)
    if (index === -1) {
      comments.value.unshift(comment)
      return
    }
    comments.value[index] = comment
  }

  const fetchComments = async () => {
    try {
      const data = await apiFetch("/v1/comments")
      comments.value = (data.items || []).map(mapComment)
      return true
    } catch (error) {
      console.error("Failed to fetch comments", error)
      return false
    }
  }

  const fetchAuditLogs = async () => {
    try {
      const data = await apiFetch("/v1/audit-logs")
      auditLogs.value = (data.items || []).map(mapAuditLog)
      return true
    } catch (error) {
      console.error("Failed to fetch audit logs", error)
      return false
    }
  }

  const fetchSettings = async () => {
    try {
      const data = await apiFetch("/v1/settings")
      settings.value = mapSettings(data)
      return true
    } catch (error) {
      console.error("Failed to fetch settings", error)
      return false
    }
  }

  const fetchOAuthStatus = async () => {
    try {
      const data = await apiFetch("/v1/oauth/status")
      oauthStatus.value = mapOAuthStatus(data)
      return true
    } catch (error) {
      console.error("Failed to fetch oauth status", error)
      return false
    }
  }

  const fetchChannelOptions = async () => {
    try {
      const data = await apiFetch("/v1/oauth/youtube/channels")
      channelOptions.value = (data.items || []).map(mapChannelOption)
      return true
    } catch (error) {
      console.error("Failed to fetch channels", error)
      return false
    }
  }

  const fetchMonitoringTargets = async () => {
    try {
      const data = await apiFetch("/v1/targets")
      monitoringTargets.value = (data.items || []).map(mapMonitoringTarget)
      return true
    } catch (error) {
      console.error("Failed to fetch monitoring targets", error)
      return false
    }
  }

  const fetchModelMetrics = async () => {
    try {
      const data = await apiFetch("/v1/models")
      const items = data.items || []
      const active = items.find((item) => item.is_active) || items[0]
      if (active) {
        modelMetrics.value = mapModelMetrics(active)
      }
      return true
    } catch (error) {
      console.error("Failed to fetch model metrics", error)
      return false
    }
  }

  const fetchPipelineStatus = async () => {
    try {
      const data = await apiFetch("/v1/pipeline/status")
      pipelineStatus.value = mapPipelineStatus(data)
      return true
    } catch (error) {
      console.error("Failed to fetch pipeline status", error)
      return false
    }
  }

  const fetchAll = async (force = false) => {
    if (isLoading.value) return
    if (hasLoaded.value && !force) return
    isLoading.value = true
    await Promise.all([
      fetchComments(),
      fetchAuditLogs(),
      fetchSettings(),
      fetchOAuthStatus(),
      fetchMonitoringTargets(),
      fetchModelMetrics(),
      fetchPipelineStatus(),
    ])
    if (oauthStatus.value.connected) {
      await fetchChannelOptions()
    }
    isLoading.value = false
    hasLoaded.value = true
  }

  const updateDecision = async (commentId, toDecision, actor = "admin") => {
    const comment = getCommentById(commentId)
    if (!comment) return false
    try {
      const updated = await apiFetch(`/v1/comments/${commentId}/decision`, {
        method: "POST",
        body: {
          decision: toDecision,
          actor,
          note: `Decision updated to ${toDecision}`,
        },
      })
      upsertComment(mapComment(updated))
      await fetchAuditLogs()
      return true
    } catch (error) {
      console.error("Failed to update decision", error)
      const fromDecision = comment.decision
      comment.decision = toDecision
      if (toDecision === "PUBLISHED") {
        comment.ytStatus = "published"
      } else if (toDecision === "REJECTED") {
        comment.ytStatus = "rejected"
      } else {
        comment.ytStatus = "heldForReview"
      }
      pushAuditLog({
        action: "DECISION_UPDATE",
        commentId,
        score: comment.score,
        fromDecision,
        toDecision,
        actor,
        note: `Decision updated to ${toDecision}`,
      })
      return false
    }
  }

  const updateSettings = async (patch, actor = "admin") => {
    try {
      const updated = await apiFetch("/v1/settings", {
        method: "PATCH",
        body: settingsToApi(patch),
      })
      settings.value = mapSettings(updated)
      await fetchAuditLogs()
      return true
    } catch (error) {
      console.error("Failed to update settings", error)
      Object.assign(settings.value, patch)
      pushAuditLog({
        action: "SETTINGS_UPDATE",
        actor,
        note: "Settings updated",
      })
      return false
    }
  }

  const updateOAuthStatus = async (patch, actor = "admin", note = "OAuth status updated") => {
    try {
      const updated = await apiFetch("/v1/oauth/status", {
        method: "PATCH",
        body: oauthToApi(patch),
      })
      oauthStatus.value = mapOAuthStatus(updated)
      if (Object.prototype.hasOwnProperty.call(patch, "connected")) {
        pipelineStatus.value.status = patch.connected ? "RUNNING" : "PAUSED"
        if (!patch.connected) {
          pipelineStatus.value.lastFetch = "-"
        }
      }
      await fetchAuditLogs()
      return true
    } catch (error) {
      console.error("Failed to update oauth status", error)
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
      return false
    }
  }

  const updatePipelineStatus = async (patch) => {
    try {
      const updated = await apiFetch("/v1/pipeline/status", {
        method: "PATCH",
        body: pipelineToApi(patch),
      })
      pipelineStatus.value = mapPipelineStatus(updated)
      return true
    } catch (error) {
      console.error("Failed to update pipeline status", error)
      Object.assign(pipelineStatus.value, patch)
      return false
    }
  }

  const refreshSync = async (actor = "system") => {
    const nowIso = new Date().toISOString()
    await updateOAuthStatus({ lastSync: nowIso }, actor, "Sync refreshed")
    await updatePipelineStatus({ lastFetch: nowIso })
  }

  const addMonitoringTarget = async (target, actor = "admin") => {
    if (!target || !target.type || !target.label || !target.target) return false
    try {
      const created = await apiFetch("/v1/targets", {
        method: "POST",
        body: target,
      })
      monitoringTargets.value.unshift(mapMonitoringTarget(created))
      await fetchAuditLogs()
      return true
    } catch (error) {
      console.error("Failed to add monitoring target", error)
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
      return false
    }
  }

  const toggleMonitoringTarget = async (id, actor = "admin") => {
    const target = monitoringTargets.value.find((item) => item.id === id)
    if (!target) return false

    try {
      const updated = await apiFetch(`/v1/targets/${id}`, {
        method: "PATCH",
        body: { active: !target.active },
      })
      Object.assign(target, mapMonitoringTarget(updated))
      await fetchAuditLogs()
      return true
    } catch (error) {
      console.error("Failed to toggle monitoring target", error)
      target.active = !target.active
      pushAuditLog({
        action: "SETTINGS_UPDATE",
        actor,
        note: `Target ${target.active ? "activated" : "paused"}: ${target.label}`,
      })
      return false
    }
  }

  const removeMonitoringTarget = async (id, actor = "admin") => {
    const index = monitoringTargets.value.findIndex((item) => item.id === id)
    if (index === -1) return false

    try {
      await apiFetch(`/v1/targets/${id}`, { method: "DELETE" })
      monitoringTargets.value.splice(index, 1)
      await fetchAuditLogs()
      return true
    } catch (error) {
      console.error("Failed to remove monitoring target", error)
      const removed = monitoringTargets.value.splice(index, 1)[0]
      pushAuditLog({
        action: "SETTINGS_UPDATE",
        actor,
        note: `Target removed: ${removed.label}`,
      })
      return false
    }
  }

  const updateModelMetrics = (patch, actor = "admin") => {
    Object.assign(modelMetrics.value, patch)

    pushAuditLog({
      action: "SETTINGS_UPDATE",
      actor,
      note: "Model metrics updated",
    })
  }

  const selectChannel = async (optionId, actor = "admin") => {
    const option = channelOptions.value.find((item) => item.id === optionId)
    if (!option) return false

    await updateOAuthStatus(
      {
        channelName: option.name,
        channelId: option.channelId,
        channelHandle: option.handle,
        channelUrl: option.url,
      },
      actor,
      `Channel selected: ${option.name}`
    )

    const channelTarget = monitoringTargets.value.find((item) => item.type === "CHANNEL")
    if (channelTarget) {
      try {
        const updated = await apiFetch(`/v1/targets/${channelTarget.id}`, {
          method: "PATCH",
          body: {
            label: option.name,
            target: option.channelId,
            active: true,
          },
        })
        Object.assign(channelTarget, mapMonitoringTarget(updated))
      } catch (error) {
        console.error("Failed to update channel target", error)
        channelTarget.label = option.name
        channelTarget.target = option.channelId
        channelTarget.active = true
      }
    } else {
      await addMonitoringTarget({
        type: "CHANNEL",
        label: option.name,
        target: option.channelId,
        filter: "",
        active: true,
      })
    }

    return true
  }

  const grantPermissions = async (actor = "admin") => {
    const nowIso = new Date().toISOString()

    await updateOAuthStatus(
      {
        connected: true,
        permissionGranted: true,
        lastSync: nowIso,
      },
      actor,
      "Permissions confirmed"
    )

    await updatePipelineStatus({ status: "RUNNING", lastFetch: nowIso })
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
    isLoading,
    hasLoaded,
    fetchAll,
    fetchOAuthStatus,
    fetchChannelOptions,
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
