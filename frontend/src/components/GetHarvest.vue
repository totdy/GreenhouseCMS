<script setup lang="ts">
import { onMounted } from "vue"

import { useHarvest } from "@/scripts/useHarvest"

import { useI18n } from 'vue-i18n'
const { t } = useI18n()

function formatDate(iso: string) {
  return new Date(iso).toLocaleDateString("default", { day: "numeric", month: "short", year: "numeric" })
}

const { harvests, loadingHarvests, currentPage, totalPages, loadPage, nextPage, prevPage } = useHarvest()

onMounted(() => loadPage(1))
</script>

<template>
  <section>
    <h2>{{ t("getHarvest.title") }}</h2>

    <ul v-show="harvests.length" :style="{ opacity: loadingHarvests ? 0.4 : 1 }">
      <li v-for="item in harvests" :key="item.id">
        <p>{{ t(`addHarvest.type.${item.plant_type.toLowerCase()}`) }}</p>
        <p>{{ item.count }} {{ t(`addHarvest.unit.${item.count_unit.toLowerCase()}`) }}</p>
        <p>€{{ item.unit_price.toFixed(2) }}/{{ t("addHarvest.unit.title") }}</p>
        <p>{{ formatDate(item.date) }}</p>
      </li>
    </ul>

    <h2 v-if="!loadingHarvests && !harvests.length">{{ t("getHarvest.empty") }}</h2>

    <div class="pagination" v-if="totalPages > 1">
      <button type="button" :disabled="currentPage === 1" @click="prevPage">‹</button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button type="button" :disabled="currentPage === totalPages" @click="nextPage">›</button>
    </div>
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

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding-top: 1rem;
}

.pagination button {
  padding: 0.25rem 0.75rem;
  font-size: 1.1rem;
  cursor: pointer;
}

.pagination button:disabled {
  opacity: 0.35;
  cursor: default;
}
</style>