<script setup lang="ts">
import { ref } from "vue"
import type { HarvestItem } from "@/scripts/types"
import { addHarvests } from "@/scripts/api"

const createEmptyRow = (): HarvestItem => ({
    date: "",
    plant_type: "",
    plant_subtype: "",
    count: 0,
    count_unit: "",
    unit_price: 0,
    note: "",
})

const rows = ref<HarvestItem[]>([createEmptyRow()])

function addRow() {
    rows.value.push(createEmptyRow())
}

function removeRow(index: number) {
    rows.value.splice(index, 1)
}

async function handleSubmit() {
    await addHarvests({ data: rows.value })
}
</script>

<template>
    <form @submit.prevent="handleSubmit">

        <div v-for="(row, index) in rows" :key="index">
            <input v-model="row.date" type="date" required />
            <input v-model="row.plant_type" placeholder="Plant type" required />
            <input v-model="row.plant_subtype" placeholder="Plant subtype" required />
            <input v-model.number="row.count" type="number" step="0.01" required />
            <input v-model="row.count_unit" placeholder="Unit" required />
            <input v-model.number="row.unit_price" type="number" step="0.0001" required />
            <textarea v-model="row.note" placeholder="Note" />
            <button type="button" @click="removeRow(index)">Remove</button>
        </div>

        <button type="button" @click="addRow">+ Add Row</button>
        <button type="submit">Submit All</button>

    </form>
</template>