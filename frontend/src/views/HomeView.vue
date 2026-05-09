<script setup lang="ts">
import RevenueChart from '@/components/RevenueChart.vue';
import ActivityChart from '@/components/ActivityChart.vue';
import ActivityTable from '@/components/ActivityTable.vue';
import RevenueTable from '@/components/RevenueTable.vue';

import { GetActivityByYear, GetRevenueByDate } from "@/scripts/api";
import type { ActivitySeries, RevenueByDateItem } from "@/scripts/types";

import { ref, watch } from 'vue';

const chartYear = ref(new Date().getFullYear());

const activityData = ref<ActivitySeries[]>([]);
const revenueData = ref<RevenueByDateItem[]>([]);

async function loadActivityData() {
  try {
    const resp = await GetActivityByYear(chartYear.value);
    activityData.value = resp?.data ?? [];
  } catch (err) {
    console.error("Failed to load activity data:", err);
  }
}

async function loadRevenueData() {
    try {
        const resp = await GetRevenueByDate(chartYear.value);
        revenueData.value = resp?.data ?? [];
    } catch (err) {
        console.error("Failed to load revenue data:", err);
    }
}

watch(chartYear, ()=>{ loadActivityData(), loadRevenueData() }, { immediate: true });
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
  <div>
    <RevenueTable :data="revenueData" />
    <RevenueChart :data="revenueData" />    
  </div>
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

  &:nth-child(even){
    grid-template-columns: 1fr 2fr;
  }

  @media (max-width: 750px) {
    grid-template-columns: 1fr !important;
  }
}
</style>