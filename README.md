# SIH26047 — Offline Threat Simulation Trainer

> **Training software only.** This project simulates abstract trainee decisions
> for Smart India Hackathon PS 26247. It does not provide a weapon, targeting,
> real doctrine, or real electronic-warfare interface.

An offline desktop trainer is being built in staged increments:

- **Python core** — FastAPI, NumPy, SQLite, deterministic scenarios, sessions,
  scoring, and adaptive skill selection.
- **Godot 4 client** — 2D-first playback and event recording; 3D is deferred.
- **React dashboard** — local AAR, replay, individual progress, and unit trends.

## Stage 1 status

Stage 1 (T1/T2) is complete in this checkout:

- repository skeleton, pinned tooling, GitHub Actions CI, and a one-command
  local development workflow;
- frozen JSON Schema Draft 2020-12 contracts for scenarios, trainee events, and
  editable doctrine, with valid and invalid samples and automated tests;
- a local FastAPI health endpoint and a React/Vite/TypeScript dashboard shell;
- a clearly labelled, abstract `doctrine/generic_demo.yaml` placeholder; and
- dependency/licence attribution in [`docs/CREDITS.md`](docs/CREDITS.md).

Scenario generation, session persistence, scoring, authentication, and Godot
playback begin in later stages. No performance number or benchmark is claimed.

## Prerequisites

- Python **3.11**
- Node.js **22** and npm **10**
- Git

The committed Python and npm lock files pin all project dependencies. Initial
installation may need access to the configured package registries; once they
are installed, the application itself makes no outbound network or telemetry
calls.

## Run locally

From the repository root, start both local processes with one command:

```bash
make dev
```

On first use, this creates `.venv`, installs `requirements-dev.lock`, and runs
`npm ci` for the dashboard. It then starts:

- FastAPI: `http://localhost:8000/api/health`
- Vite dashboard: `http://localhost:5173`

Press `Ctrl+C` to stop both. The dashboard uses relative `/api` URLs; Vite's
server-side development proxy is the only component that talks to the local
API port.

## Verify

```bash
# Explicit dependency installation (optional; make dev performs it when needed)
make setup

# Contract tests and API smoke test
make test

# Python lint/format checks and dashboard production build
make ci
```

GitHub Actions executes the same `make setup && make ci` checks.

## Contracts

| Contract | Purpose |
| --- | --- |
| [`contracts/scenario.schema.json`](contracts/scenario.schema.json) | Seed/profile/versioned deterministic playback scenario, including `t_visible_ms` and trajectories. |
| [`contracts/event.schema.json`](contracts/event.schema.json) | UUID-idempotent trainee event at a logical `t_offset_ms`. |
| [`contracts/doctrine.schema.json`](contracts/doctrine.schema.json) | Editable abstract score weights, response bounds, and decision tree. |

See [`contracts/README.md`](contracts/README.md) for the Stage 1 freeze and
compatibility rule. YAML is loaded only with `yaml.safe_load`, then schema
validated. Future upload endpoints must use `core.contracts.load_and_validate`.

## Repository layout

```text
contracts/      Frozen JSON contracts and valid/invalid samples
core/           Python service: generator, sessions, scoring, sensors, adaptive, api, db
client/         Godot skeleton: 2d, scenes3d, replay
dashboard/      React + Vite + TypeScript shell
doctrine/       Validated generic placeholder doctrine
experiments/    Future pilot-study scripts
docs/           Credits and recorded decisions
tests/          Automated contract and API tests
.github/         CI workflow
```

## Safety and determinism commitments

- Runtime operation is local-only: no cloud API, telemetry, paid API, or model
  download is configured.
- Ultralytics YOLO and AGPL dependencies are not used.
- The generic doctrine is explicitly a placeholder and uses only abstract
  responses (`monitor`, `report`, `escalate`, `defer`).
- Stage 2 will use a seeded NumPy generator only, precompute trajectories, and
  keep generation/scoring free of global randomness and wall-clock time.
- Detection-delay scoring will be measured from contract `t_visible_ms`, not
  scenario start, with weights and bounds read from validated doctrine YAML.

Implementation choices made because the referenced blueprint was not available
in this checkout are recorded in [`docs/DECISIONS.md`](docs/DECISIONS.md).
