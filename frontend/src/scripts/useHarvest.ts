import { ref } from "vue"
import { GetHarvestsAll } from "@/scripts/api"
import type { HarvestOut } from "@/scripts/types"

const harvests = ref<HarvestOut[]>([])
const loadingHarvests = ref(false)
const currentPage = ref(1)
const totalPages = ref(1)

export function useHarvest() {
  async function loadPage(page: number) {
    loadingHarvests.value = true
    try {
      const res = await GetHarvestsAll(page)
      harvests.value = res.data
      currentPage.value = res.page
      totalPages.value = res.total_pages
    } finally {
      loadingHarvests.value = false
    }
  }

  function nextPage() {
    if (currentPage.value < totalPages.value) loadPage(currentPage.value + 1)
  }

  function prevPage() {
    if (currentPage.value > 1) loadPage(currentPage.value - 1)
  }

  return { harvests, loadingHarvests, currentPage, totalPages, loadPage, nextPage, prevPage }
}