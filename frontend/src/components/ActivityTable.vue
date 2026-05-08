<script setup lang="ts">
import { onMounted, ref, watch } from "vue";
import { GetActivityByYear } from "@/scripts/api";
import type { ActivitySeries } from "@/scripts/types";
import { useI18n } from "vue-i18n";

const { t } = useI18n();

const props = defineProps<{
    year: number;
}>();

const tableData = ref<ActivitySeries[]>([]);

async function loadChartData() {
    try {
        const resp = await GetActivityByYear(props.year);        
        tableData.value = resp.data;

    } catch (err) {
        console.error("Failed to load activity data:", err);
    }
}

watch(() => props.year, loadChartData);

onMounted(() => {
    loadChartData();
});
</script>

<template>
    <section>
        <ol>
            <li v-for="item in tableData" :key="item.plant_type">
                <span>{{ t(`addHarvest.type.${item.plant_type.toLocaleLowerCase()}`) }}</span>
                <span>{{item.count.reduce((accumulator,
                    currentValue) => accumulator + currentValue, 0)}}
                    {{ t(`addHarvest.unit.${item.count_unit.toLocaleLowerCase()}`) }}
                </span>
            </li>
        </ol>
    </section>
</template>

<style lang="css" scoped>
ol {
    gap: 0.5rem;
}

li {
    display: grid;
    grid-template-columns: 1fr 1fr;
}
</style>