<script setup lang="ts">
import RevenueChart from '@/components/RevenueChart.vue';
import ActivityChart from '@/components/ActivityChart.vue';
import ActivityTable from '@/components/ActivityTable.vue';

import { GetActivityByYear } from "@/scripts/api";
import type { ActivitySeries } from "@/scripts/types";

import { ref, watch } from 'vue';

const chartYear = ref(new Date().getFullYear());

const activityData = ref<ActivitySeries[]>([])

async function loadActivityData() {
  try {
    const resp = await GetActivityByYear(chartYear.value);
    activityData.value = resp?.data ?? [];
  } catch (err) {
    console.error("Failed to load activity data:", err);
  }
}

watch(chartYear, loadActivityData, { immediate: true });
</script>

<template>
  <section class="controls">
    <h2>
      <label>🗓️:</label>
      <select v-model="chartYear">
        <option v-for="year in [2025, 2026].sort((a, b) => b - a)" :key="year" :value="year">
          {{ year }}
        </option>
      </select>
    </h2>
  </section>

  <RevenueChart :year="chartYear" />
  <div>
    <ActivityChart :data="activityData" />
    <ActivityTable :data="activityData" />
  </div>
</template>

<style lang="css" scoped>
.controls h2 {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
}

div {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1rem;

  @media (max-width: 750px) {
    grid-template-columns: 1fr;
  }
}
</style>