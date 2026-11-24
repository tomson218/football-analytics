# Frontend — Football Analytics

React 19 + TypeScript + Vite web application for predicting the probability that a home football team will not lose a match based on bookmaker odds.

For full project details, see [README.md](../README.md).

## Prediction Form

The main component is a form with 6 fields: 5 bookmaker odds fields and 1 Asian Handicap (HandiSize) field. After submission, the form maps camelCase field names to snake_case and sends the values to the FastAPI backend, which uses a trained CatBoost 6-feature model to predict the probability of the home team not losing (win or draw).

**Features:**

- **Zod validation** — Each field has individual min/max ranges matching the backend (e.g. oddHome: 1.04–26.13, handiSize: -3.5–2.8). Default values are set to the minimum.
- **Feature importance** — Displayed next to each field, fetched dynamically from the API.
- **camelCase → snake_case transformation** — Form data is mapped to backend field names before sending.
- **Loading state** — Spinner shown while waiting for the prediction.
- **Result display** — Shows predicted probability, implied probability, and whether it's a value bet.

## Tech Stack

| Technology | Purpose |
|---|---|
| React 19 | UI framework |
| TypeScript | Type safety |
| Vite | Build tool and dev server |
| Tailwind CSS | Utility-first styling |
| shadcn/ui (Radix UI) | Accessible UI primitives |
| TanStack Query | Server state management (queries + mutations) |
| React Hook Form | Form state management |
| Zod v4 | Schema validation |
| Axios | HTTP client |
| Lucide React | Icons |

## Folder Structure

```
frontend/src/
├── api/                        # HTTP client and TanStack Query hooks
│   ├── index.ts                # Axios instance with base URL from VITE_API_URL
│   ├── mutations/              # Mutation hooks
│   │   └── use-predict-home-no-lose.ts  # POST /predict/home-no-lose
│   └── queries/                # Query hooks
│       └── use-feature-importance.ts     # GET /predict/feature-importance
├── components/
│   ├── prediction/             # Prediction form
│   │   └── PredictionForm.tsx  # Main form component with 6 odds fields
│   └── ui/                     # shadcn/ui primitives
│       ├── Button.tsx
│       ├── Card.tsx
│       ├── Input.tsx
│       ├── Label.tsx
│       └── Spinner.tsx
├── schemas/                    # Zod validation schemas
│   └── odds.ts                 # Odds form schema (individual ranges per field: oddHome 1.04–26.13, handiSize -3.5–2.8, etc.)
├── types/                      # TypeScript types (one file per type)
│   ├── country.ts
│   ├── division.ts
│   ├── feature-importance.ts   # Pick<Match, odds fields>
│   ├── historical-elo.ts
│   ├── match.ts
│   ├── prediction-response.ts  # API response type
│   └── team.ts
├── lib/                        # Utility functions
│   └── utils.ts                # cn() helper (clsx + tailwind-merge)
├── App.tsx                     # Root component (PredictionForm)
├── main.tsx                    # Entry point (QueryClientProvider)
└── index.css                   # Tailwind + shadcn CSS variables
```

## Quick Start

### Docker

```bash
docker compose up -d --build
# Frontend available at http://localhost:5173
```

### Local Development

```bash
cd frontend
npm install
npm run dev
```

The dev server runs on `http://localhost:5173`. Make sure the backend API is running on the URL specified by `VITE_API_URL` in the root `.env` file.

### Build for Production

```bash
npm run build
# Output in dist/
```

## Environment Variables

| Variable | Description |
|---|---|
| `VITE_API_URL` | Backend API base URL (e.g., `http://localhost:8080`) |

Set in the root `.env` file. Docker Compose passes it to the frontend container automatically.
