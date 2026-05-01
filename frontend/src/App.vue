<script setup lang="ts">
import { RouterLink, RouterView } from "vue-router"
import ThemeToggle from "@/components/ThemeToggle.vue";
import LocalizationSelect from "@/components/LocalizationSelect.vue";

import { useI18n } from 'vue-i18n'
const { t } = useI18n()

</script>

<template>
  <header>
    <nav>
      <RouterLink to="/">{{ t("navbar.home") }}</RouterLink>
      <RouterLink to="/add">{{ t("navbar.add") }}</RouterLink>
      <ThemeToggle />
    </nav>
  </header>
  <main>
    <RouterView />
  </main>
  <footer>
    <LocalizationSelect />
  </footer>
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

  :last-child {
    margin-left: auto;
  }
}

main,
header,
footer {
  max-width: 60rem;
  width: 100%;
}

main {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

footer {
  margin-top: auto;
}
</style>