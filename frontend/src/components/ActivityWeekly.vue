<script setup lang="ts">
import { computed } from "vue";
import type { WeeklyActivityItem } from "@/scripts/types";
import { type PlantType, getPlantUnit } from "@/scripts/plants";
import { getISOWeekDates } from "@/scripts/functions.ts";

import { useI18n } from "vue-i18n";
const { t } = useI18n();

const props = defineProps<{
    data: WeeklyActivityItem[],
    plant: PlantType,
    year: number,
}>();

const MONTH_LABELS = [t("common.month.jan"), t("common.month.feb"), t("common.month.mar"), t("common.month.apr"), t("common.month.may"), t("common.month.jun"), t("common.month.jul"), t("common.month.aug"), t("common.month.sep"), t("common.month.oct"), t("common.month.nov"), t("common.month.dec")];

const fmt = (d: Date) => d.toISOString().split('T')[0]?.split('-').slice(2).join('') ?? '';

const weekRows = computed(() => {
    const unit = getPlantUnit(props.plant);
    return props.data
        .filter((e) => e.plant_type === props.plant)
        .map((e) => ({
            week: e.week,
            count: e.count,
            avg: Math.round((e.count / 7) * 10) / 10,
            unit,
        }));
});
</script>

<template>
    <section id="aw">
        <h2>{{ t("activityWeekly.title") }}</h2>
        <div>
            <ul class="week-rows">
                <li v-for="row in weekRows" :key="row.week">
                    <span>{{ t("activityWeekly.shortWeek") }}{{ row.week }}</span>
                    {{ MONTH_LABELS[getISOWeekDates(props.year, row.week).month - 1] }}
                    <span>
                        {{ fmt(getISOWeekDates(props.year, row.week).firstDay) }} - {{ fmt(getISOWeekDates(props.year,
                        row.week).lastDay) }}
                    </span>
                    ~{{ row.avg }}{{ t(`common.unit.${row.unit}`) }}/{{ t("activityWeekly.day") }}
                    <span class="total">{{ row.count }} {{ row.unit }}</span>
                </li>
            </ul>
        </div>
    </section>
</template>

<style lang="css" scoped>
#aw {
    grid-area: aw;
    position: relative;
    overflow-y: auto;
}

div {
    overflow: auto;
}

li {
    display: flex;
    flex-direction: column;
    background: var(--bg-light);
    padding: 0.5rem;
    border-radius: 0.5rem;
}

.week-rows {
    flex-direction: row;
    display: flex;
    gap: 1rem;
    flex-wrap: nowrap;
    width: fit-content;
}

.total {
    font-weight: 600;
    color: var(--primary);
    min-width: 4rem;
    text-align: right;
}
</style>