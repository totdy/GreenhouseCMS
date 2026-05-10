<script setup lang="ts">
import type { ActivitySeries } from "@/scripts/types";

import { useI18n } from "vue-i18n";
const { t } = useI18n();

const props = defineProps<{
    data: ActivitySeries[]
}>();

</script>

<template>
    <section id="at">
        <h2>{{ t("activityTable.title") }}</h2>
        <ol>
            <li v-for="item in props.data" :key="item.plant_type">
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
#at {
    grid-area: at;

    /* ???? */
    min-width: 20rem;
}

ol {
    gap: 0.5rem;
}

li {
    display: grid;
    grid-template-columns: 1fr 1fr;
}
</style>