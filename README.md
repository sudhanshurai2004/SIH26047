# SIH26047 — Offline Threat Simulation Trainer

> **Training software only.** This project simulates abstract trainee decisions
> for Smart India Hackathon PS 26247. It provides no weapon control, targeting,
> real doctrine, or real electronic-warfare interface.

The trainer runs locally on one machine:

- a **Python core** for deterministic scenario generation, SQLite sessions,
  validated doctrine scoring, replay, and adaptive skill selection;
- a **Godot 4 client** for 2D-first playback and trainee-event recording; and
- a **React dashboard** for login, local session review, replay, AAR, progress,
  and unit trends.

No runtime endpoint uses cloud APIs, telemetry, paid services, or model
downloads.

## Current implementation status

The repository now includes the planned T1–T16 foundation and MVP-hardening
components:

- frozen v1 scenario/event/doctrine JSON Schemas and safe YAML validation;
- deterministic generator V0 and generator V1 (swarms, abstract clutter,
  environment variants, novelty checks, and seeded sensor visibility/noise/dropouts);
- SQLite ORM users, salted PBKDF2 PINs, role checks, idempotent events,
  interrupted-session exclusion, backup, and additive migration handling;
- validated doctrine repository, decision-tree AAR scoring, per-skill Elo-style
  ratings, weakness-targeted selection, deterministic replay, and unit trends;
- local FastAPI routes plus the dashboard login/session/AAR/replay UI;
- Godot 2D playback/event outbox/local API bridge and optional 3D presentation;
- a headless self-test, source-package script, and real-session experiment scripts.

The attached Execution Blueprint PDF was not mounted into this workspace even
though its path was supplied. Per the user's instruction, implementation used
the explicit prompt and frozen contracts without inventing missing
Blueprint-specific data. Consequently **G1–G10 Blueprint golden fixtures and
any Blueprint-only benchmark/performance target remain unmeasured**. See
[`docs/DECISIONS.md`](docs/DECISIONS.md).

## Prerequisites

- Python **3.11**
- Node.js **22** and npm **10**
- Git
- Godot **4.x** (optional for the native client)

All Python/npm dependencies are pinned in committed lock files. Initial setup
may access configured package registries; application runtime remains local.

## Quick start

```bash
cd /home/user/SIH26047
make setup

# Headless seed → event → score verification in a temporary SQLite database.
make self-test

# Starts FastAPI on :8000 and the dashboard on :5173.
make dev
```

Open the dashboard at `http://localhost:5173`. On first run, enter a local admin
ID and PIN and choose **First run: create local admin**. This creates only a
local SQLite identity and seeds the generic placeholder doctrine.

## Run a full local session

The self-test verifies this headlessly. To use the desktop flow instead:

1. Start `make dev` and create a local admin in the dashboard.
2. While signed in as that admin, use **Local administration → Create local
   user** to create one instructor and one trainee (with different local PINs).
3. Sign in as the instructor, enter the trainee ID and a deliberate seed, then
   select **Create fixed demo** or **Create adaptive demo**. Copy the assigned
   session UUID from the session list/API response.
4. Open `client/project.godot` in Godot 4. Configure `LocalApiBridge` with the
   trainee ID, PIN, and assigned session UUID. The 2D client loads the local
   scenario, writes each abstract decision to its durable local outbox, retries
   it idempotently, and can complete the session.
5. Return to the instructor dashboard, refresh, select the completed session,
   and choose **Score session**. The AAR, deterministic replay, rating updates,
   and local trends become available there. Instructor tools also expose local
   doctrine validation/upload; admins can make a controlled SQLite backup.

For API-only deployments, the same role-protected routes are documented at
`http://localhost:8000/api/docs` while `make dev` is running.

The default `client/scenarios/pack-v0.json` also works with no API credentials;
it writes event data only to the local Godot outbox.

## Verification and packaging

```bash
# Tests, lint, formatting, self-test, and dashboard production build.
make ci

# Audit locked dashboard dependencies.
npm --prefix dashboard audit --audit-level=high

# Create a source archive from the committed revision in out/.
make package
```

GitHub Actions runs `make setup && make ci`.

## Contracts and safety

| Contract | Purpose |
| --- | --- |
| [`contracts/scenario.schema.json`](contracts/scenario.schema.json) | Versioned scenario trajectories and `t_visible_ms`. |
| [`contracts/event.schema.json`](contracts/event.schema.json) | UUID-idempotent trainee actions at logical `t_offset_ms`. |
| [`contracts/doctrine.schema.json`](contracts/doctrine.schema.json) | Editable abstract score weights, response bounds, and decision tree. |

Contract version `1.0` remains frozen. YAML is parsed only through
`yaml.safe_load`, then schema and semantic validation. All user-controlled
persistence queries use SQLAlchemy ORM parameters; static SQLite migration and
foreign-key setup statements contain no user data.

Detection delay is always calculated from `t_visible_ms`, not scenario start.
Action weights and allowed abstract responses come from validated doctrine YAML.
Interrupted sessions set `rating_eligible=false` and are ignored by the skill
model.

The shipped [`doctrine/generic_demo.yaml`](doctrine/generic_demo.yaml) is a
clearly labelled generic placeholder—not real doctrine.

## Repository layout

```text
contracts/      Frozen JSON contracts and valid/invalid samples
core/           Generator, sensors, SQLite, sessions, scoring, adaptive, replay, API
client/         Godot 2D, replay, bundled scenarios, and optional 3D view
dashboard/      React + Vite + TypeScript local dashboard
doctrine/       Validated generic placeholder doctrine
experiments/    Real-session pilot analysis scripts
docs/           Decisions and third-party credits
tests/          Automated core, API, client-pack, and experiment tests
scripts/        Dev, headless self-test, and source packaging helpers
```

## Backups and pilot scripts

- An authenticated local admin can call `POST /api/backups` to make a controlled
  SQLite backup under `data/backups/`.
- See [`experiments/README.md`](experiments/README.md) for adaptive-vs-fixed,
  unseen-seed, and rote-learning scripts. They read real local session rows and
  fail rather than fabricate missing data.
- See [`client/README.md`](client/README.md) for Godot setup and the optional
  3D-view limitations.

## Dependency credits

Every resolved Python/npm dependency and its package licence is recorded in
[`docs/CREDITS.md`](docs/CREDITS.md). Ultralytics YOLO and AGPL dependencies are
not used.
