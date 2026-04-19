export interface HarvestItem {
  date: string
  plant_type: string
  plant_subtype: string
  count: number
  count_unit: string
  unit_price: number
  note?: string
}

export interface HarvestPayload {
  data: HarvestItem[]
}