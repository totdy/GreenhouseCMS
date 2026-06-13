<script lang="ts" setup>
import type { YearlyRevenueItem } from '@/scripts/types';
import { ref, watch } from 'vue';

import { useI18n } from "vue-i18n";
const { t } = useI18n();

const props = defineProps<{
    data: YearlyRevenueItem[],
    year: number
}>();

const currentMonth = ref(new Date().getMonth());
const currentYear = ref(new Date().getFullYear());

const yearlyRevenue = ref(0);
const monthlyRevenue = ref(0);

function roundToTwo(num: number) {
    return Math.round(num * 100) / 100;
}

function calculateRevenue() {
    yearlyRevenue.value = roundToTwo(props.data.reduce((sum, item) => sum + item.revenue, 0));
    monthlyRevenue.value = roundToTwo(yearlyRevenue.value / (props.year === currentYear.value ? currentMonth.value + 1 : 12));
}

watch(() => props.data, calculateRevenue, { deep: true, immediate: true });

</script>
<template>
    <section id="rty">
        <h2>{{ t('revenueTable.title.y') }}</h2>
        <h1>€{{ yearlyRevenue }}</h1>
    </section>
    <section id="rtm">
        <h2>{{ t('revenueTable.title.m') }}</h2>
        <h1>€{{ monthlyRevenue }}</h1>
    </section>
</template>
<style lang="css" scoped>
#rty {
    grid-area: rty;
}

#rtm {
    grid-area: rtm;
}
</style>
