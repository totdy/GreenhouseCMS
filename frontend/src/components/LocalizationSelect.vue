<template>
    <select :value="locale" @change="onLocaleChange">
        <option value="en">English</option>
        <option value="ua">Українська</option>
    </select>
</template>

<script setup lang="ts">
import { useI18n } from "vue-i18n"

const { locale } = useI18n()

function onLocaleChange(event: Event) {
    const newLocale = (event.target as HTMLSelectElement).value
    locale.value = newLocale
    localStorage.setItem("locale", newLocale)
}
</script>