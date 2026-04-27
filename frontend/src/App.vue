<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router"
import ThemeToggle from "./components/ThemeToggle.vue";

import { useI18n } from 'vue-i18n'
const { t } = useI18n()

</script>

<template>
  <main>
    <nav>
      <RouterLink to="/">{{ t("navbar.home") }}</RouterLink>
      <RouterLink to="/add">{{ t("navbar.add") }}</RouterLink>
      <ThemeToggle class="end" />
    </nav>
    <RouterView />
  </main>
</template>

<style lang="css" scoped>
nav {
  display: flex;
  flex-direction: row;
  gap: 1rem;
  align-items: center;
  justify-content: flex-start;
  flex-wrap: nowrap;

  a {
    padding: 0.5rem 1rem;
  }

  .end {
    justify-self: flex-end;
  }
}

main {
  max-width: 60rem;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>