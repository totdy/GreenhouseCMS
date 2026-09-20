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
const validationModal = ref<HTMLDialogElement | null>(null)

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

function openValidationModal() {
    validationModal.value?.showModal()
}

function closeValidationModal() {
    validationModal.value?.close()
}

async function confirmSubmit() {
    closeValidationModal()
    await handleSubmit()
}
</script>
<template>
    <section>
        <form @submit.prevent="openValidationModal">
            <h2>{{ t("addHarvest.title") }}
                <button type="submit" :disabled="isLoading || rows.length === 0">
                    {{ isLoading ? t("addHarvest.msg.saving") + "..." : t("addHarvest.btn.submit") }}
                </button>
            </h2>
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
                <label></label>
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

            <button type="button" @click="addRow">{{ t("addHarvest.btn.add") }}</button>

            <PopUp v-if="successMsg" type="success" :msg="successMsg" @close="successMsg = null" />
            <PopUp v-if="error" type="error" :msg="error" @close="error = null" />

        </form>

        <dialog ref="validationModal" class="validationModal">
            <div class="modalHeader">
                <h3>{{ t("addHarvest.validation.title") }}</h3>
                <button type="button" class="close" :aria-label="t('addHarvest.validation.close')" @click="closeValidationModal">
                    ×
                </button>
            </div>

            <dl>
                <div>
                    <dt>{{ t("addHarvest.date.title") }}</dt>
                    <dd>{{ globalDate }}</dd>
                </div>
                <div>
                    <dt>{{ t("addHarvest.destination.title") }}</dt>
                    <dd>{{ globalDestination ? t(`common.destination.${globalDestination}`) : "" }}</dd>
                </div>
            </dl>

            <h4>{{ t("addHarvest.validation.products") }}</h4>
            <ul>
                <li v-for="(row, index) in rows" :key="index">
                    {{ t(`common.type.${row.plant_type}`) }} — {{ row.count }} - €{{ row.unit_price }}
                </li>
            </ul>

            <div class="modalActions">
                <button class="cancel" type="button" @click="closeValidationModal">{{ t("addHarvest.validation.cancel") }}</button>
                <button class="confirm" type="button" :disabled="isLoading" @click="confirmSubmit">
                    {{ isLoading ? t("addHarvest.msg.saving") + "..." : t("addHarvest.validation.confirm") }}
                </button>
            </div>
        </dialog>
    </section>
</template>
<style lang="css" scoped>
h2 {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

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

    border-bottom: 1px solid var(--border);

    padding: 0.75rem 0;

    @media (max-width: 750px) {
        grid-template-columns: 1fr;
    }
}

.validationModal {
    width: min(100% - 2rem, 30rem);
    border: none;
    border-radius: 0.5rem;
    padding: 1.25rem;
    background: var(--bg);
    margin: auto;
}

.validationModal::backdrop {
    background: var(--secondary05);
}

.modalHeader,
.modalActions {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
}

.close {
    width: auto;
    font-size: 1.5rem;
    line-height: 1;
}

dl {
    margin: 1.25rem 0;
}

dl div {
    display: grid;
    grid-template-columns: 1fr 2fr;
    gap: 1rem;
    padding: 0.5rem 0;
    border-bottom: 1px solid var(--border);
}

ul {
    margin: 0.75rem 0 1.25rem;
    padding-left: 1.25rem;
}
</style>
