.PHONY: dev dev-frontend dev-backend test lint check

FRONTEND_DIR := frontend
BACKEND_APP := src.main:app
BACKEND_HOST := 0.0.0.0
BACKEND_PORT := 8000

dev:
	@set -e; \
	pids=""; \
	trap 'kill $$pids 2>/dev/null || true' INT TERM EXIT; \
	( cd "$(FRONTEND_DIR)" && npm run dev ) & pids="$$pids $$!"; \
	python -m uvicorn "$(BACKEND_APP)" --reload --host "$(BACKEND_HOST)" --port "$(BACKEND_PORT)" & pids="$$pids $$!"; \
	wait

dev-frontend:
	@cd "$(FRONTEND_DIR)" && npm run dev

dev-backend:
	@python -m uvicorn "$(BACKEND_APP)" --reload --host "$(BACKEND_HOST)" --port "$(BACKEND_PORT)"

test:
	@python -m pytest

lint:
	@python -m compileall -q src tests
	@cd "$(FRONTEND_DIR)" && npm run lint

check: lint test
