<script setup lang="ts">
import { ref, onMounted } from "vue"
import { GetRecentActivity } from "@/scripts/api"
import type { RecentActivityItem } from "@/scripts/types"

import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const recentActivity = ref<RecentActivityItem[]>([])
const loadingRecent = ref(true)

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("default", { day: "numeric", month: "short", year: "numeric" })
}

async function loadRecent() {
  loadingRecent.value = true
  try {
    const res = await GetRecentActivity(10)
    recentActivity.value = res.data
  } finally {
    loadingRecent.value = false
  }
}

onMounted(() => {
  loadRecent()
})

</script>

<template>
  <section>
    <h2>{{ t("home.recentActivity.title") }}</h2>

    <ul v-if="!loadingRecent && recentActivity.length">
      <li v-for="item in recentActivity" :key="item.id">
        <p>{{ t(`addHarvest.type.${item.plant_type.toLowerCase()}`) }}</p>
        <p>{{ item.count }} {{t(`addHarvest.unit.${item.count_unit.toLowerCase()}`) }}</p>
        <p>€{{ item.unit_price.toFixed(2) }}/unit</p>
        <p>{{ formatDate(item.date) }}</p>
      </li>
    </ul>

    <p class="empty" v-else>{{ t("home.recentActivity.empty") }}</p>
  </section>
</template>

<style lang="css" scoped>
li {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto;
  gap: 1rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--bg2, #232b23);
}

li:last-child {
  border-bottom: none;
}

.empty {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: var(--tc);
  text-align: center;
  padding: 2rem 0;
}
</style>