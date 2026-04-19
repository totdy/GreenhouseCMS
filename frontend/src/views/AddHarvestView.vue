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
        <button type="button" @click="addRow">+ Add Row</button>

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
                <textarea v-model="row.note" placeholder="Note" rows="1" />
            </div>
            <button class="remove" type="button" @click="removeRow(index)">x Remove</button>
        </div>        

        <button type="submit" :disabled="isLoading || rows.length === 0 ">
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
}

.rows {
    display: grid;
    grid-template-columns: repeat(4, 1fr) ;
    gap: 0.5rem;

    background-color: var(--bg1);
    padding: 1rem;
    border-radius: 0.5rem;

    position: relative;

    div {
        display: flex;
        flex-direction: column;        

        input, select, textarea {
            border: none;
            border-radius: 0.5rem;

            padding: 0.5rem;

            height: 2rem;
            
            background-color: var(--bg2);            
        }
    }
}
.remove{
    align-self: end;

    width: -webkit-fill-available;

    background-color: rgb(255, 134, 134);
    color: red;

    padding: 0.4rem 0.6rem;
}
</style>