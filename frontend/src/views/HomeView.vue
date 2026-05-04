<script setup lang="ts">
import RevenueChart from '@/components/RevenueChart.vue';
import ActivityChart from '@/components/ActivityChart.vue';
import ActivityTable from '@/components/ActivityTable.vue';
</script>

<template>
  <RevenueChart />
  <div>
    <ActivityChart />
    <ActivityTable />
  </div>  
</template>

<style lang="css" scoped>
div {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1rem;
}
</style>