<script setup lang="ts">
import Chart from 'chart.js/auto';
import { onMounted, ref } from 'vue';

const canvasRef = ref<HTMLCanvasElement | null>(null);

const data = [
    { year: 2010, count: 10 },
    { year: 2011, count: 20 },
    { year: 2012, count: 15 },
    { year: 2013, count: 25 },
    { year: 2014, count: 22 },
    { year: 2015, count: 30 },
    { year: 2016, count: 28 },
];

onMounted(() => {
    if (!canvasRef.value) return;

    new Chart(canvasRef.value, {
        type: "bar",
        data: {
            labels: data.map(row => row.year),
            datasets: [
                {
                    label: "Acquisitions by year",
                    data: data.map(row => row.count)
                }
            ]
        }
    });
});

</script>

<template>
    <div style="width: 600px;">
        <canvas ref="canvasRef"></canvas>
    </div>
</template>

<style scoped></style>