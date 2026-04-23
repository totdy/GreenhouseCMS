<script setup lang="ts">
import { ref, watch } from "vue"
import type { HarvestItem } from "@/scripts/types"
import { addHarvests } from "@/scripts/api"

const isLoading = ref(false)
const error = ref<string | null>(null)
const successMsg = ref<string | null>(null)

const globalDate = ref(new Date().toISOString().split("T")[0] || "")

watch(globalDate, (newDate) => {
    rows.value.forEach(row => row.date = newDate)
})

const createEmptyRow = (): HarvestItem => ({
    date: globalDate.value,
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
    <button type="button" @click="addRow">+ Add Row</button>

    <form @submit.prevent="handleSubmit">
        <div class="gDate">
            <label>Date</label>
            <input type="date" v-model="globalDate" required />
        </div>
        <div v-for="(row, index) in rows" :key="index" class="rows">
            <input v-model="row.date" type="date" required hidden />
            <div>
                <label>Type</label>
                <select v-model.lazy="row.plant_type" required>
                    <option value="" selected disabled></option>
                    <option value="Tomato">🍅</option>
                    <option value="Cucumber">🥒</option>
                    <option value="Bell pepper">🫑</option>
                    <option value="Garlic">🧄</option>
                    <option value="Onion">🧅</option>
                    <option value="Eggplant">🍆</option>
                </select>
            </div>
            <div>
                <label>Subtype</label>
                <select v-model.lazy="row.plant_subtype">
                    <option value="" selected></option>
                    <option value="Cherry">🍒</option>
                </select>
            </div>
            <div>
                <label>Count</label>
                <input v-model.number="row.count" type="number" step="0.1" min="0" required />
            </div>
            <div>
                <label>Unit</label>
                <select v-model.lazy="row.count_unit" required>
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
                <textarea v-model="row.note" placeholder="Note" rows="1" />
            </div>
            <button class="remove" type="button" @click="removeRow(index)">x Remove</button>
        </div>

        <button type="submit" :disabled="isLoading || rows.length === 0">
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

form {
    display: flex;
    flex-direction: column;
    gap: 1rem;

    background-color: var(--bg1);
    padding: 1rem;
    border-radius: 0.5rem;
}

.gDate,
.rows div {
    display: flex;
    flex-direction: column;

    input,
    select,
    textarea {
        border: none;
        border-radius: 0.5rem;

        padding: 0.5rem;

        height: 2rem;

        background-color: var(--bg2);
    }
}

.rows {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.5rem;
}

@media (max-width: 900px) {
    .rows {
        grid-template-columns: 1fr;
    }
}

button {
    background-color: var(--bg1);

    padding: 0.5rem 1rem;
}

.remove {
    align-self: end;

    width: -webkit-fill-available;

    background-color: rgb(207, 207, 207);
}
</style>