SHELL := /bin/bash

PYTHON ?= python3
VENV ?= .venv
VENV_PYTHON := $(VENV)/bin/python
VENV_PIP := $(VENV)/bin/pip

.PHONY: setup python-install dashboard-install dev test self-test lint format-check dashboard-build ci package clean

# Install exactly the versions captured in the committed lock files.
setup: python-install dashboard-install

python-install:
	@test -x "$(VENV_PYTHON)" || $(PYTHON) -m venv "$(VENV)"
	"$(VENV_PIP)" install -r requirements-dev.lock

dashboard-install:
	npm --prefix dashboard ci

# Starts only local processes: FastAPI on :8000 and Vite on :5173.
dev:
	./scripts/dev.sh

test:
	"$(VENV_PYTHON)" -m pytest

self-test:
	PYTHONPATH=. "$(VENV_PYTHON)" scripts/self_test.py

lint:
	"$(VENV_PYTHON)" -m ruff check core tests experiments scripts

format-check:
	"$(VENV_PYTHON)" -m ruff format --check core tests experiments scripts

dashboard-build:
	npm --prefix dashboard run build

ci: lint format-check test self-test dashboard-build

package:
	./scripts/package.sh

clean:
	rm -rf .pytest_cache .ruff_cache dashboard/dist
