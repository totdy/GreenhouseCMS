<script setup lang="ts">
import { onMounted } from "vue"

import { useRecentActivity } from "@/scripts/useRecentActivity"

import { useI18n } from 'vue-i18n'
const { t } = useI18n()

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("default", { day: "numeric", month: "short", year: "numeric" })
}

const { recentActivity, loadingRecent, loadRecent } = useRecentActivity()

onMounted(() => loadRecent())

</script>

<template>
  <section>
    <h2>{{ t("recentActivity.title") }}</h2>

    <ul v-if="!loadingRecent && recentActivity.length">
      <li v-for="item in recentActivity" :key="item.id">
        <p>{{ t(`addHarvest.type.${item.plant_type.toLowerCase()}`) }}</p>
        <p>{{ item.count }} {{ t(`addHarvest.unit.${item.count_unit.toLowerCase()}`) }}</p>
        <p>€{{ item.unit_price.toFixed(2) }}/{{ t("addHarvest.unit.title") }}</p>
        <p>{{ formatDate(item.date) }}</p>
      </li>
    </ul>

    <h2 v-else>{{ t("recentActivity.empty") }}</h2>
  </section>
</template>

<style lang="css" scoped>
li {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr auto;
  gap: 1rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-muted);
}

li:last-child {
  border-bottom: none;
}
</style>