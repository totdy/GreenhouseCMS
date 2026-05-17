import type { PlantType } from "./plants"

export interface HarvestIn {
  date: string
  plant_type: PlantType
  count: number
  unit_price: number
}

export interface HarvestOut extends HarvestIn {
  id: number
  created_at: string
}

export interface HarvestPayload {
  data: HarvestIn[]
}

export interface YearlyRevenueItem {
  month: number
  revenue: number
}

export interface YearlyRevenueList {
  data: YearlyRevenueItem[]
}

export interface MonthlyRevenueItem {
  date: string
  revenue: number
}

export interface MonthlyRevenueList {
  data: MonthlyRevenueItem[]
}

export interface YearlyActivityItem {
  month: number
  plant_type: PlantType
  count: number
}

export interface YearlyActivityList {
  data: YearlyActivityItem[]
}

export interface MonthlyActivityItem {
  date: string
  plant_type: PlantType
  count: number
}

export interface MonthlyActivityList {
  data: MonthlyActivityItem[]
}

export interface HarvestsAllResponse {
  data: HarvestOut[]
  total: number
  page: number
  total_pages: number
}
