import type { HarvestPayload } from "@/scripts/types"

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

export async function GetRevenueByDate() {
    const response = await fetch(`${BASE_URL}/harvests/revenue-by-date`);
    
    if (!response.ok) throw new Error(`Error: ${response.statusText}`)
    return response.json()
}