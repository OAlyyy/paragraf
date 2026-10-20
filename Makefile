.PHONY: install db-up db-down migrate api test test-unit lint format up

install:          ## Install backend deps into backend/.venv
	cd backend && uv sync

db-up:            ## Start Postgres + pgvector and wait until healthy
	docker compose up -d --wait db

db-down:
	docker compose down

migrate:          ## Apply SQL migrations in backend/migrations
	cd backend && uv run python -m paragraf.migrate

api:              ## Run the API with auto-reload
	cd backend && uv run uvicorn paragraf.api.main:app --reload

up:               ## Run everything in Docker
	docker compose up --build

test:             ## All tests (integration tests need `make db-up migrate`)
	cd backend && uv run pytest

test-unit:        ## Tests that need no database
	cd backend && uv run pytest -m "not integration"

lint:
	cd backend && uv run ruff check . && uv run ruff format --check .

format:
	cd backend && uv run ruff check --fix . && uv run ruff format .
