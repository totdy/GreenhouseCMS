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