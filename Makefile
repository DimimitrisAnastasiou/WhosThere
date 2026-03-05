.PHONY: help install dev migrate upgrade downgrade reset seed test lint format check build clean

# ── Colours ───────────────────────────────────────────────────────────────────
CYAN  := \033[0;36m
RESET := \033[0m

help: ## Show this help
	@echo ""
	@echo "  $(CYAN)Who'sThere Web App$(RESET) — available commands"
	@echo ""
	@awk 'BEGIN {FS = ":.*##"} /^[a-zA-Z_-]+:.*##/ { printf "  $(CYAN)%-18s$(RESET) %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""

# ── Setup ─────────────────────────────────────────────────────────────────────
install: ## Install all dependencies and copy .env
	@echo "$(CYAN)→ Setting up backend...$(RESET)"
	cd backend && python -m venv .venv && .venv/bin/pip install --upgrade pip && .venv/bin/pip install -r requirements.txt
	@if [ ! -f backend/.env ]; then cp backend/.env.example backend/.env; echo "$(CYAN)→ Created backend/.env from example — fill in your keys$(RESET)"; fi
	@echo "$(CYAN)→ Done! Run 'make dev' to start.$(RESET)"

# ── Development ───────────────────────────────────────────────────────────────
dev: ## Start backend + serve frontend (requires two terminals or use tmux)
	@echo "$(CYAN)→ Starting FastAPI backend on http://localhost:8000$(RESET)"
	@echo "$(CYAN)→ Frontend at http://localhost:5500 (use Live Server or 'make frontend')$(RESET)"
	cd backend && .venv/bin/uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

frontend: ## Serve the frontend with Python's built-in server
	@echo "$(CYAN)→ Frontend at http://localhost:5500$(RESET)"
	cd frontend && python3 -m http.server 5500

dev-all: ## Start both backend and frontend in parallel
	@make -j2 dev frontend

# ── Database ──────────────────────────────────────────────────────────────────
migrate: ## Create a new migration (usage: make migrate msg="your message")
	cd backend && .venv/bin/alembic revision --autogenerate -m "$(msg)"

upgrade: ## Apply all pending migrations
	cd backend && .venv/bin/alembic upgrade head

downgrade: ## Roll back one migration
	cd backend && .venv/bin/alembic downgrade -1

reset: ## Drop everything and re-run all migrations (⚠ destructive)
	@echo "$(CYAN)→ Resetting database...$(RESET)"
	cd backend && .venv/bin/alembic downgrade base && .venv/bin/alembic upgrade head

seed: ## Seed the database with sample data
	cd backend && .venv/bin/python -m app.db.seed

# ── Testing ───────────────────────────────────────────────────────────────────
test: ## Run all tests
	cd backend && .venv/bin/pytest tests/ -v

test-cov: ## Run tests with coverage report
	cd backend && .venv/bin/pytest tests/ -v --cov=app --cov-report=term-missing

# ── Code Quality ──────────────────────────────────────────────────────────────
lint: ## Run linter (ruff)
	cd backend && .venv/bin/ruff check app/ tests/

format: ## Auto-format code (ruff + black)
	cd backend && .venv/bin/ruff format app/ tests/

check: lint ## Run all checks (used in CI)
	cd backend && .venv/bin/mypy app/ --ignore-missing-imports

# ── Docker (optional, for production parity) ──────────────────────────────────
docker-build: ## Build Docker image
	docker compose build

docker-up: ## Start with Docker Compose
	docker compose up

docker-down: ## Stop Docker Compose
	docker compose down

# ── Cleanup ───────────────────────────────────────────────────────────────────
clean: ## Remove caches and compiled files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; \
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null; \
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null; \
	find . -name "*.pyc" -delete 2>/dev/null; \
	echo "$(CYAN)→ Cleaned$(RESET)"
