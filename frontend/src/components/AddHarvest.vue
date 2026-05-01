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
    count: 0,
    count_unit: "",
    unit_price: 0,
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
        successMsg.value = t("addHarvest.msg.success", { rows: result.data })
    } catch (err: any) {
        error.value = err.message
    } finally {
        isLoading.value = false
    }
}
</script>
<template>
    <section>
        <h2>{{ t("addHarvest.title") }}</h2>

        <div class="gDate">
            <label>{{ t("addHarvest.date.title") }}</label>
            <input type="date" v-model="globalDate" required />
        </div>

        <form @submit.prevent="handleSubmit">
            <div v-for="(row, index) in rows" :key="index" class="rows">
                <input v-model="row.date" type="date" required hidden />
                <div>
                    <label>{{ t("addHarvest.type.title") }}</label>
                    <select v-model.lazy="row.plant_type" required>
                        <option value="" selected disabled></option>
                        <option value="Tomato">{{ t("addHarvest.type.tomato") }}</option>
                        <option value="Cucumber">{{ t("addHarvest.type.cucumber") }}</option>
                        <option value="Bellpepper">{{ t("addHarvest.type.bellpepper") }}</option>
                        <option value="Garlic">{{ t("addHarvest.type.garlic") }}</option>
                        <option value="Dill">{{ t("addHarvest.type.dill") }}</option>
                        <option value="Onion">{{ t("addHarvest.type.onion") }}</option>
                        <option value="Parsley">{{ t("addHarvest.type.parsley") }}</option>
                        <option value="Eggplant">{{ t("addHarvest.type.eggplant") }}</option>
                        <option value="Lovage">{{ t("addHarvest.type.lovage") }}</option>
                        <option value="Sorrel">{{ t("addHarvest.type.sorrel") }}</option>
                        <option value="Mint">{{ t("addHarvest.type.mint") }}</option>
                        <option value="Radish">{{ t("addHarvest.type.radish") }}</option>
                        <option value="Coriander">{{ t("addHarvest.type.coriander") }}</option>
                        <option value="Basil">{{ t("addHarvest.type.basil") }}</option>
                    </select>
                </div>
                <div>
                    <label>{{ t("addHarvest.count.title") }}</label>
                    <input v-model.number="row.count" type="number" step="0.1" min="0" required />
                </div>
                <div>
                    <label>{{ t("addHarvest.unit.title") }}</label>
                    <select v-model.lazy="row.count_unit" required>
                        <option disabled value="">{{ t("addHarvest.unit.title") }}</option>
                        <option value="kg">{{ t("addHarvest.unit.kg") }}</option>
                        <option value="box">{{ t("addHarvest.unit.box") }}</option>
                        <option value="bunch">{{ t("addHarvest.unit.bunch") }}</option>
                    </select>
                </div>
                <div>
                    <label>{{ t("addHarvest.price.title") }}</label>
                    <input v-model.number="row.unit_price" type="number" step="0.05" min="0" required />
                </div>
                <div>
                    <label>{{ t("addHarvest.remove.title") }}</label>
                    <button class="remove" type="button" @click="removeRow(index)">❌</button>
                </div>
            </div>

            <div class="btnsPanel">
                <button type="submit" :disabled="isLoading || rows.length === 0">
                    {{ isLoading ? t("addHarvest.msg.saving") + "..." : t("addHarvest.btn.submit") }}
                </button>

                <button type="button" @click="addRow">➕ {{ t("addHarvest.btn.add") }}</button>
            </div>            

            <p v-if="successMsg" class="success">{{ successMsg }}</p>
            <p v-if="error" class="error">{{ error }}</p>

        </form>
    </section>
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

.btnsPanel{
    display: flex;
    flex-direction: row;
    justify-content: space-between;
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

    @media (max-width: 750px) {
        grid-template-columns: 1fr;
    }
}

button {
    background-color: var(--bg2);

    padding: 0.5rem;
}
</style>