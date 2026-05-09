<script lang="ts" setup>
import type { RevenueByDateItem } from '@/scripts/types';
import { ref, watch } from 'vue';

import { useI18n } from "vue-i18n";
const { t } = useI18n();

const props = defineProps<{
    data: RevenueByDateItem[]
}>();

const yearlyRevenue = ref(0);
const monthlyRevenue = ref(0);

function calculateRevenue() {
    yearlyRevenue.value = props.data.reduce((sum, item) => sum + item.revenue, 0);
    monthlyRevenue.value = Math.round(yearlyRevenue.value / 12 * 100) / 100;
}

watch(() => props.data, calculateRevenue, { deep: true, immediate: true });

</script>
<template>
    <div class="panels">
        <section>
            <h2>{{ t('revenueTable.title.y') }}</h2>
            <h1>€{{ yearlyRevenue }}</h1>
        </section>
        <section>
            <h2>{{ t('revenueTable.title.m') }}</h2>
            <h1>€{{ monthlyRevenue }}</h1>
        </section>
    </div>
</template>
<style lang="css" scoped>
.panels {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;
    gap: 1rem;
}
</style>