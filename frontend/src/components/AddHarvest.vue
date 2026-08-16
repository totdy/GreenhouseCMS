<script setup lang="ts">
import { ref, watch } from "vue"
import type { HarvestIn } from "@/scripts/types"
import { AddHarvests } from "@/scripts/api"
import { useHarvest } from "@/scripts/useHarvest"
import { DEFAULT_PLANT, PLANT_LIST } from "@/scripts/plants"
import { DESTINATION_LIST, isDestination, type Destination } from "@/scripts/destinations"

import { useI18n } from 'vue-i18n'
import PopUp from "./PopUp.vue"
const { t } = useI18n()

const isLoading = ref(false)
const error = ref<string | null>(null)
const successMsg = ref<string | null>(null)

const globalDate = ref(new Date().toISOString().split("T")[0] || "")
const globalDestination = ref<Destination | "">("")

watch(globalDate, (newDate) => {
    rows.value.forEach(row => row.date = newDate)
})

watch(globalDestination, (newDestination) => {
    rows.value.forEach(row => row.destination = newDestination)
})

const { loadPage } = useHarvest()

type HarvestFormRow = Omit<HarvestIn, "destination"> & {
    destination: Destination | ""
}

const createEmptyRow = (): HarvestFormRow => ({
    date: globalDate.value,
    plant_type: DEFAULT_PLANT,
    destination: globalDestination.value,
    count: 0,
    unit_price: 0,
})

const rows = ref<HarvestFormRow[]>([createEmptyRow()])

function toHarvest(row: HarvestFormRow): HarvestIn {
    if (!isDestination(row.destination)) {
        throw new Error(t("addHarvest.msg.destinationRequired"))
    }

    return { ...row, destination: row.destination }
}

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
        const result = await AddHarvests({ data: rows.value.map(toHarvest) })

        successMsg.value = t("addHarvest.msg.success", { rows: result.inserted })

        await loadPage(1)
    } catch (err: unknown) {
        error.value = err instanceof Error ? err.message : String(err)
    } finally {
        isLoading.value = false
    }
}
</script>
<template>
    <section>
        <h2>{{ t("addHarvest.title") }}</h2>

        <form @submit.prevent="handleSubmit">
            <div class="globalFields">
                <div>
                    <label>{{ t("addHarvest.date.title") }}</label>
                    <input type="date" v-model="globalDate" required />
                </div>
                <div>
                    <label>{{ t("addHarvest.destination.title") }}</label>
                    <select v-model="globalDestination" required>
                        <option value="" disabled></option>
                        <option v-for="destination in DESTINATION_LIST" :key="destination" :value="destination">
                            {{ t(`common.destination.${destination}`) }}
                        </option>
                    </select>
                </div>
            </div>

            <div class="rows">
                <label>{{ t("addHarvest.type.title") }}</label>
                <label>{{ t("addHarvest.count.title") }}</label>
                <label>{{ t("addHarvest.price.title") }}</label>
                <label><button type="button" @click="addRow">{{ t("addHarvest.btn.add") }}</button></label>
            </div>
            <div v-for="(row, index) in rows" :key="index" class="rows">
                <input v-model="row.date" type="date" required hidden />
                <div>
                    <select v-model.lazy="row.plant_type" required>
                        <option value="" selected disabled></option>
                        <option v-for="plant in PLANT_LIST" :key="plant" :value="plant">
                            {{ t(`common.type.${plant}`) }}
                        </option>
                    </select>
                </div>
                <div>
                    <input v-model.number="row.count" type="number" step="0.1" min="0" required />
                </div>
                <div>
                    <input v-model.number="row.unit_price" type="number" step="0.05" min="0" required />
                </div>
                <div>
                    <button class="remove" type="button" @click="removeRow(index)">{{ t("addHarvest.btn.remove")
                        }}</button>
                </div>
            </div>

            <button type="submit" :disabled="isLoading || rows.length === 0">
                {{ isLoading ? t("addHarvest.msg.saving") + "..." : t("addHarvest.btn.submit") }}
            </button>

            <PopUp v-if="successMsg" type="success" :msg="successMsg" @close="successMsg = null" />
            <PopUp v-if="error" type="error" :msg="error" @close="error = null" />

        </form>
    </section>
</template>
<style lang="css" scoped>
form {
    display: flex;
    flex-direction: column;
}

.globalFields div,
.rows div {
    display: flex;
    flex-direction: column;
}

.globalFields {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;

    @media (max-width: 750px) {
        grid-template-columns: 1fr;
    }
}

.remove {
    width: -webkit-fill-available;
}

.rows {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr auto;
    gap: 1rem;

    border-bottom: 1px solid var(--bg2);

    padding: 0.75rem 0;

    @media (max-width: 750px) {
        grid-template-columns: 1fr;
    }
}
</style>
