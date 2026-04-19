<script setup lang="ts">
import Chart from 'chart.js/auto';
import { onMounted, ref } from 'vue';

const canvasRef = ref<HTMLCanvasElement | null>(null);

onMounted(async () => {
    if (!canvasRef.value) return;

    const res = await fetch('http://localhost:8000/harvests/revenue-by-date');
    const json = await res.json();
    const data: { date: string; revenue: number }[] = json.data;

    new Chart(canvasRef.value, {
        type: 'line',
        data: {
            labels: data.map(row => row.date),
            datasets: [
                {
                    label: 'Revenue',
                    data: data.map(row => row.revenue),
                    borderColor: '#4caf82',
                    backgroundColor: 'rgba(76, 175, 130, 0.1)',
                    fill: true,
                    tension: 0.3,
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                x: { title: { display: true, text: 'Date' } },
                y: { title: { display: true, text: 'Revenue' }, beginAtZero: true },
            }
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