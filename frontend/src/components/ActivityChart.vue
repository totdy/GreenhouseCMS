<script setup lang="ts">
import ChartDataLabels from "chartjs-plugin-datalabels";
import Chart from "chart.js/auto";
Chart.register(ChartDataLabels);

import { nextTick, onMounted, ref, watch } from "vue";
import type { ActivitySeries } from "@/scripts/types";

import { useI18n } from "vue-i18n";
const { t } = useI18n();

const props = defineProps<{
    data: ActivitySeries[];
}>();

const canvasRef = ref<HTMLCanvasElement | null>(null);

let chart: Chart | null = null;

const MONTH_LABELS = [t("common.month.jan"), t("common.month.feb"), t("common.month.mar"), t("common.month.apr"), t("common.month.may"), t("common.month.jun"), t("common.month.jul"), t("common.month.aug"), t("common.month.sep"), t("common.month.oct"), t("common.month.nov"), t("common.month.dec")];

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
            datasets: [],
        },
        options: {
            responsive: true,            
            animation: { duration: 600, easing: "easeInOutQuart" },
            scales: {
                x: {
                    stacked: true,
                    ticks: { color: getCssVar("--text")},
                    title: { display: false },
                    grid: { color: getCssVar("--highlight") },
                },
                y: {
                    beginAtZero: true,
                    ticks: { display: false },
                    title: { display: false },
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

async function applyData(data: ActivitySeries[]) {
    if (!chart) return;
    await nextTick();

    chart.data.datasets = data.map((s) => {
        const color = getCssVar("--primary");
        return {
            label: t(`addHarvest.type.${s.plant_type.toLowerCase()}`),
            data: s.count,
            borderColor: color,
            backgroundColor: color,
            borderWidth: 2,
            fill: false,
            tension: 0.3,
        };
    });

    chart.update();
}

watch(
    () => props.data,
    (data) => {
        if (!chart) return;
        if (!data.length) {
            chart.data.datasets = [];
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
    <section id="ac">
        <h2>{{ t("activityChart.title") }}</h2>
        <canvas ref="canvasRef"></canvas>
    </section>
</template>

<style lang="css" scoped>
#ac {
    grid-area: ac;
}
</style>