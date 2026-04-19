<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import ThemeToggle from "./components/ThemeToggle.vue";
</script>

<template>
  <main>
    <nav>
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/add">Add</RouterLink>
      <ThemeToggle />
    </nav>
    <RouterView />
  </main>
</template>

<style lang="css" scoped>
nav {
  display: flex;
  flex-direction: row;
  gap: 1rem;

  a {
    padding: 0.5rem 1rem;
  }
}

main {
  max-width: 60rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
</style>