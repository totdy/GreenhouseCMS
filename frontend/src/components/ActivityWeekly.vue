<script setup lang="ts">
import ChartDataLabels from "chartjs-plugin-datalabels";
import Chart from "chart.js/auto";
Chart.register(ChartDataLabels);

import { computed, nextTick, onMounted, ref, watch } from "vue";
import type { WeeklyActivityItem } from "@/scripts/types";
import { type PlantType, getPlantUnit } from "@/scripts/plants";
import { getCssVar, getISOWeekDates } from "@/scripts/functions";

import { useI18n } from "vue-i18n";
const { t } = useI18n();

const props = defineProps<{
    data: WeeklyActivityItem[],
    plant: PlantType,
    year: number,
}>();

const MONTH_LABELS = [t("common.month.jan"), t("common.month.feb"), t("common.month.mar"), t("common.month.apr"), t("common.month.may"), t("common.month.jun"), t("common.month.jul"), t("common.month.aug"), t("common.month.sep"), t("common.month.oct"), t("common.month.nov"), t("common.month.dec")];

const canvasRef = ref<HTMLCanvasElement | null>(null);

let chart: Chart | null = null;

const weekRows = computed(() => {
    const unit = getPlantUnit(props.plant);
    return props.data
        .filter((e) => e.plant_type === props.plant)
        .map((e) => ({
            week: e.week,
            count: e.count,
            avg: Math.round((e.count / 7) * 10) / 10,
            unit,
        }))
        .sort((a, b) => a.week - b.week);
});

function fmt(d: Date) {
    return d.toISOString().split('T')[0]?.split('-').slice(2).join('') ?? '';
}

const unitLabel = computed(() => t(`common.unit.${getPlantUnit(props.plant)}`));

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
                    label: `${t("activityWeekly.title")}`,
                    data: [],
                    borderColor: getCssVar("--primary"),
                    backgroundColor: getCssVar("--primary05"),
                    fill: true,
                    tension: 0.3,
                    pointHoverRadius: 8,
                    pointHitRadius: 16,
                },
                {
                    label: `~${t("activityWeekly.day")}`,
                    data: [],
                    borderColor: getCssVar("--highlight"),
                    backgroundColor: "transparent",
                    borderDash: [6, 4],
                    fill: false,
                    tension: 0.3,
                    pointHoverRadius: 8,
                    pointHitRadius: 16,
                },
            ],
        },
        options: {
            responsive: true,
            animation: { duration: 600, easing: "easeInOutQuart" },
            scales: {
                x: {
                    ticks: { color: getCssVar("--text") },
                    title: { color: getCssVar("--text"), display: false, text: t("activityWeekly.shortWeek") },
                    grid: { color: getCssVar("--highlight") },
                },
                y: {
                    ticks: { color: getCssVar("--text"), display: false },
                    title: { color: getCssVar("--text"), display: false, text: unitLabel.value },
                    beginAtZero: true,
                    grid: { color: getCssVar("--highlight") },
                },
            },
            plugins: {
                datalabels: {
                    anchor: "end",
                    align: "top",
                    clip: false,
                    color: getCssVar("--text"),
                    font: { size: 11 },
                    display: (ctx) => (ctx.dataset.data[ctx.dataIndex] as number) > 0,
                    formatter: (value: number, ctx) => {
                        if (ctx.datasetIndex === 1) return value.toLocaleString();
                        return `${value.toLocaleString()}`;
                    },
                },
                legend: {
                    labels: { color: getCssVar("--text") },
                },
            },
        },
    });
}

async function applyData() {
    if (!chart) return;
    await nextTick();

    chart.data.labels = weekRows.value.map((row) => `${ MONTH_LABELS[getISOWeekDates(props.year, row.week).month - 1] } ${fmt(getISOWeekDates(props.year, row.week).firstDay)} - ${fmt(getISOWeekDates(props.year, row.week).lastDay)}`);

    const totalDataset = chart.data.datasets[0];
    const avgDataset = chart.data.datasets[1];
    if (!totalDataset || !avgDataset) return;

    totalDataset.label = `${t("activityWeekly.title")}`;
    avgDataset.label = `~${t("activityWeekly.day")}`;

    (totalDataset.data as number[]).splice(
        0, totalDataset.data.length, ...weekRows.value.map((row) => row.count)
    );
    (avgDataset.data as number[]).splice(
        0, avgDataset.data.length, ...weekRows.value.map((row) => row.avg)
    );

    chart.update();
}

watch(
    () => [props.data, props.plant] as const,
    () => {
        if (!chart) return;
        void applyData();
    },
    { deep: true },
);

onMounted(() => {
    initChart();
    void applyData();
});
</script>

<template>
    <section id="aw">
        <h2>{{ t("activityWeekly.title") }}</h2>
        <canvas ref="canvasRef"></canvas>
    </section>
</template>

<style lang="css" scoped>
#aw {
    grid-area: aw;
    position: relative;
}
</style>
