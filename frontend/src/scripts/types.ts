export interface HarvestItem {
  date: string
  plant_type: string
  count: number
  count_unit: string
  unit_price: number
}

export interface HarvestPayload {
  data: HarvestItem[]
}

export interface ActivitySeries {
  plant_type: string
  count: number[]
}

export interface ActivityPivotResponse {
  data: ActivitySeries[]
}

export interface RevenueByDateItem {
  date: string
  revenue: number
}

export interface RevenueByDateResponse {
  data: RevenueByDateItem[]
}

export interface RecentActivityItem {
  id: number
  date: string
  plant_type: string
  count: number
  count_unit: string
  unit_price: number
  created_at: string
}

export interface RecentActivityResponse {
  data: RecentActivityItem[]
}