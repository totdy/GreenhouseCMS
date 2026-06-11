<script setup lang="ts">
import RevenueChart from '@/components/RevenueChart.vue';
import ActivityChart from '@/components/ActivityChart.vue';
import ActivityTable from '@/components/ActivityTable.vue';
import RevenueTable from '@/components/RevenueTable.vue';
import ActivityWeekly from '@/components/ActivityWeekly.vue';

import { GetActivityByYear, GetActivityByWeek, GetRevenueByYear } from "@/scripts/api";
import type { YearlyActivityItem, YearlyRevenueItem, WeeklyActivityItem } from "@/scripts/types";
import { DEFAULT_PLANT, PLANT_LIST, type PlantType } from "@/scripts/plants";

import { ref, watch } from 'vue';

import { useI18n } from "vue-i18n";
const { t } = useI18n();

const chartYear = ref(new Date().getFullYear());
const selectedPlant = ref<PlantType>(DEFAULT_PLANT);

const activityData = ref<YearlyActivityItem[]>([]);
const revenueData = ref<YearlyRevenueItem[]>([]);
const weeklyActivityData = ref<WeeklyActivityItem[]>([]);

async function loadActivityData() {
  try {
    const resp = await GetActivityByYear(chartYear.value);
    activityData.value = resp?.data ?? [];
  } catch (err) {
    console.error("Failed to load activity data:", err);
  }
}

async function loadWeeklyActivityData() {
  try {
    const resp = await GetActivityByWeek(chartYear.value);
    weeklyActivityData.value = resp?.data ?? [];
  } catch (err) {
    console.error("Failed to load weekly activity data:", err);
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

watch(chartYear, () => {
  loadActivityData();
  loadWeeklyActivityData();
  loadRevenueData();
}, { immediate: true });
</script>

<template>
  <div>
    <section id="sy">
      <h2>
        <label>🗓️:</label>
        <select v-model="chartYear">
          <option v-for="year in [2025, 2026].sort((a, b) => b - a)" :key="year" :value="year">
            {{ year }}
          </option>
        </select>
      </h2>
    </section>
    <RevenueTable :data="revenueData" :year="chartYear" />
    <RevenueChart :data="revenueData" :year="chartYear" />
    <ActivityTable :data="activityData" />
    <section id="sp">
      <h2>
        <label>🧺:</label>
        <select v-model="selectedPlant">
          <option v-for="plant in PLANT_LIST" :key="plant" :value="plant">
            {{ t(`common.type.${plant}`) }}
          </option>
        </select>
      </h2>
    </section>
    <ActivityChart :data="activityData" :year="chartYear" :plant="selectedPlant" />
    <ActivityWeekly :data="weeklyActivityData" :year="chartYear" :plant="selectedPlant" />
  </div>
</template>

<style lang="css" scoped>
#sy {
  grid-area: sy;
}

#sp {
  grid-area: sp;
}

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
    "sy sy sy"
    "rty rc rc"
    "rtm rc rc"
    "sp  sp at"
    "ac  ac at"
    "ac  ac at"
    "aw  aw at";

  &>* {
    min-width: 0;
    min-height: 0;
  }

  @media (max-width: 750px) {
    grid-template-columns: 1fr 1fr;
    grid-template-areas:
      "sy sy"
      "rc  rc"
      "rty rtm"
      "at  at"
      "sp  sp"
      "ac  ac"
      "aw  aw";
  }
}
</style>