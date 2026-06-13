export function getISOWeekDates(year: number, week: number) {
    // January 4th is always in ISO week 1
    const jan4 = new Date(year, 0, 4);

    // Find Monday of week 1
    const dayOfWeek = jan4.getDay() || 7; // Sunday -> 7
    const week1Monday = new Date(jan4);
    week1Monday.setDate(jan4.getDate() - dayOfWeek + 1);

    // Monday of requested week
    const firstDay = new Date(week1Monday);
    firstDay.setDate(week1Monday.getDate() + (week - 1) * 7);

    // Sunday of requested week
    const lastDay = new Date(firstDay);
    lastDay.setDate(firstDay.getDate() + 6);

    return {
        firstDay,
        lastDay,
        month: firstDay.getMonth() + 1
    };
}

export function getCssVar(name: string): string {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}