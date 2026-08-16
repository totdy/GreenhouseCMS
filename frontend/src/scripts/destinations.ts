export const DESTINATION_LIST = [
  'Slovyanskiy',
  'MultiCook',
  'Uzbecs',
  'Cheburechna',
  'Other',
] as const

export type Destination = (typeof DESTINATION_LIST)[number]

export function isDestination(value: string): value is Destination {
  return DESTINATION_LIST.some((destination) => destination === value)
}
