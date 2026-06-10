<script setup lang="ts">
import RevenueChart from '@/components/RevenueChart.vue';
import ActivityChart from '@/components/ActivityChart.vue';
import ActivityTable from '@/components/ActivityTable.vue';
import RevenueTable from '@/components/RevenueTable.vue';
import ActivityDaily from '@/components/ActivityDaily.vue';

import { GetActivityByYear, GetRevenueByYear } from "@/scripts/api";
import type { MonthlyActivityItem, YearlyActivityItem, YearlyRevenueItem } from "@/scripts/types";

import { ref, watch } from 'vue';

const chartYear = ref(new Date().getFullYear());

const currentMonth = ref(new Date().getMonth());
const currentYear = ref(new Date().getFullYear());

const activityData = ref<YearlyActivityItem[]>([]);
const revenueData = ref<YearlyRevenueItem[]>([]);

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
    const resp = await GetRevenueByYear(chartYear.value);
    revenueData.value = resp?.data ?? [];
  } catch (err) {
    console.error("Failed to load revenue data:", err);
  }
}

const dailyMonth = ref<{ label: string; entries: MonthlyActivityItem[] } | null>(null);
const dailyLoading = ref(false);

function onMonthSelected(payload: { label: string; entries: MonthlyActivityItem[] } | null) {
  dailyMonth.value = payload;
}

watch(chartYear, () => {
  dailyMonth.value = null;
  loadActivityData();
  loadRevenueData();
}, { immediate: true });
</script>

<template>
  <section>
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
    <RevenueTable :data="revenueData" :currentMonth=" chartYear===currentYear ? currentMonth+1 : 12" />
    <RevenueChart :data="revenueData" :year="chartYear" />
    <ActivityChart :data="activityData" :year="chartYear" @month-selected="onMonthSelected" @month-loading="dailyLoading = $event" />
    <ActivityDaily :month-label="dailyMonth?.label ?? null" :entries="dailyMonth?.entries ?? []" :loading="dailyLoading" />
    <ActivityTable :data="activityData" />
  </div>
</template>

<style lang="css" scoped>
h2 {
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 0.5rem;
}

div {
  display: grid;
  gap: 1rem;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-areas:
    "rty rc rc"
    "rtm rc rc"
    "ac  ac at"
    "ac  ac at"
    "ad  ad at";

  &>* {
    min-width: 0;
    min-height: 0;
  }

  @media (max-width: 750px) {
    grid-template-columns: 1fr 1fr;
    grid-template-areas:
      "rc  rc"
      "rty rtm"
      "ac  ac"
      "ad  ad"
      "at  at";
  }
}
</style>