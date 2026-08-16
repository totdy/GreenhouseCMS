# GreenhouseCMS — agent context

Reference for AI assistants and contributors: layout, technologies, and how the pieces fit together.

## Repository layout

```
GreenhouseCMS/
├── AGENT.md                 # This file
├── README.md                # Screenshots (GitHub assets)
├── frontend/                # Vue 3 SPA (pnpm)
│   ├── index.html
│   ├── package.json
│   ├── pnpm-lock.yaml
│   ├── vite.config.ts       # Vue plugin, path alias `@` → `src/`, Vue DevTools
│   ├── tsconfig.json
│   ├── tsconfig.app.json
│   ├── tsconfig.node.json
│   ├── eslint.config.ts
│   ├── env.d.ts
│   ├── .oxlintrc.json / .oxfmtrc.json
│   ├── .gitignore / .gitattributes
│   └── src/
│       ├── main.ts          # App bootstrap: vue-router, vue-i18n, theme from localStorage
│       ├── main.css
│       ├── App.vue
│       ├── views/
│       │   ├── HomeView.vue      # Dashboard: year selector, revenue + activity charts/tables
│       │   └── HarvestView.vue   # Harvest list / add flows
│       ├── components/
│       │   ├── ActivityChart.vue / ActivityTable.vue / ActivityWeekly.vue
│       │   ├── RevenueChart.vue / RevenueTable.vue
│       │   ├── AddHarvest.vue / GetHarvest.vue
│       │   ├── PopUp.vue / ThemeToggle.vue / LocalizationSelect.vue
│       └── scripts/
│           ├── api.ts         # fetch() to FastAPI (BASE_URL in file)
│           ├── types.ts       # TS types aligned with API payloads
│           ├── plants.ts      # PLANT_TYPES registry (name → unit); single source for plant list
│           ├── destinations.ts # Destination registry, union type, and validation helper
│           ├── functions.ts   # Shared chart/date formatting helpers
│           ├── router.ts      # `/` home, `/harvest` lazy-loaded harvest view
│           └── useHarvest.ts  # Paginated harvest list composable
│       └── localization/
│           ├── index.ts
│           ├── en.json
│           └── ua.json
│   └── .vscode/
│       └── extensions.json
└── backend/                 # FastAPI API (Python 3.14, uv lockfile)
    ├── pyproject.toml
    ├── uv.lock
    ├── .python-version      # 3.14
    ├── alembic.ini          # sqlalchemy.url → sqlite:///greenhouse.db
    ├── .gitignore / .gitattributes
    ├── src/
    │   ├── main.py          # FastAPI app, CORS, routes, lifespan (create_all)
    │   ├── db.py            # SQLAlchemy engine/session, CRUD + analytics queries
    │   ├── models.py        # Declarative `Harvests` model
    │   └── schemas.py       # Pydantic request/response models
    └── migrations/          # Alembic
        ├── env.py
        ├── README
        ├── script.py.mako
        └── versions/
            ├── 380defc4f02e_drop_plant_subtype_and_note.py
            ├── 95da640e5993_removed_count_unit.py
            └── c7a8f6e4d2b1_add_harvest_destination.py
```

Runtime database file: `sqlite:///greenhouse.db` (created beside the process working directory when using defaults in `db.py` / Alembic config).

## Stack

| Area | Technology |
|------|------------|
| **Frontend language** | TypeScript |
| **Frontend framework** | Vue 3 (Composition API / SFCs) |
| **Build / dev server** | Vite 8 |
| **Routing** | Vue Router 5 |
| **i18n** | Vue I18n 11 (locales: `en`, `ua`; persisted in `localStorage`) |
| **Charts** | Chart.js 4 + chartjs-plugin-datalabels |
| **HTTP** | Native `fetch` (no Axios) |
| **Lint / format** | ESLint 10 + Vue/TS plugins, Oxlint, Oxfmt |
| **Type-check** | vue-tsc |
| **Package manager** | pnpm (engines: Node ^20.19 or >=22.12) |
| **Backend language** | Python (project pins **3.14** via `.python-version`) |
| **API** | FastAPI |
| **Server** | Uvicorn |
| **ORM / DB access** | SQLAlchemy 2.x |
| **Migrations** | Alembic |
| **Validation / API models** | Pydantic (via FastAPI) |
| **Database** | SQLite (`greenhouse.db`) |
| **Dependency lock** | uv (`uv.lock`) |

## Plant registry (`frontend/src/scripts/plants.ts`)

All supported plant types and their display units live in one object. **Do not** duplicate plant names in components.

```ts
export const PLANT_TYPES = {
  Tomato: { unit: "kg" },
  TomatoCherry: { unit: "box" },
  // ...
} as const

export type PlantType = keyof typeof PLANT_TYPES
export const PLANT_LIST = Object.keys(PLANT_TYPES) as PlantType[]
export function isPlantType(value: string): value is PlantType
export function getPlantUnit(plant: PlantType): CountUnit
```

**Adding a plant** requires:

1. Entry in `PLANT_TYPES` (key = API `plant_type` string, e.g. `TomatoCherry`).
2. i18n labels in `en.json` and `ua.json` under `common.type.<PlantType>` (e.g. `common.type.TomatoCherry`).

Units (`kg` | `box` | `bunch` | `piece`) are **frontend-only**; the backend does not store `count_unit`. UI resolves units via `getPlantUnit(plant_type)`.

`types.ts` imports `PlantType` for harvest and activity shapes.

## Destination registry (`frontend/src/scripts/destinations.ts`)

Harvest destinations have canonical API/DB values in `DESTINATION_LIST`: `Slovyanskiy`, `MultiCook`, `Uzbecs`, `Cheburechna`, and `Other`. `Destination` is the corresponding TypeScript union and `isDestination()` validates form values before submission. Do not duplicate this list in components.

Localized display labels live under `common.destination.<Destination>` in both locale files. The add-harvest form has one required global destination selector, like the global harvest date; changing it updates every row and newly added rows inherit it. The database migration assigns `Other` only to rows created before the field existed.

## Backend API

| Method | Path | Response wrapper | Notes |
|--------|------|------------------|-------|
| `POST` | `/harvests` | `{ success, inserted }` | Body: `{ data: HarvestIn[] }` |
| `PUT` | `/harvests/{id}` | `{ success }` | Single harvest update |
| `GET` | `/harvests/all/{page}` | `HarvestsAllResponse` | 15 rows per page |
| `GET` | `/revenue-by/{year}` | `{ data: YearlyRevenueItem[] }` | `{ month, revenue }` per row |
| `GET` | `/revenue-by/{year}/{month}` | `{ data: MonthlyRevenueItem[] }` | `{ date, revenue }` per day |
| `GET` | `/activity/{year}` | `{ data: YearlyActivityItem[] }` | `{ month, plant_type, count }` |
| `GET` | `/activity/{year}/{month}` | `{ data: MonthlyActivityItem[] }` | `{ date, plant_type, count }` per day |
| `GET` | `/activity-weekly/{year}` | `{ data: WeeklyActivityItem[] }` | `{ week, plant_type, count }` |

**Harvest fields** (`HarvestIn` / DB): `date`, `plant_type`, `destination`, `count`, `unit_price`. `destination` is required for new and updated harvests and, like `plant_type`, is represented as an unconstrained string by the backend schema. `HarvestOut` additionally includes `id` and `created_at`.

CORS is open (`allow_origins=["*"]`) for local/dev. The frontend sends requests to the relative `/api` path configured in `frontend/src/scripts/api.ts`.

## Frontend dashboard (`HomeView.vue`)

- Loads yearly revenue and activity for the selected year via `GetRevenueByYear` / `GetActivityByYear`.
- Passes `year` into chart components for month drill-down.

**RevenueChart** — single line chart of 12 monthly totals; click a month → `GetRevenueByMonth(year, month)` → popup with daily revenue.

**ActivityChart** — single line chart for one selected plant (`PLANT_LIST` select); click a month → `GetActivityByMonth(year, month)` → popup filtered to that plant’s daily counts.

**RevenueTable** — yearly sum and average monthly revenue.

**ActivityTable** — yearly totals per plant (aggregation logic lives in the component); units from `getPlantUnit`.

Keep chart/table **transform logic inside components**, not in `types.ts` helpers.

## Frontend API client (`api.ts`)

Exported functions mirror backend routes: `AddHarvests`, `GetHarvestsAll`, `GetRevenueByYear`, `GetRevenueByMonth`, `GetActivityByYear`, `GetActivityByMonth`, `GetActivityByWeek`.

`BASE_URL` is the relative `/api`; nginx proxies that path to FastAPI, so the client works on localhost, LAN hosts, and deployed hosts without a hard-coded origin.

## Common commands

**Frontend** (from `frontend/`):

- `pnpm install`
- `pnpm dev` — Vite dev server
- `pnpm build` — type-check + production build
- `pnpm lint` — oxlint + eslint

**Backend** (from `backend/`): use `uv` per `uv.lock` / `pyproject.toml` (e.g. `uv sync`, `uv run uvicorn src.main:app --reload` — adjust module path if your cwd differs).

Apply pending database migrations manually before starting the updated API against an existing database: `uv run alembic upgrade head`. Docker startup does not run Alembic automatically; `Base.metadata.create_all()` creates missing tables but does not upgrade existing ones.
