<script lang="ts" setup>
import type { YearlyRevenueItem } from '@/scripts/types';
import { ref, watch } from 'vue';

import { useI18n } from "vue-i18n";
const { t } = useI18n();

const props = defineProps<{
    data: YearlyRevenueItem[],
    currentMonth: number
}>();

const yearlyRevenue = ref(0);
const monthlyRevenue = ref(0);

function calculateRevenue() {
    yearlyRevenue.value = props.data.reduce((sum, item) => sum + item.revenue, 0);
    monthlyRevenue.value = Math.round(yearlyRevenue.value / props.currentMonth * 100) / 100;
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
