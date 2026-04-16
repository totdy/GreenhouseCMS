<script setup lang="ts">
import { ref } from "vue"
import type { HarvestItem } from "@/scripts/types"
import { addHarvests } from "@/scripts/api"

const isLoading = ref(false)
const error = ref<string | null>(null)
const successMsg = ref<string | null>(null)

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
    isLoading.value = true
    error.value = null
    successMsg.value = null

    try {
        const result = await addHarvests({ data: rows.value })
        successMsg.value = `Inserted ${result.data} row(s) successfully!`
    } catch (err: any) {
        error.value = err.message
    } finally {
        isLoading.value = false
    }
}
</script>

<template>
    <form @submit.prevent="handleSubmit">

        <div v-for="(row, index) in rows" :key="index">
            <input v-model="row.date" type="date" required />
            <input v-model="row.plant_type" placeholder="Plant type" required />
            <input v-model="row.plant_subtype" placeholder="Plant subtype" />
            <input v-model.number="row.count" type="number" step="0.01" required />
            <input v-model="row.count_unit" placeholder="Unit" required />
            <input v-model.number="row.unit_price" type="number" step="0.0001" required />
            <textarea v-model="row.note" placeholder="Note" />
            <button type="button" @click="removeRow(index)">Remove</button>
        </div>

        <button type="button" @click="addRow">+ Add Row</button>
        <button type="submit" :disabled="isLoading">
            {{ isLoading ? "Saving..." : "Submit All" }}
        </button>

        <p v-if="successMsg" style="color: green">{{ successMsg }}</p>
        <p v-if="error" style="color: red">{{ error }}</p>
    </form>
</template>