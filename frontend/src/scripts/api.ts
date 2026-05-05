import type { HarvestPayload, ActivityPivotResponse, HarvestsAllResponse, RevenueByDateResponse } from "@/scripts/types"

const BASE_URL = "http://192.168.1.69:8000"

export async function AddHarvests(payload: HarvestPayload) {
    const response = await fetch(`${BASE_URL}/harvests`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    })

    if (!response.ok) throw new Error(`Error: ${response.statusText}`)
    return response.json()
}

export async function GetHarvestsAll(page: number = 1): Promise<HarvestsAllResponse> {
    const response = await fetch(`${BASE_URL}/harvests/all/${page}`)

    if (!response.ok) throw new Error(`Error: ${response.statusText}`)
    return response.json()
}

export async function GetRevenueByDate(chartYear: number): Promise<RevenueByDateResponse> {
    const response = await fetch(`${BASE_URL}/revenue-by-date/${chartYear}`)

    if (!response.ok) throw new Error(`Error: ${response.statusText}`)
    return response.json()
}

export async function GetActivityByYear(year: number): Promise<ActivityPivotResponse> {
    const response = await fetch(`${BASE_URL}/activity/${year}`)

    if (!response.ok) throw new Error(`Error: ${response.statusText}`)
    return response.json()
}