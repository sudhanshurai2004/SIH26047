# Release-readiness evidence — SIH 2026 PS 26247

**Scope:** offline, local, training-only software. This is not a weapon,
targeting, operational-doctrine, real-sensor, or real-EW product. The governing
source is [`docs/input/SIH 26247 Execution Blueprint.md`](input/SIH%2026247%20Execution%20Blueprint.md).
The historical `SIH26047` technical alias is intentional and explained in
[`DECISIONS.md`](DECISIONS.md#d-011--blueprint-source-and-corrected-problem-identifier-2026-10-15).

## Requirement matrix

Status meanings: **Done** has automated/command evidence for the described
scope; **Partial** has a real implementation but a stated validation or
functional gap; **Missing** has no implementation. Counts are over the seven
briefed outcome rows, not a claim that every Blueprint target is complete.

| Outcome | Status | Shipped evidence | Executed evidence | Honest boundary / next evidence needed |
| --- | --- | --- | --- | --- |
| Desktop simulator | Partial | `client/2d/`, `client/scenes3d/`, local bridge/outbox, dashboard | Static client tests are included in the full suite. | Godot was unavailable here; native execution, interaction, rendering, startup, and FPS are **not verified**. Follow `GODOT_CHECKLIST.md`. |
| Scripted and procedural scenarios | Done | `demo/scenarios/01-*` static scripted snapshot; V0/V1 seeded generators; `scripts/seed_demo.py` | Contract/generator/demo asset tests in full suite; demo seed command creates three sessions. | Synthetic training data only; no real threat data. |
| Environment and swarm variants | Partial | V1 boid-style swarm/clutter generation; rural/urban, day/night/rain fields; synthetic sensor `t_visible_ms`; ready swarm/night snapshots | V1 tests and demo asset test in full suite. | Core generation is verified; native visual presentation and any realism/performance assertion are not. |
| Decision-tree scoring | Done | Frozen doctrine schema, safe YAML validation, generic placeholder, per-node AAR, real-v1 G1–G9 adapter | Production-Golden command passes 11 tests; full engine/API tests pass. | Placeholder doctrine is not approved operational doctrine; proposed sidecar policy is not native v1 doctrine. |
| Individual, unit, repeated-session AAR | Partial | SQLite scores/replay, Elo records, unit IDs, role-scoped unit summary API/dashboard | Session/API/unit-summary tests in full suite; dashboard production build passes. | Browser/native UI interaction and real repeated trainee data are not manually validated; no pilot claims. |
| Difficulty and randomisation | Partial | Seeded NumPy V1 generator, difficulty profiles, adaptive selector, fresh-seed UI, exact V1 fingerprint repeat rejection | Generator/adaptive/novelty tests in full suite. | Repeat guard is exact structural matching across history, not the Blueprint’s semantic “similar last N” metric; no pilot calibration. |
| Offline minimal-hardware unit use | Partial | SQLite, relative API UI, local package folder, one-origin launcher, `.bat`/`.sh`, generic no-cloud runtime | Packaged localhost root/API smoke test succeeds; clean-clone build/test evidence below. | No clean target-laptop, air-gapped wheelhouse, Godot export, or hardware/FPS measurement has been performed. |

**Matrix count: 2 Done / 5 Partial / 0 Missing.** Partial does not mean safe
to silently promote a claim; see [`LIMITATIONS.md`](LIMITATIONS.md).

## Proposed G1–G10 production bridge

The proposed hand-authored pack is not canonical Blueprint data or doctrine.
Frozen v1 schemas were not changed to accept its compact objects. Instead,
`core/scoring/golden_v1_adapter.py` creates nested valid scenario/doctrine and
lowercase versioned event payloads, then calls real `score_scenario()` once per
target.

| Proposed behavior | Production v1 path exercised | Result / boundary |
| --- | --- | --- |
| G1–G4 normal/benign/friendly behavior | schema validation; v1 tree detect/classify/respond scoring | Executed by adapter tests; aggregate policy remains sidecar where needed. |
| G5 timing | `t_visible_ms` to real detection-delay node calculation | Tested: production node observes `12_000` ms from visibility, not scenario start. |
| G6 swarm member aggregation | one valid v1 production score per translated target | Per-target production scoring is exercised; pack aggregate mean is adapter sidecar. |
| G7 no action / critical miss | v1 timeout path | Timeout is native; inner-zone critical penalty is sidecar because v1 lacks zones. |
| G8 duplicate batch | `score_scenario()` canonical identical-event-ID deduplication | Native production hardening: identical retry scores once; changed-content reuse raises `ScoringError`. |
| G9 interrupted session | production `interrupted=True` rating eligibility | Native report is scoreable and `rating_eligible=false`; proposed aggregate remains sidecar. |
| G10 invalid doctrine upload | validated doctrine repository/API keeps prior valid record | Covered by hardening/API test; intentionally no scoreable event scenario exists. |

**Non-expressible in frozen v1:** the proposed class-specific response matrix,
outer/inner zones, protected-zone behavior, critical engagement/miss penalties,
friendly cap, aggregate mean, and proposed source retry count. The adapter
implements them visibly as test sidecar logic; production v1 does **not** claim
to implement them. A future approved requirement needs a versioned contract and
doctrine migration.

### Golden evidence

```text
$ PYTHONPATH=. .venv/bin/python -m pytest tests/golden/test_production_v1_golden.py -q
...........                                                              [100%]
11 passed in 0.29s
```

That result specifically covers G1–G9 adapter/reference equivalence plus the
G5 visibility and G8 duplicate production assertions. The latest complete
suite result appears below.

## Packaging, demo, and local controls

- `make package` runs `scripts/package_offline.sh`, producing
  `out/SIH26247-offline-trainer/`, its `.tar.gz`, `api/`, built `dashboard/`,
  `godot/`, `launch.sh`, and `launch.bat`.
- A package smoke run served `/` and `/api/health` from `127.0.0.1:8765`; both
  returned HTTP 200. This verifies local one-origin static/API wiring, not a
  Windows run, air-gapped dependency installation, Godot export, or target
  hardware.
- `make demo-seed` creates an ignored disposable database with one scripted,
  one swarm, and one night/rain higher-difficulty session. It uses public demo
  credentials only and refuses a non-empty database unless `--reset` is explicit.
  See `DEMO.md`.
- Users have salted PBKDF2 PINs; event retries are idempotent; conflicting IDs
  are rejected; interrupted sessions are rating-ineligible; ORM queries and role
  checks are used; instructors are scoped to their unit. The dashboard starts
  with blank credentials.

## Fresh-clone evidence

On 2026-10-15, the pushed branch commit `16ac81c` was freshly cloned from GitHub
into `/tmp/SIH26047-release-clean` with:

```text
$ git clone --branch arena/14719d8a-sih26047 --single-branch \
  https://github.com/sudhanshurai2004/SIH26047.git /tmp/SIH26047-release-clean
HEAD=16ac81c
tracked_files=126
```

The README workflow then succeeded in that new directory:

```text
$ make setup
Successfully installed ... fastapi-0.115.12 ... pytest-8.3.5 ... uvicorn-0.34.2
added 73 packages, and audited 74 packages in 1s
found 0 vulnerabilities

$ make self-test
{"rating_eligible": true, "scenario_id": "scenario-4f38d04fd72b2af0", "score": 100.0, "status": "ok"}

$ make ci
All checks passed!
50 files already formatted
collected 89 items
89 passed, 1 warning in 16.81s
{"rating_eligible": true, "scenario_id": "scenario-4f38d04fd72b2af0", "score": 100.0, "status": "ok"}
vite ... built in 870ms
```

`make dev` started FastAPI on `:8000` and Vite on `:5173`; direct local checks
returned:

```text
API health: {"status":"ok","stage":"8","offline_only":true}
API OpenAPI HTTP: 200
Dashboard HTTP/title: <title>SIH 26247 Offline Trainer</title>
```

`make package` also succeeded in the fresh clone, producing its folder/archive.
Running its copied `api/serve_local.py` with the fresh clone’s pinned virtual
environment returned a dashboard HTTP 200 and:

```text
packaged API health: {"status":"ok","stage":"8","offline_only":true}
```

**Fresh-clone outcome:** no setup, self-test, CI, API, dashboard, or package
failure occurred, so no fresh-clone code fix was required. This is a Linux
source/pinned-environment check—not a Windows, air-gapped, Godot, or target
hardware validation.

## Quality, dependency, and hygiene evidence

Executed on 2026-10-15:

```text
$ make ci
All checks passed!
50 files already formatted
89 passed, 1 warning in 17.21s
{"rating_eligible": true, "scenario_id": "scenario-4f38d04fd72b2af0", "score": 100.0, "status": "ok"}
vite ... built in 805ms

$ make golden-test
collected 31 items
31 passed in 0.34s

$ npm --prefix dashboard audit --audit-level=high
found 0 vulnerabilities

$ .venv/bin/python -m pip check
No broken requirements found.

$ [lock-file scan]
agpl_or_ultralytics_lock_hits=none

$ printf '%s\n' data/demo.sqlite3 .env .env.local secrets/real-doctrine.yaml device-private.key certificate.pem | git check-ignore -v --stdin
.gitignore:12:data/  data/demo.sqlite3
.gitignore:17:.env  .env
.gitignore:18:.env.*  .env.local
.gitignore:24:secrets/  secrets/real-doctrine.yaml
.gitignore:21:*.key  device-private.key
.gitignore:20:*.pem  certificate.pem
$ git ls-files 'data/*' '*.sqlite3' '.env' '.env.*' 'secrets/*' | wc -l
0
$ [basic marker scan]
private_key_markers=0
aws_access_key_markers=0
```

The audited source uses the MIT repository `LICENSE`; `CREDITS.md` inventories
pinned dependencies and records that no AGPL/Ultralytics dependency is declared.
`.gitignore` excludes SQLite/runtime data, local environment files, key/cert
patterns, and `secrets/`. The public demo PIN is source-visible by design but is
created only by an explicit disposable seeder, never by normal startup.

## Remaining user actions before any real use

1. Validate Godot 4 client interaction, 2D/3D rendering, startup, and FPS on
the actual intended laptop using `GODOT_CHECKLIST.md`; preserve recordings.
2. Obtain and approve real doctrine/cue policy through the responsible authority;
do not substitute the generic placeholder.
3. Prepare a vetted Python wheelhouse/environment and test the packaged folder
on the actual air-gapped Windows/Linux/macOS target; make no portability claim
until then.
4. Run pilot/rehearsal sessions with consent and keep real evidence separate
from the disposable demo data. Do not claim training transfer without it.
