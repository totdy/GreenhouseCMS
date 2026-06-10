<script setup lang="ts">
import { computed } from "vue";
import { useI18n } from "vue-i18n";
import type { MonthlyActivityItem } from "@/scripts/types";

const { t } = useI18n();

const props = defineProps<{
    monthLabel: string | null;
    entries: MonthlyActivityItem[];
    loading: boolean;
}>();

type WeekGroup = {
    week: number;
    fromDay: number;
    toDay: number;
    avg: number;
};

// Build calendar week windows for a given year/month (1-based).
// W1 starts on day 1 and ends on the day before the first Monday (or day 7
// if the 1st is already a Monday). Every subsequent week is Mon–Sun,
// and the last window is clipped to the last day of the month.
function calendarWindows(year: number, month: number): { from: number; to: number }[] {
    const daysInMonth = new Date(year, month, 0).getDate();
    const firstDow = new Date(year, month - 1, 1).getDay(); // 0=Sun,1=Mon,...
    // How many days until (and including) the first Saturday of the month,
    // i.e. end of the ISO partial week containing day 1.
    // If day 1 is Monday, first window is the full Mon-Sun week (7 days).
    const daysToFirstWeekEnd = firstDow === 1 ? 7 : (8 - firstDow) % 7 || 7;

    const windows: { from: number; to: number }[] = [];
    let from = 1;
    let firstEnd = daysToFirstWeekEnd;

    // First (possibly partial) week
    windows.push({ from, to: Math.min(firstEnd, daysInMonth) });
    from = firstEnd + 1;

    // Full Mon-Sun weeks
    while (from <= daysInMonth) {
        const to = Math.min(from + 6, daysInMonth);
        windows.push({ from, to });
        from = to + 1;
    }

    return windows;
}

const groups = computed((): WeekGroup[] => {
    if (!props.entries.length) return [];

    // Derive year and month from the first entry date "YYYY-MM-DD"
    const firstDate = props.entries[0]!.date;
    const year  = parseInt(firstDate.slice(0, 4), 10);
    const month = parseInt(firstDate.slice(5, 7), 10);

    const windows = calendarWindows(year, month);
    const result: WeekGroup[] = [];

    for (const { from, to } of windows) {
        const inWindow = props.entries.filter((e) => {
            const d = parseInt(e.date.slice(8, 10), 10);
            return d >= from && d <= to;
        });

        if (!inWindow.length) continue;

        const total = inWindow.reduce((sum, e) => sum + e.count, 0);
        const days  = to - from + 1;
        const avg   = Math.round((total / days) * 10) / 10;

        result.push({ week: result.length + 1, fromDay: from, toDay: to, avg });
    }

    return result;
});
</script>

<template>
    <section id="ad">
        <h2 v-if="monthLabel">{{ monthLabel }}</h2>

        <p v-if="loading" class="state-msg">...</p>

        <p v-else-if="!monthLabel" class="state-msg hint">
            {{ t("activityDaily.hint") }}
        </p>

        <p v-else-if="!groups.length" class="state-msg">
            {{ t("activityDaily.noData") }}
        </p>

        <ul v-else class="list">
            <li v-for="g in groups" :key="g.week">
                <span class="week">w{{ g.week }}</span>
                <span class="range">({{ g.fromDay }}-{{ g.toDay }})</span>
                <span class="avg">{{ g.avg }}kg</span>
            </li>
        </ul>
    </section>
</template>

<style lang="css" scoped>
#ad {
    grid-area: ad;
    position: relative;
}

h2 {
    margin-bottom: 0.6rem;
}

.state-msg {
    opacity: 0.55;
    font-size: 0.9rem;
}

.hint {
    font-style: italic;
}

.list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    font-size: 0.9rem;
}

li {
    display: flex;
    gap: 0.5rem;
    align-items: baseline;
}

.week {
    font-weight: 600;
    min-width: 2rem;
    color: var(--primary);
}

.range {
    opacity: 0.6;
    min-width: 5rem;
}

.avg {
    font-weight: 600;
}
</style>