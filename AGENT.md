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
│       │   ├── HomeView.vue      # Dashboard: revenue + activity charts/tables
│       │   └── HarvestView.vue   # Harvest list / add / edit flows
│       ├── components/
│       │   ├── ActivityChart.vue / ActivityTable.vue
│       │   ├── RevenueChart.vue / RevenueTable.vue
│       │   ├── AddHarvest.vue / GetHarvest.vue
│       │   ├── PopUp.vue / ThemeToggle.vue / LocalizationSelect.vue
│       └── scripts/
│           ├── api.ts         # fetch() to FastAPI (BASE_URL in file)
│           ├── types.ts       # Shared TS types aligned with API payloads
│           ├── router.ts      # `/` home, `/harvest` lazy-loaded harvest view
│           └── useHarvest.ts  # Harvest-related composable logic
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

## Backend API (summary)

- `POST /harvests` — bulk insert (`HarvestPayload`)
- `PUT /harvests/{id}` — update one harvest
- `GET /harvests/all/{page}` — paginated list (15 per page)
- `GET /revenue-by-date/{year}` — daily revenue aggregates
- `GET /activity/{year}` — monthly totals pivoted by plant type

CORS is open (`allow_origins=["*"]`) for local/dev use. The frontend API base URL is set in `frontend/src/scripts/api.ts` (currently a LAN IP — change for your environment).

## Common commands

**Frontend** (from `frontend/`):

- `pnpm install`
- `pnpm dev` — Vite dev server
- `pnpm build` — type-check + production build
- `pnpm lint` — oxlint + eslint

**Backend** (from `backend/`): use `uv` per `uv.lock` / `pyproject.toml` (e.g. `uv sync`, `uv run uvicorn src.main:app --reload` — adjust module path if your cwd differs).