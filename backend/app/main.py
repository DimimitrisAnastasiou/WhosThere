from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db.session import init_db
from app.api import checkins, places, users

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run setup on startup, teardown on shutdown."""
    await init_db()
    yield


app = FastAPI(
    title="CheckIn API",
    description="Backend for the CheckIn social location app.",
    version="0.1.0",
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(checkins.router, prefix="/api/checkins", tags=["checkins"])
app.include_router(places.router, prefix="/api/places", tags=["places"])
app.include_router(users.router, prefix="/api/users", tags=["users"])


@app.get("/health", tags=["meta"])
async def health():
    return {"status": "ok", "env": settings.app_env}
