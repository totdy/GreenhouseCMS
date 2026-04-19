<script setup lang="ts">
import { ref } from "vue"
import type { HarvestItem } from "@/scripts/types"
import { addHarvests } from "@/scripts/api"

const isLoading = ref(false)
const error = ref<string | null>(null)
const successMsg = ref<string | null>(null)

const createEmptyRow = (): HarvestItem => ({
    date: new Date().toISOString().split("T")[0] || "",
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

        <div v-for="(row, index) in rows" :key="index" class="rows">
            <div>
                <label>Day</label>
                <input v-model="row.date" type="date" required />
            </div>
            <div>
                <label>Type</label>
                <input v-model="row.plant_type" placeholder="Tomato" required />
            </div>
            <div>
                <label>Subtype</label>
                <input v-model="row.plant_subtype" placeholder="Cherry" />
            </div>
            <div>
                <label>Count</label>
                <input v-model.number="row.count" type="number" step="0.1" min="0" required />
            </div>
            <div>
                <label>Unit</label>
                <select v-model="row.count_unit" required>
                    <option disabled value="">Unit</option>
                    <option value="kg">kgs</option>
                    <option value="box">boxes</option>
                    <option value="bunch">bunches</option>
                </select>
            </div>
            <div>
                <label>Price</label>
                <input v-model.number="row.unit_price" type="number" step="0.05" min="0" required />
            </div>
            <div>
                <label>Note</label>
                <textarea v-model="row.note" placeholder="Note" />
            </div>
            <button type="button" @click="removeRow(index)">x Remove</button>
        </div>

        <button type="button" @click="addRow">+ Add Row</button>
        <button type="submit" :disabled="isLoading">
            {{ isLoading ? "Saving..." : "Submit All" }}
        </button>

        <p v-if="successMsg" class="success">{{ successMsg }}</p>
        <p v-if="error" class="error">{{ error }}</p>

    </form>
</template>
<style lang="css" scoped>
.success {
    color: green;
}

.error {
    color: red;
}

.rows {
    display: flex;
    flex-direction: row;

    div {
        display: flex;
        flex-direction: column;
        width: 5.5rem;
    }
}
</style>