<script setup lang="ts">
import type { YearlyActivityItem } from "@/scripts/types";
import { isPlantType, getPlantUnit } from "@/scripts/plants";
import { computed } from "vue";

import { useI18n } from "vue-i18n";
const { t } = useI18n();

const props = defineProps<{
    data: YearlyActivityItem[]
}>();

const rows = computed(() => {
    const totals = new Map<string, number>();
    for (const row of props.data) {
        totals.set(row.plant_type, (totals.get(row.plant_type) ?? 0) + row.count);
    }
    return [...totals.entries()].map(([plant_type, total]) => ({ plant_type, total }));
});

</script>

<template>
    <section id="at">
        <h2>{{ t("activityTable.title") }}</h2>
        <ol>
            <li v-for="item in rows" :key="item.plant_type">
                <span>{{ t(`common.type.${item.plant_type}`) }}</span>
                <span>
                    {{ item.total }}
                    <template v-if="isPlantType(item.plant_type)">
                        {{ t(`common.unit.${getPlantUnit(item.plant_type)}`) }}
                    </template>
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
