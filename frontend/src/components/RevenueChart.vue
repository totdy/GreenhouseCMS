<script setup lang="ts">
import ChartDataLabels from "chartjs-plugin-datalabels";
import Chart from "chart.js/auto";
Chart.register(ChartDataLabels);

import { nextTick, onMounted, ref, watch } from "vue";
import { GetRevenueByDate } from "@/scripts/api";
import type { RevenueByDateItem } from "@/scripts/types";

import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const canvasRef = ref<HTMLCanvasElement | null>(null);

let chart: Chart | null = null;

const chartYear = ref(new Date().getFullYear());

const MONTH_LABELS = [""];
const ZERO_DATA = [0];

function getCssVar(name: string): string {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function initChart() {
    if (!canvasRef.value) return;

    chart?.destroy();
    chart = null;

    chart = new Chart(canvasRef.value, {
        type: "line",
        data: {
            labels: [...MONTH_LABELS],
            datasets: [
                {
                    label: t("RevenueChart.title"),
                    data: [...ZERO_DATA],
                    borderColor: getCssVar("--primary"),
                    backgroundColor: getCssVar("--primary05"),
                    fill: true,
                    tension: 0.3,
                },
            ],
        },
        options: {
            responsive: true,
            animation: { duration: 600, easing: "easeInOutQuart" },
            scales: {
                x: {
                    ticks: { color: getCssVar("--text") },
                    title: { color: getCssVar("--text"), display: true, text: t("RevenueChart.xAxis") },
                    grid: { color: getCssVar("--highlight") },
                },
                y: {
                    ticks: { color: getCssVar("--text") },
                    title: { color: getCssVar("--text"), display: true, text: t("RevenueChart.yAxis") },
                    beginAtZero: true,
                    grid: { color: getCssVar("--highlight") },
                },
            },
            plugins: {
                datalabels: {
                    anchor: "end",
                    align: "top",
                    color: getCssVar("--text"),
                    font: { size: 11 },
                    formatter: (value: number) => `€${value.toLocaleString()}`,
                },
                legend: {
                    labels: { color: getCssVar("--text") },
                },
            },
        },
    });
}

async function setChartData(labels: string[], values: number[]) {
    if (!chart) return;
    await nextTick();
    chart.data.labels!.splice(0, chart.data.labels!.length, ...labels);
    (chart.data.datasets[0].data as number[]).splice(0, chart.data.datasets[0].data.length, ...values);
    chart.update();
}

async function loadChartData(resetFirst = true) {
    if (!chart) return;

    if (resetFirst) {
        await setChartData([...MONTH_LABELS], [...ZERO_DATA]);
    }

    try {
        const resp = await GetRevenueByDate(chartYear.value);
        const data: RevenueByDateItem[] = resp?.data ?? [];
        if (!data.length) return;
        await setChartData(
            data.map((row) => row.date),
            data.map((row) => row.revenue),
        );
    } catch (err) {
        console.error("Failed to load revenue data:", err);
    }
}

watch(chartYear, () => loadChartData(true));

onMounted(() => {
    initChart();
    loadChartData(false);
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