<script setup lang="ts">
import Chart from "chart.js/auto";
import { nextTick, onMounted, ref, watch } from "vue";
import { GetRevenueByDate } from "@/scripts/api";

import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const canvasRef = ref<HTMLCanvasElement | null>(null);

let chart: Chart | null = null;

const chartYear = ref(new Date().getFullYear());

const MONTH_LABELS = [""];
const ZERO_DATA = [0];

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
                    label: t("home.chart.title"),
                    data: [...ZERO_DATA],
                    borderColor: "#4caf82",
                    backgroundColor: "rgba(76, 175, 130, 0.1)",
                    fill: true,
                    tension: 0.3,
                },
            ],
        },
        options: {
            responsive: true,
            animation: { duration: 600, easing: "easeInOutQuart" },
            scales: {
                x: { title: { display: true, text: t("home.chart.xAxis") } },
                y: { title: { display: true, text: t("home.chart.yAxis") }, beginAtZero: true },
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
        const data: { date: string; revenue: number }[] = resp?.data ?? [];
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
    <div>
        <div>
            <label>🗓️:</label>
            <select v-model="chartYear">
                <option
                    v-for="year in [2023, 2024, 2025, 2026].sort((a, b) => b - a)"
                    :key="year"
                    :value="year"
                >
                    {{ year }}
                </option>
            </select>
        </div>
        <canvas ref="canvasRef"></canvas>
    </div>
</template>

<style scoped>
div {
    background-color: var(--bg1);
    border-radius: 0.5rem;
    width: -webkit-fill-available;
}
</style>