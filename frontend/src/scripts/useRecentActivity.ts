import { ref } from "vue"
import { GetRecentActivity } from "@/scripts/api"
import type { RecentActivityItem } from "@/scripts/types"

const recentActivity = ref<RecentActivityItem[]>([])
const loadingRecent = ref(false)

export function useRecentActivity() {
  async function loadRecent() {
    loadingRecent.value = true
    try {
      const res = await GetRecentActivity(10)
      recentActivity.value = res.data
    } finally {
      loadingRecent.value = false
    }
  }

  return { recentActivity, loadingRecent, loadRecent }
}