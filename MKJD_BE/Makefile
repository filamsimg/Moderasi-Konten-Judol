.PHONY: docker-up docker-down docker-start docker-stop docker-restart docker-logs docker-ps docker-fresh db-wait db-migrate db-seed db-seed-sample venv install install-ml api-run dev dev-ml dev-reset

COMPOSE ?= docker compose
PY ?= python
PY_BOOT ?= python
VENV ?= .venv
REQ_CORE ?= requirements-core.txt
REQ_ML ?= requirements-ml.txt
DB_URL ?= postgresql+psycopg2://mkjd:mkjd@localhost:5432/mkjd

ifeq ($(OS),Windows_NT)
  VENV_PY := $(VENV)/Scripts/python
else
  VENV_PY := $(VENV)/bin/python
endif
CORE_STAMP := $(VENV)/.deps_core_installed
ML_STAMP := $(VENV)/.deps_ml_installed

$(VENV_PY):
	$(PY_BOOT) -m venv $(VENV)

$(CORE_STAMP): $(REQ_CORE) | $(VENV_PY)
	$(VENV_PY) -m pip install -r $(REQ_CORE)
	$(VENV_PY) -c "from pathlib import Path; Path('$(CORE_STAMP)').touch()"

$(ML_STAMP): $(REQ_ML) | $(VENV_PY)
	$(VENV_PY) -m pip install -r $(REQ_ML)
	$(VENV_PY) -c "from pathlib import Path; Path('$(CORE_STAMP)').touch(); Path('$(ML_STAMP)').touch()"

venv: $(VENV_PY)

install: $(CORE_STAMP)

install-ml: $(ML_STAMP)

api-run: install
	$(VENV_PY) -m uvicorn app.main:app --reload

dev: install api-run

dev-ml: install-ml api-run

dev-reset:
ifeq ($(OS),Windows_NT)
	powershell -NoProfile -Command "Remove-Item -Recurse -Force '$(VENV)' -ErrorAction SilentlyContinue"
else
	rm -rf "$(VENV)"
endif
	$(MAKE) dev

docker-up:
	$(COMPOSE) up -d

docker-down:
	$(COMPOSE) down

docker-start:
	$(COMPOSE) start

docker-stop:
	$(COMPOSE) stop

docker-restart:
	$(COMPOSE) restart

docker-logs:
	$(COMPOSE) logs -f

docker-ps:
	$(COMPOSE) ps

db-wait:
	$(PY) scripts/wait_for_db.py --url "$(DB_URL)" --timeout 60

db-migrate:
	DATABASE_URL=$(DB_URL) alembic upgrade head

db-seed:
	DATABASE_URL=$(DB_URL) $(PY) app/seed.py

db-seed-sample:
	DATABASE_URL=$(DB_URL) $(PY) app/seed.py --sample

docker-fresh:
	$(COMPOSE) down -v
	$(COMPOSE) up -d
	$(MAKE) db-wait
	$(MAKE) db-migrate
	$(MAKE) db-seed-sample
