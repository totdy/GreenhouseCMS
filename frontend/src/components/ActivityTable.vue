<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { GetActivityByYear } from "@/scripts/api";
import type { ActivitySeries } from "@/scripts/types";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const chartYear = ref(new Date().getFullYear());

const tableData = ref<ActivitySeries[]>([]);

async function loadChartData() {
    try {
        const resp = await GetActivityByYear(chartYear.value);
        if (!resp?.data?.length) return;
        tableData.value = resp.data;

    } catch (err) {
        console.error("Failed to load activity data:", err);
    }
}

watch(chartYear, loadChartData);

onMounted(() => {
    loadChartData();
});
</script>

<template>
    <section>
        <h2>
            <label>🗓️:</label>
            <select v-model="chartYear">
                <option v-for="year in [2026].sort((a, b) => b - a)" :key="year" :value="year">
                    {{ year }}
                </option>
            </select>
        </h2>
        <ol>
            <li v-for="item in tableData" :key="item.plant_type">
                <span>{{ t(`addHarvest.type.${item.plant_type.toLocaleLowerCase()}`) }}</span>
                <span>{{item.count.reduce((accumulator,
                    currentValue) => accumulator + currentValue, 0)}}
                    {{ t(`addHarvest.unit.${item.count_unit.toLocaleLowerCase()}`) }}
                </span>
            </li>
        </ol>
    </section>
</template>

<style lang="css" scoped>
h2 {
    display: flex;
    flex-direction: row;
    align-items: center;
}

ol {
    gap: 0.5rem;
}

li {
    display: grid;
    grid-template-columns: 1fr 1fr;
}
</style>