<script setup lang="ts">
import ChartDataLabels from "chartjs-plugin-datalabels";
import Chart from "chart.js/auto";
Chart.register(ChartDataLabels);

import { nextTick, onMounted, ref, watch } from "vue";
import type { RevenueByDateItem } from "@/scripts/types";

import { useI18n } from 'vue-i18n'
const { t } = useI18n()

const MONTH_LABELS = [t("common.month.jan"), t("common.month.feb"), t("common.month.mar"), t("common.month.apr"), t("common.month.may"), t("common.month.jun"), t("common.month.jul"), t("common.month.aug"), t("common.month.sep"), t("common.month.oct"), t("common.month.nov"), t("common.month.dec")];

const props = defineProps<{
    data: RevenueByDateItem[];
}>();

const canvasRef = ref<HTMLCanvasElement | null>(null);

let chart: Chart | null = null;

const selectedMonth = ref<{ label: string; entries: RevenueByDateItem[] } | null>(null);

function getCssVar(name: string): string {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function groupByMonth(data: RevenueByDateItem[]): number[] {
    const buckets = Array(12).fill(0);
    for (const row of data) {
        const month = new Date(row.date).getMonth();
        buckets[month] += row.revenue;
    }
    return buckets;
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
                    label: t("revenueChart.title"),
                    data: Array(12).fill(0),
                    borderColor: getCssVar("--primary"),
                    backgroundColor: getCssVar("--primary05"),
                    fill: true,
                    tension: 0.3,
                    pointHoverRadius: 8,
                    pointHitRadius: 16,
                },
            ],
        },
        options: {
            responsive: true,
            animation: { duration: 600, easing: "easeInOutQuart" },
            layout: { padding: { top: 24 } },
            onClick: (_e, elements) => {
                if (!elements.length) {
                    selectedMonth.value = null;
                    return;
                }
                const monthIndex = elements[0].index;
                const entries = props.data.filter(
                    (row) => new Date(row.date).getMonth() === monthIndex
                );
                selectedMonth.value = {
                    label: MONTH_LABELS[monthIndex] || "",
                    entries,
                };
            },
            scales: {
                x: {
                    ticks: { color: getCssVar("--text") },
                    title: { color: getCssVar("--text"), display: false, text: t("revenueChart.xAxis") },
                    grid: { color: getCssVar("--highlight") },
                },
                y: {
                    ticks: { color: getCssVar("--text"), display: false },
                    title: { color: getCssVar("--text"), display: false, text: t("revenueChart.yAxis") },
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

    (chart.data.datasets[0].data as number[]).splice(
        0, 12, ...groupByMonth(data)
    );

    chart.update();
}

watch(
    () => props.data,
    (data) => {
        if (!chart) return;
        if (!data.length) {
            (chart.data.datasets[0].data as number[]).fill(0);
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
    <section id="rc">
        <h2>{{ t("revenueChart.title") }}</h2>
        <canvas ref="canvasRef"></canvas>

        <div v-if="selectedMonth" class="popup">
            <div class="popup-header">
                <span>{{ selectedMonth.label }}</span>
                <button @click="selectedMonth = null">✕</button>
            </div>
            <ul>
                <li v-for="entry in selectedMonth.entries" :key="entry.date">
                    <span>{{ entry.date }}</span>
                    <span>€{{ entry.revenue.toLocaleString() }}</span>
                </li>
            </ul>
        </div>
    </section>
</template>

<style lang="css" scoped>
#rc {
    grid-area: rc;
    position: relative;
}

.popup {
    position: absolute;
    top: 1rem;
    right: 1rem;
    z-index: 10;

    min-width: 220px;

    background: var(--bg-light);
    border: 1px solid var(--highlight);
    border-radius: 0.5rem;
    
    padding: 0.75rem;
    
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
}

.popup-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-weight: 600;
    margin-bottom: 0.5rem;

    button {
        background: none;
        border: none;
        cursor: pointer;
    }
}

li {
    display: flex;
    justify-content: space-between;
}
</style>