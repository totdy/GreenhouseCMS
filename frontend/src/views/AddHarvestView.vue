<script setup lang="ts">
import { ref, watch } from "vue"
import type { HarvestItem } from "@/scripts/types"
import { addHarvests } from "@/scripts/api"

import { useI18n } from 'vue-i18n'
const { t } = useI18n()

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
        successMsg.value = t("addHarvest.successMsg", { rows: result.data })
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
            <label>{{t("addHarvest.date.title")}}</label>
            <input type="date" v-model="globalDate" required />
        </div>
        <div v-for="(row, index) in rows" :key="index" class="rows">
            <input v-model="row.date" type="date" required hidden />
            <div>
                <label>{{t("addHarvest.type.title")}}</label>
                <select v-model.lazy="row.plant_type" required>
                    <option value="" selected disabled></option>
                    <option value="Tomato">🍅 {{ t("addHarvest.type.tomato") }}</option>
                    <option value="Cucumber">🥒 {{ t("addHarvest.type.cucumber") }}</option>
                    <option value="Bell pepper">🫑 {{ t("addHarvest.type.bellPepper") }}</option>
                    <option value="Garlic">🧄 {{ t("addHarvest.type.garlic") }}</option>
                    <option value="Dill">🌿 {{ t("addHarvest.type.dill") }}</option>
                    <option value="Onion">🧅 {{ t("addHarvest.type.onion") }}</option>
                    <option value="Parsley">🌿 {{ t("addHarvest.type.parsley") }}</option>
                    <option value="Eggplant">🍆 {{ t("addHarvest.type.eggplant") }}</option>
                    <option value="Lovage">🌿 {{ t("addHarvest.type.lovage") }}</option>
                    <option value="Sorrel">🥬 {{ t("addHarvest.type.sorrel") }}</option>                                                        
                    <option value="Mint">🌿 {{ t("addHarvest.type.mint") }}</option>
                    <option value="Radish">🍎 {{ t("addHarvest.type.radish") }}</option>
                    <option value="Coriander">🌿 {{ t("addHarvest.type.coriander") }}</option>
                    <option value="Basil">💐 {{ t("addHarvest.type.basil") }}</option>                    
                </select>
            </div>
            <div style="display: none;">
                <label>Subtype</label>
                <select v-model.lazy="row.plant_subtype">
                    <option value="" selected></option>
                    <option value="Cherry">🍒</option>
                </select>
            </div>
            <div>
                <label>{{t("addHarvest.count.title")}}</label>
                <input v-model.number="row.count" type="number" step="0.1" min="0" required />
            </div>
            <div>
                <label>{{t("addHarvest.unit.title")}}</label>
                <select v-model.lazy="row.count_unit" required>
                    <option disabled value="">{{t("addHarvest.unit.title")}}</option>
                    <option value="kg">⚫kgs</option>
                    <option value="box">📦boxes</option>
                    <option value="bunch">💐bunches</option>
                </select>
            </div>
            <div>
                <label>{{t("addHarvest.price.title")}}</label>
                <input v-model.number="row.unit_price" type="number" step="0.05" min="0" required />
            </div>
            <div style="display: none;">
                <label>{{t("addHarvest.note.title")}}</label>
                <textarea v-model="row.note" placeholder="Note" rows="1" />
            </div>
            <div>
                <label>{{t("addHarvest.remove.title")}}</label>
                <button class="remove" type="button" @click="removeRow(index)">❌</button>
            </div>            
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

        width: 100%;

        background-color: var(--bg2);
    }
    & .remove {        
        width: -webkit-fill-available;

        background-color: rgb(255, 176, 176);
    }
}

.rows {
    display: grid;
    grid-template-columns: repeat(4, 1fr) 4rem;
    gap: 0.5rem;
}

@media (max-width: 900px) {
    .rows {
        grid-template-columns: 1fr;
    }
}

button {
    background-color: var(--bg1);

    padding: 0.5rem;
}
</style>