# Who'sThere

A social location check-in web app. Built with **FastAPI** (Python) + **Plain HTML/JS** + **Supabase** + **PostgreSQL**.

---

## Quickstart

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/checkin-app.git
cd checkin-app

# 2. Install everything & create your .env
make install

# 3. Fill in your keys
#    Edit backend/.env (Supabase + Google Places)

# 4. Fill in frontend config
#    Edit frontend/js/config.js (Supabase URL + anon key)

# 5. Run migrations
make upgrade

# 6. Start the app (two terminals)
make dev         # terminal 1 — FastAPI on :8000
make frontend    # terminal 2 — Frontend on :5500

# Optional: seed with sample data
make seed
```

Open [http://localhost:5500](http://localhost:5500)
API docs at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## All Commands

```
make install      Install Python deps, create .env
make dev          Start FastAPI backend (hot reload)
make frontend     Serve frontend on :5500
make dev-all      Start both in parallel
make upgrade      Apply DB migrations
make migrate      Create a new migration  (msg="your message")
make downgrade    Roll back one migration
make reset        Drop + re-migrate (⚠ destroys data)
make seed         Insert sample data
make test         Run test suite
make test-cov     Run tests + coverage report
make lint         Run ruff linter
make format       Auto-format with ruff
make check        Lint + type check (used in CI)
make docker-up    Run everything via Docker Compose
make clean        Remove caches
```

---

## Project Structure

```
checkin-app/
├── backend/
│   ├── app/
│   │   ├── main.py           FastAPI entry point
│   │   ├── config.py         Settings from .env
│   │   ├── api/              Route handlers
│   │   ├── models/           SQLAlchemy models
│   │   ├── schemas/          Pydantic request/response
│   │   ├── services/         Business logic
│   │   ├── db/               Session + seed
│   │   └── middleware/       JWT auth
│   ├── alembic/              DB migrations
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── index.html            Feed
│   ├── checkin.html          Check-in flow
│   ├── places.html           Browse places
│   ├── profile.html          User profile
│   ├── css/main.css
│   └── js/
│       ├── config.js         ← set your keys here
│       ├── api.js            All fetch() calls
│       ├── auth.js           Supabase login
│       ├── feed.js
│       ├── checkin.js
│       ├── places.js
│       └── profile.js
├── docker-compose.yml
└── Makefile
```

---

## Environment Variables

Copy `backend/.env.example` → `backend/.env` and fill in:

| Variable | Where to get it |
|---|---|
| `DATABASE_URL` | Supabase → Settings → Database → Connection string |
| `SUPABASE_URL` | Supabase → Settings → API |
| `SUPABASE_ANON_KEY` | Supabase → Settings → API |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase → Settings → API |
| `SUPABASE_JWT_SECRET` | Supabase → Settings → API → JWT Secret |
| `GOOGLE_PLACES_API_KEY` | Google Cloud Console → APIs & Services |

---

## Deploying

### Backend → Railway
1. Connect your GitHub repo on [Railway](https://railway.app)
2. Set the root directory to `backend/`
3. Add all env variables from `backend/.env`
4. Railway auto-detects the `Dockerfile`

### Frontend → Vercel / Netlify
1. Connect your GitHub repo
2. Set the root directory to `frontend/`
3. No build command needed (static files)
4. Update `frontend/js/config.js` with your production API URL

### Database migrations in production
```bash
# Run from Railway shell or locally with prod DATABASE_URL
make upgrade
```

---

## Branches

| Branch | Purpose |
|---|---|
| `main` | Production — auto-deploys |
| `dev` | Staging / integration |
| `feature/*` | Feature branches → PR into `dev` |
