# SIH26047 — Offline Threat Simulation Trainer

> **Training software only.** This project simulates abstract trainee decisions
> for Smart India Hackathon PS 26247. It does not provide a weapon, targeting,
> real doctrine, or real electronic-warfare interface.

An offline desktop trainer is being built in staged increments:

- **Python core** — FastAPI, NumPy, SQLite, deterministic scenarios, sessions,
  scoring, and adaptive skill selection.
- **Godot 4 client** — 2D-first playback and event recording; 3D is deferred.
- **React dashboard** — local AAR, replay, individual progress, and unit trends.

## Stage 2 status

Stages 1–2 (T1–T5) are complete in this checkout:

- repository skeleton, pinned tooling, GitHub Actions CI, and a one-command
  local development workflow;
- frozen JSON Schema Draft 2020-12 contracts for scenarios, trainee events, and
  editable doctrine, with valid and invalid samples and automated tests;
- deterministic generator V0: one precomputed abstract target trajectory per
  seeded scenario, with schema, validity, and solvability checks;
- local SQLite ORM models for users, sessions, event-id idempotency, session
  interruption, role checks, and salted PIN hashes;
- deterministic decision-tree scoring driven by validated doctrine YAML; and
- a clearly labelled, abstract `doctrine/generic_demo.yaml` placeholder plus
  dependency/licence attribution in [`docs/CREDITS.md`](docs/CREDITS.md).

Godot playback and the dashboard AAR workflow begin in Stage 3. No performance
number or benchmark is claimed.

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

## Stage 2 scoring and local session rules

- `core.generator.generate_scenario` uses a local seeded NumPy `PCG64`
  generator and canonical JSON output. The same seed, profile, and generator
  version produce byte-identical scenario bytes.
- `core.scoring.score_scenario` is pure: it reads action weights, timing
  thresholds, decision-tree branches, and permitted abstract responses from
  doctrine YAML. Detection delay is always `event.t_offset_ms - t_visible_ms`.
- SQLite sessions persist canonical scenario/event JSON. Event UUIDs are
  idempotency keys; reusing an ID with different content is rejected.
- A `session_interrupted` event marks the session interrupted and
  `rating_eligible=false`. Future skill-rating code must exclude those rows.
- Only `trainee`, `instructor`, and `admin` roles are accepted. PINs use salted
  PBKDF2-SHA256 hashes; plaintext PINs are never stored.

The Blueprint PDF content was not readable in this workspace, and the user
asked to proceed from the prompt only. Therefore no synthetic replacement for
Blueprint golden scenarios G1–G10 was created. See
[`docs/DECISIONS.md`](docs/DECISIONS.md).

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
- Stage 2 uses a seeded NumPy generator only, precomputes trajectories, and
  keeps generation/scoring free of global randomness and wall-clock time.
- Detection-delay scoring is measured from contract `t_visible_ms`, not
  scenario start, with weights and response bounds read from validated doctrine YAML.

Implementation choices made because the referenced blueprint was not available
in this checkout are recorded in [`docs/DECISIONS.md`](docs/DECISIONS.md).
