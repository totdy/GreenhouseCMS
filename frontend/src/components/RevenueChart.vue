<script setup lang="ts">
import ChartDataLabels from "chartjs-plugin-datalabels";
import Chart from "chart.js/auto";
Chart.register(ChartDataLabels);

import { nextTick, onMounted, ref, watch } from "vue";
import { GetRevenueByDate } from "@/scripts/api";
import type { RevenueByDateItem } from "@/scripts/types";

import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const props = defineProps<{
    year: number;
}>();

const canvasRef = ref<HTMLCanvasElement | null>(null);

let chart: Chart | null = null;

const EMPTY_LABELS = [""];
const EMPTY_DATA = [0];

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
            labels: [...EMPTY_LABELS],
            datasets: [
                {
                    label: t("revenueChart.title"),
                    data: [...EMPTY_DATA],
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
        await setChartData([...EMPTY_LABELS], [...EMPTY_DATA]);
    }

    try {
        const resp = await GetRevenueByDate(props.year);
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

watch(() => props.year, () => loadChartData(true));

onMounted(() => {
    initChart();
    loadChartData(false);
});
</script>

<template>
    <section>
        <canvas ref="canvasRef"></canvas>
    </section>
</template>

<style lang="css" scoped></style>