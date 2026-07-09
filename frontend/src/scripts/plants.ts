export type CountUnit = "kg" | "box" | "bunch"

export const PLANT_TYPES = {
  Tomato: { unit: "kg" },
  TomatoCherry: { unit: "box" },
  Cucumber: { unit: "kg" },
  BellPepper: { unit: "kg" },
  Garlic: { unit: "bunch" },
  Dill: { unit: "bunch" },
  Onion: { unit: "bunch" },
  Parsley: { unit: "bunch" },
  Eggplant: { unit: "kg" },
  Lovage: { unit: "bunch" },
  Sorrel: { unit: "bunch" },
  Mint: { unit: "bunch" },
  Radish: { unit: "box" },
  Coriander: { unit: "bunch" },
  Basil: { unit: "bunch" },
  Bouquet: { unit: "bunch" },
  Zucchini: { unit: "kg" },
  RedBeet: { unit: "kg" },
  SaltedCucumbers: { unit: "kg" },
} as const satisfies Record<string, { unit: CountUnit }>

export type PlantType = keyof typeof PLANT_TYPES

export const PLANT_LIST = Object.keys(PLANT_TYPES) as PlantType[]

export const DEFAULT_PLANT: PlantType = "Cucumber"

export function isPlantType(value: string): value is PlantType {
  return value in PLANT_TYPES
}

export function getPlantUnit(plant: PlantType): CountUnit {
  return PLANT_TYPES[plant].unit
}
