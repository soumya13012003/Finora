# Finora — AI-Powered Financial Intelligence Platform

> Upload corporate annual reports as PDFs. Get structured dashboards, health scores, side-by-side comparisons, and a RAG-powered AI chat — in under two minutes.

Built with **FastAPI** · **React 19** · **Groq LLM** · **ChromaDB** · **Tailwind CSS v4** · **shadcn/ui**

---

## ✨ Features

### 📊 AI-Powered Dashboard
- **Financial Health Score** — 1–10 gauge computed from revenue, margins, debt, and growth signals
- **Key Metrics & Ratios** — Auto-extracted KPIs with trend indicators and color-coded assessments
- **Revenue Breakdown** — Segment-level pie/bar charts with percentage and absolute amounts
- **Executive Summary** — Board-level narrative synthesized from the full report
- **Strategic Focus & Risk Analysis** — AI-identified initiatives and risk factors

### 📑 Smart PDF Processing
- Scores every page for financial signal density using keyword lexicons, currency/percentage detection, and section classification
- Selectively extracts tables only from financially relevant pages
- Aggressively filters low-value content (TOC, boilerplate, legal disclaimers)
- Processes PDFs up to **600 pages** in under **60 seconds**

### 🔀 Multi-Company Comparison
- Upload up to **3 annual reports** side-by-side
- Compare KPIs, margins, and growth trajectories across competitors
- AI-generated comparative analysis with strategic insights

### 💬 RAG-Powered AI Chat
- Ask natural language questions about any uploaded report
- Retrieval-Augmented Generation grounded in actual document context
- Streaming SSE responses with full dashboard context awareness

### 🎨 Cinematic UI
- Animated landing page with gradient orbs, light streaks, and typewriter hero heading
- Dark-first glassmorphism design with full light-mode support
- Hover micro-interactions — lift, shimmer sweep, border glow, and icon scale
- Responsive layout with mobile sidebar support

### 🔐 Authentication & Security
- JWT-based auth (pure stdlib — zero dependency)
- Per-user data isolation across reports, chat, and vector collections
- SHA-256 + salt password hashing

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      Frontend (React 19)                │
│  Landing Page → Auth → Upload → Dashboard → Chat       │
│  Vite 7 · TanStack Router · Tailwind v4 · shadcn/ui    │
└────────────────────────┬────────────────────────────────┘
                         │  REST API + SSE
┌────────────────────────▼────────────────────────────────┐
│                     Backend (FastAPI)                    │
│                                                         │
│  ┌─────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │  Auth   │  │   Reports    │  │      Chat         │  │
│  │ Router  │  │   Router     │  │     Router        │  │
│  └────┬────┘  └──────┬───────┘  └────────┬──────────┘  │
│       │              │                   │              │
│       │    ┌─────────▼──────────┐        │              │
│       │    │  AI Pipeline       │        │              │
│       │    │  ┌───────────────┐ │   ┌────▼────────┐    │
│       │    │  │ Map-Reduce    │ │   │ RAG         │    │
│       │    │  │ LLM Analysis  │ │   │ Retrieval   │    │
│       │    │  └───────────────┘ │   └─────────────┘    │
│       │    │  ┌───────────────┐ │                       │
│       │    │  │ Vectorization │ │                       │
│       │    │  └───────────────┘ │                       │
│       │    └────────────────────┘                       │
│  ┌────▼────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ SQLite/ │  │  ChromaDB    │  │   Redis           │  │
│  │ Postgres│  │  (Vectors)   │  │   (Progress)      │  │
│  └─────────┘  └──────────────┘  └───────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

### AI Pipeline Flow

1. **Phase 1 — Intelligent Financial Extraction**
   - Page scoring by financial signal density
   - Selective table extraction from relevant pages
   - Boilerplate filtering → prioritized LLM context (~150K chars) + RAG context (~300K chars)

2. **Phase 2 — Parallel Downstream Processing**
   - **Pipeline A (Map-Reduce):** Dynamic 1–6 map agents extract structured data, reduce agent synthesizes into `ReportInsights`
   - **Pipeline B (RAG):** Financial-aware chunking → ChromaDB embedding with score-boosted retrieval

3. **Phase 3 — Dashboard & Chat**
   - Structured insights feed the React dashboard
   - Chat uses RAG retrieval + dashboard context for grounded, streaming responses

---

## 🚀 Quick Start

### Prerequisites

| Tool | Version |
|---|---|
| **Python** | 3.12+ |
| **Node.js** | 20+ |
| **Groq API Key** | [Get one here](https://console.groq.com/) |

### 1. Clone the repository

```bash
git clone https://github.com/soumya13012003/Finora.git
cd Finora
```

### 2. Backend Setup

```bash
cd Back/finora-backend-main

# Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env — set GROQ_API_KEY at minimum
```

**Start the backend:**

```bash
uvicorn main:app --reload --port 8000
```

- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### 3. Frontend Setup

```bash
cd Front/finora-frontend-main

npm install
npm run dev
```

Open `http://localhost:5173` — API calls are automatically proxied to `localhost:8000`.

---

## 🔌 API Reference

```
POST /api/auth/register          →  Create account
POST /api/auth/login             →  Get JWT token
GET  /api/auth/me                →  Current user profile + usage totals
GET  /api/auth/usage             →  Detailed token usage analytics

POST /api/reports/upload         →  Upload up to 3 PDF files
POST /api/reports/process/:id    →  Run AI extraction pipeline
GET  /api/reports/progress/:id   →  Real-time progress (Redis-backed)
GET  /api/reports/set/:id        →  Fetch report set + insights
GET  /api/reports/history        →  Past report sets
GET  /api/reports/compare/:id    →  Side-by-side multi-company comparison
GET  /api/reports/compare_ai/:id →  AI-generated comparative analysis (cached)
DELETE /api/reports/set/:id      →  Delete a report set + cleanup

POST /api/chat/session           →  SSE streaming chat with RAG context
POST /api/chat/turn              →  Persist a chat turn
POST /api/chat/messages          →  Load chat history
POST /api/chat/clear             →  Clear chat history

GET  /health                     →  Health check
```

---

## ⚙️ Environment Variables

### Backend (`Back/finora-backend-main/.env`)

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | — | **Required.** Your Groq API key |
| `AI_MODEL` | `openai/gpt-oss-120b` | Groq model for extraction |
| `DATABASE_URL` | `sqlite:///./finora.db` | SQLite (dev) or PostgreSQL (prod) |
| `REDIS_URL` | _(empty)_ | Redis for progress tracking; empty = in-memory fallback |
| `JWT_SECRET` | dev-default | Change to a random 64-char string in production |
| `JWT_EXPIRY_HOURS` | `72` | Token lifetime |
| `ALLOWED_ORIGINS` | localhost | Comma-separated frontend URLs |
| `MAX_FILE_SIZE_MB` | `25` | PDF upload size limit |
| `MAX_FILES_PER_SET` | `3` | Max PDFs per upload set |
| `MAX_MAP_CONCURRENCY` | `4` | Max concurrent LLM map agents |
| `MAX_GLOBAL_LLM_CONCURRENCY` | `6` | Global LLM call concurrency limit |
| `EXTRACTION_WORKERS` | `3` | Process pool workers for PDF extraction |

### Frontend (`Front/finora-frontend-main/.env`)

| Variable | Required | Description |
|---|---|---|
| `VITE_API_BASE_URL` | Production only | Backend URL (baked at build time) |

> **Note:** No `.env` is needed for local frontend development — the Vite dev server proxies `/api/*` to `localhost:8000` automatically.

---

## 📁 Project Structure

```
Finora/
├── README.md                          # This file
├── .gitignore
│
├── Back/finora-backend-main/          # FastAPI Backend
│   ├── main.py                        # App entry point, lifespan, middleware
│   ├── config.py                      # Centralized env config
│   ├── database.py                    # SQLAlchemy engine, session, ORM models
│   ├── models.py                      # Pydantic request/response schemas
│   ├── ai_schema.py                   # LLM structured output schemas
│   ├── logger.py                      # Structured JSON logging
│   ├── requirements.txt               # Python dependencies
│   ├── Dockerfile                     # Multi-stage production container
│   ├── routers/
│   │   ├── auth.py                    # JWT auth, registration, usage analytics
│   │   ├── reports.py                 # Upload, process, history, compare
│   │   └── chat.py                    # SSE streaming chat with RAG
│   └── services/
│       ├── financial_extractor.py     # Intelligent PDF extraction engine
│       ├── table_extractor.py         # PDF table-to-markdown helper
│       ├── rag.py                     # Financial-aware chunking + ChromaDB
│       └── progress_tracker.py        # Redis-backed progress tracking
│
└── Front/finora-frontend-main/        # React Frontend
    ├── index.html
    ├── package.json
    ├── vite.config.ts
    ├── tsconfig.json
    ├── public/
    │   └── favicon.svg
    └── src/
        ├── main.tsx                   # App entry point
        ├── router.tsx                 # TanStack Router config
        ├── styles.css                 # Tailwind CSS, theme tokens, animations
        ├── components/
        │   ├── dashboard/
        │   │   ├── AuthPage.tsx       # Split-panel login/register
        │   │   ├── ChatSection.tsx    # SSE streaming chat with markdown
        │   │   ├── ComparisonView.tsx # Multi-company comparison + AI insights
        │   │   ├── HealthGauge.tsx    # Animated financial health gauge
        │   │   ├── HistoryMenu.tsx    # Past report sets with reload/delete
        │   │   ├── KeyRatiosStrip.tsx # Ratio cards with assessment colors
        │   │   ├── Overview.tsx       # Main dashboard layout
        │   │   ├── ProgressIndicator.tsx # Animated pipeline progress bar
        │   │   ├── Scorecards.tsx     # Key metric cards with trend gradients
        │   │   ├── Sidebar.tsx        # Desktop + mobile navigation
        │   │   ├── TacticalUI.tsx     # Summary + strategy + risk panels
        │   │   └── UploadSection.tsx  # Drag-and-drop PDF staging
        │   ├── landing/
        │   │   └── LandingPage.tsx    # Cinematic hero with animations
        │   ├── theme/                 # Dark/light mode provider + toggle
        │   └── ui/                    # shadcn/ui components + custom UI
        ├── lib/
        │   ├── api.ts                 # All backend API calls
        │   ├── types.ts              # Shared TypeScript types
        │   └── utils.ts              # Tailwind class merge helper
        └── routes/                    # TanStack Router file-based routes
```

---

## 🛠️ Tech Stack

### Backend

| Library | Purpose |
|---|---|
| **FastAPI** | Async web framework |
| **SQLAlchemy** | ORM — SQLite (dev), PostgreSQL (prod) |
| **ChromaDB** | Vector database for RAG |
| **Groq** | LLM API (async, streaming) |
| **PyMuPDF** | Fast PDF text extraction |
| **pdfplumber** | PDF table extraction |
| **langchain-text-splitters** | Financial semantic chunking |
| **json-repair** | Recovery of malformed LLM JSON |
| **Redis** | Production progress tracking |
| **pg8000** | PostgreSQL driver (Cloud SQL) |

### Frontend

| Library | Purpose |
|---|---|
| **React 19** | UI framework |
| **Vite 7** | Build tool and dev server |
| **TanStack Router** | Type-safe file-based routing |
| **Tailwind CSS v4** | Utility-first styling |
| **shadcn/ui** | Component library (Radix UI + Tailwind) |
| **Recharts** | Chart components (bar, line, pie, area) |
| **react-markdown** | Chat message rendering |
| **lucide-react** | Icon library |

---

## 🐳 Production Deployment

The backend includes a Dockerfile optimized for **Google Cloud Run**:

```bash
# Build the container
docker build -t finora-backend ./Back/finora-backend-main

# Run locally
docker run -p 8080:8080 -e GROQ_API_KEY=your_key_here finora-backend
```

The frontend builds to a static `dist/` folder deployable on any static host:

```bash
cd Front/finora-frontend-main
VITE_API_BASE_URL=https://api.your-domain.com npm run build
# Serve with nginx, Vercel, Netlify, S3+CloudFront, etc.
```

---

## 📈 Performance Targets

| Metric | Target | How |
|---|---|---|
| Concurrent PDFs | 3 | Global asyncio semaphore + horizontal scaling |
| Max PDF size | 600 pages | Intelligent page filtering + tiered detail levels |
| Extraction speed | <60s for 600pp | Selective table extraction, fast text scoring |
| End-to-end latency | <2 min | Parallel map-reduce + vectorization pipelines |
| Progress accuracy | Real steps | Redis-backed tracking with 10 granular pipeline stages |

---

## 📄 License

MIT
