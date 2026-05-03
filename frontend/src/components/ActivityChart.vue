<script setup lang="ts">
import ChartDataLabels from "chartjs-plugin-datalabels";
import Chart from "chart.js/auto";
Chart.register(ChartDataLabels);

import { nextTick, onMounted, ref, watch } from "vue";
import { GetActivityByYear } from "@/scripts/api";
import type { ActivityPivotResponse } from "@/scripts/types";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const canvasRef = ref<HTMLCanvasElement | null>(null);

let chart: Chart | null = null;

const chartYear = ref(new Date().getFullYear());

const MONTH_LABELS = [t("common.month.jan"), t("common.month.feb"), t("common.month.mar"), t("common.month.apr"), t("common.month.may"), t("common.month.jun"), t("common.month.jul"), t("common.month.aug"), t("common.month.sep"), t("common.month.oct"), t("common.month.nov"), t("common.month.dec")];

function getCssVar(name: string): string {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function initChart() {
    if (!canvasRef.value) return;

    chart?.destroy();
    chart = null;

    chart = new Chart(canvasRef.value, {
        type: "bar",
        data: {
            labels: [...MONTH_LABELS],
            datasets: [],
        },
        options: {
            responsive: true,
            animation: { duration: 600, easing: "easeInOutQuart" },
            scales: {
                x: {
                    stacked: true,
                    ticks: { color: getCssVar("--text") },
                    title: { color: getCssVar("--text"), display: true, text: t("activityChart.xAxis") },
                    grid: { color: getCssVar("--highlight") },
                },
                y: {
                    stacked: true,
                    ticks: { color: getCssVar("--text") },
                    title: { color: getCssVar("--text"), display: true, text: t("activityChart.yAxis") },
                    beginAtZero: true,
                    grid: { color: getCssVar("--highlight") },
                },
            },
            plugins: {
                datalabels: {
                    clip: false,
                    color: getCssVar("--text"),
                    font: { size: 10 },
                    display: (ctx) => (ctx.dataset.data[ctx.dataIndex] as number) > 0,
                    formatter: (value: number) => value,
                },
                legend: {
                    labels: { color: getCssVar("--text") },
                },
            },
        },
    });
}

async function setChartData({ data }: ActivityPivotResponse) {
    if (!chart) return;
    await nextTick();

    chart.data.datasets.splice(
        0,
        chart.data.datasets.length,
        ...data.map((s, i) => ({
            label: t(`addHarvest.type.${s.plant_type.toLowerCase()}`),
            data: s.count,
            backgroundColor: getCssVar("--primary"),
        }))
    );

    chart.update();
}

async function loadChartData() {
    if (!chart) return;

    try {
        const resp = await GetActivityByYear(chartYear.value);
        if (!resp?.data?.length) return;
        await setChartData(resp);
    } catch (err) {
        console.error("Failed to load activity data:", err);
    }
}

watch(chartYear, loadChartData);

onMounted(() => {
    initChart();
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
        <canvas ref="canvasRef"></canvas>
    </section>
</template>

<style lang="css" scoped>
h2 {
    display: flex;
    flex-direction: row;
    align-items: center;
}
</style>