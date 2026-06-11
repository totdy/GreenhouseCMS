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
│       │   ├── ActivityChart.vue / ActivityTable.vue
│       │   ├── RevenueChart.vue / RevenueTable.vue
│       │   ├── AddHarvest.vue / GetHarvest.vue
│       │   ├── PopUp.vue / ThemeToggle.vue / LocalizationSelect.vue
│       └── scripts/
│           ├── api.ts         # fetch() to FastAPI (BASE_URL in file)
│           ├── types.ts       # TS types aligned with API payloads; uses PlantType from plants.ts
│           ├── plants.ts      # PLANT_TYPES registry (name → unit); single source for plant list
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
            └── 380defc4f02e_drop_plant_subtype_and_note.py
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
  Tomatocherry: { unit: "box" },
  // ...
} as const

export type PlantType = keyof typeof PLANT_TYPES
export const PLANT_LIST = Object.keys(PLANT_TYPES) as PlantType[]
export function isPlantType(value: string): value is PlantType
export function getPlantUnit(plant: PlantType): CountUnit
```

**Adding a plant** requires:

1. Entry in `PLANT_TYPES` (key = API `plant_type` string, e.g. `Tomatocherry`).
2. i18n labels in `en.json` and `ua.json` under `common.type.<lowercase>` (e.g. `tomatocherry`).

Units (`kg` | `box` | `bunch`) are **frontend-only**; the backend stores `plant_type`, `count`, and `unit_price` but not `count_unit`. UI resolves units via `getPlantUnit(plant_type)`.

`types.ts` imports `PlantType` for harvest and activity shapes.

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

**Harvest fields** (`HarvestIn` / DB): `date`, `plant_type`, `count`, `unit_price`.

CORS is open (`allow_origins=["*"]`) for local/dev. The frontend API base URL is set in `frontend/src/scripts/api.ts` (currently a LAN IP — change for your environment).

## Frontend dashboard (`HomeView.vue`)

- Loads yearly revenue and activity for the selected year via `GetRevenueByYear` / `GetActivityByYear`.
- Passes `year` into chart components for month drill-down.

**RevenueChart** — single line chart of 12 monthly totals; click a month → `GetRevenueByMonth(year, month)` → popup with daily revenue.

**ActivityChart** — single line chart for one selected plant (`PLANT_LIST` select); click a month → `GetActivityByMonth(year, month)` → popup filtered to that plant’s daily counts.

**RevenueTable** — yearly sum and average monthly revenue.

**ActivityTable** — yearly totals per plant (aggregation logic lives in the component); units from `getPlantUnit`.

Keep chart/table **transform logic inside components**, not in `types.ts` helpers.

## Frontend API client (`api.ts`)

Exported functions mirror backend routes: `AddHarvests`, `GetHarvestsAll`, `GetRevenueByYear`, `GetRevenueByMonth`, `GetActivityByYear`, `GetActivityByMonth`.

## Common commands

**Frontend** (from `frontend/`):

- `pnpm install`
- `pnpm dev` — Vite dev server
- `pnpm build` — type-check + production build
- `pnpm lint` — oxlint + eslint

**Backend** (from `backend/`): use `uv` per `uv.lock` / `pyproject.toml` (e.g. `uv sync`, `uv run uvicorn src.main:app --reload` — adjust module path if your cwd differs).
