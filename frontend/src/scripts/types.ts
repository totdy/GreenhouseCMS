export interface HarvestIn {
  date: string
  plant_type: string
  count: number
  count_unit: string
  unit_price: number
}

export interface HarvestOut extends HarvestIn {
  id: number
  created_at: string
}

export interface HarvestPayload {
  data: HarvestIn[]
}

export interface ActivitySeries {
  plant_type: string
  count: number[]
  count_unit: string
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

export interface HarvestsAllResponse {
  data: HarvestOut[]
  total: number
  page: number
  total_pages: number
}