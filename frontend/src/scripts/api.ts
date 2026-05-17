import type {
  HarvestPayload,
  HarvestsAllResponse,
  YearlyActivityList,
  YearlyRevenueList,
  MonthlyRevenueList,
  MonthlyActivityList,
} from "@/scripts/types"

const BASE_URL = "http://192.168.1.69:8000"

export async function AddHarvests(payload: HarvestPayload) {
  const response = await fetch(`${BASE_URL}/harvests`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  })

  if (!response.ok) throw new Error(`Error: ${response.statusText}`)
  return response.json() as Promise<{ success: boolean; inserted: number }>
}

export async function GetHarvestsAll(page: number = 1): Promise<HarvestsAllResponse> {
  const response = await fetch(`${BASE_URL}/harvests/all/${page}`)

  if (!response.ok) throw new Error(`Error: ${response.statusText}`)
  return response.json()
}

export async function GetRevenueByYear(year: number): Promise<YearlyRevenueList> {
  const response = await fetch(`${BASE_URL}/revenue-by/${year}`)

  if (!response.ok) throw new Error(`Error: ${response.statusText}`)
  return response.json()
}

export async function GetRevenueByMonth(year: number, month: number): Promise<MonthlyRevenueList> {
  const response = await fetch(`${BASE_URL}/revenue-by/${year}/${month}`)

  if (!response.ok) throw new Error(`Error: ${response.statusText}`)
  return response.json()
}

export async function GetActivityByYear(year: number): Promise<YearlyActivityList> {
  const response = await fetch(`${BASE_URL}/activity/${year}`)

  if (!response.ok) throw new Error(`Error: ${response.statusText}`)
  return response.json()
}

export async function GetActivityByMonth(year: number, month: number): Promise<MonthlyActivityList> {
  const response = await fetch(`${BASE_URL}/activity/${year}/${month}`)

  if (!response.ok) throw new Error(`Error: ${response.statusText}`)
  return response.json()
}
