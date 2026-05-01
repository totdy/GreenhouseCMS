import type { HarvestPayload, ActivityResponse, RecentActivityResponse, RevenueByDateResponse } from "@/scripts/types"

const BASE_URL = "http://192.168.1.69:8000"

export async function addHarvests(payload: HarvestPayload) {
    const response = await fetch(`${BASE_URL}/harvests`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
    })

    if (!response.ok) throw new Error(`Error: ${response.statusText}`)
    return response.json()
}

export async function GetRevenueByDate(chartYear: number): Promise<RevenueByDateResponse> {
    const response = await fetch(`${BASE_URL}/harvests/revenue-by-date/${chartYear}`)

    if (!response.ok) throw new Error(`Error: ${response.statusText}`)
    return response.json()
}

export async function GetActivityByYear(year: number): Promise<ActivityResponse> {
    const response = await fetch(`${BASE_URL}/harvests/activity/${year}`)

    if (!response.ok) throw new Error(`Error: ${response.statusText}`)
    return response.json()
}

export async function GetRecentActivity(limit: number = 10): Promise<RecentActivityResponse> {
    const response = await fetch(`${BASE_URL}/harvests/recent?limit=${limit}`)

    if (!response.ok) throw new Error(`Error: ${response.statusText}`)
    return response.json()
}