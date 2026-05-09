<script setup lang="ts">
import ChartDataLabels from "chartjs-plugin-datalabels";
import Chart from "chart.js/auto";
Chart.register(ChartDataLabels);

import { nextTick, onMounted, ref, watch } from "vue";
import type { RevenueByDateItem } from "@/scripts/types";

import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const props = defineProps<{
    data: RevenueByDateItem[];
}>();

const canvasRef = ref<HTMLCanvasElement | null>(null);

let chart: Chart | null = null;

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
            labels: [],
            datasets: [
                {
                    label: t("revenueChart.title"),
                    data: [],
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
                    title: { color: getCssVar("--text"), display: true, text: t("revenueChart.xAxis") },
                    grid: { color: getCssVar("--highlight") },
                },
                y: {
                    ticks: { color: getCssVar("--text") },
                    title: { color: getCssVar("--text"), display: true, text: t("revenueChart.yAxis") },
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

async function applyData(data: RevenueByDateItem[]) {
    if (!chart) return;
    await nextTick();

    chart.data.labels = data.map((row) => row.date);
    chart.data.datasets[0].data = data.map((row) => row.revenue);

    chart.update();
}

watch(
    () => props.data,
    (data) => {
        if (!chart) return;
        if (!data.length) {
            chart.data.datasets[0].data = [];
            chart.update();
            return;
        }
        void applyData(data);
    },
    { deep: true },
);

onMounted(() => {
    initChart();
    if (props.data.length) void applyData(props.data);
});
</script>

<template>
    <section>
        <h2>{{ t("revenueChart.title") }}</h2>
        <canvas ref="canvasRef"></canvas>
    </section>
</template>

<style lang="css" scoped></style>