# Decisions

This log records only decisions needed when the supplied requirements leave an
implementation choice open. Dates use the project-local Asia/Kolkata date.

## D-001 — Stage 1 contract representation (2026-10-12)

**Context:** The request refers to an attached Execution Blueprint, but no
blueprint file or attachment was available in the checked-out repository at the
start of Stage 1.

**Decision:** Implement the explicitly requested Stage 1 deliverables from the
prompt using JSON Schema Draft 2020-12 and contract version `1.0`. Scenario
times are logical millisecond offsets; event actions use `t_offset_ms`; and the
doctrine contains only abstract training choices (`monitor`, `report`,
`escalate`, `defer`). No data set, benchmark, doctrine, or performance claim
was invented.

**Consequence:** `contracts/*.schema.json` are frozen at `1.0` after Stage 1.
Before Stage 2, reconcile any conflicting blueprint field names or semantics by
adding a versioned migration rather than silently changing this contract.

## D-002 — Local development topology (2026-10-12)

**Decision:** `make dev` starts FastAPI on port 8000 and Vite on port 5173.
The dashboard is configured to use relative `/api` paths; only Vite's local
development proxy targets `127.0.0.1:8000` server-side. Browser-facing code
contains no localhost API address.

**Consequence:** The desktop product remains local-only and no runtime endpoint
is configured to send telemetry or call a remote service.

## D-003 — Demo doctrine safety boundary (2026-10-12)

**Decision:** Ship `doctrine/generic_demo.yaml` now as a clearly labelled,
abstract placeholder so later scoring has a versioned fixture. It contains no
weapon operation, targeting, electronic-warfare technique, or real doctrine.

**Consequence:** Scoring reads action weights and permitted abstract responses
exclusively from validated YAML contract data, not hard-coded values.

## D-004 — Blueprint golden-scenario limitation (2026-10-12)

**Context:** The Execution Blueprint PDF was attached for Stage 2, but its
reported `/home/user/uploads/` path was not mounted in this workspace. When
asked how to proceed, the user selected **“Proceed from the prompt only.”**

**Decision:** Implement the explicit prompt scope and add hand-checked tests
for the generic demo doctrine, without claiming those tests are Blueprint golden
scenarios. Do not invent G1–G10 inputs, scores, or benchmark data.

**Consequence:** The required Blueprint G1–G10 golden-fixture suite remains
unmeasured and must be added from the supplied source material before an MVP
lock that requires it.

## D-005 — V0 detection-delay credit curve (2026-10-12)

**Context:** Contract v1 contains doctrine-owned action weights and three
detection-delay thresholds, but no separate per-band credit coefficients.

**Decision:** Award full detection credit through `excellent_ms`, then linearly
decrease it to zero at `late_ms`; preserve `acceptable_ms` as an auditable AAR
band boundary. The formula adds no hard-coded action weight and uses only the
validated doctrine thresholds.

**Consequence:** The generic demo scoring tests state their arithmetic. Replace
this formula only through a versioned doctrine/contract decision once the
Blueprint scoring specification is available.

## D-006 — Continue from the supplied prompt when the attached PDF is unavailable (2026-10-12)

**Context:** The Execution Blueprint was attached again, but the declared
`/home/user/uploads/SIH 26247 Execution Blueprint.pdf` path is not mounted in
this coding workspace. The user explicitly asked to continue without repeated
questions.

**Decision:** Continue implementation from the explicit project prompt and the
frozen contracts. Do not claim that unavailable Blueprint-specific values (in
particular G1–G10 fixtures or performance targets) have been reproduced.

**Consequence:** Later functionality remains generic, training-only, and is
covered by real local tests. Blueprint-specific acceptance items remain labelled
unmeasured until its contents become accessible.

## D-007 — V1 sensor traces preserve the frozen scenario contract (2026-10-12)

**Context:** The frozen scenario contract records a target's precomputed
`t_visible_ms`, but has no field for a complete sensor trace.

**Decision:** Generate deterministic visibility/noise/dropout traces with
caller-local NumPy PCG64 generators. Keep the trace as a generator/replay
artifact and persist only its precomputed first-visible logical offset in the
contract scenario.

**Consequence:** V1 generation remains byte-stable for seed/profile/version and
scoring still measures detection relative to `t_visible_ms`. Adding serialized
sensor samples later requires a new contract version rather than an extra v1
field.

## D-008 — Generic adaptive model and evidence boundaries (2026-10-12)

**Decision:** Use a small persisted per-skill Elo-style adjustment with a stable
weakest-skill selector. Analyze adaptive-vs-fixed, unseen seeds, and repetition
only from recorded SQLite scored-session data; scripts refuse missing data.

**Consequence:** The project provides an auditable local pilot mechanism, not a
claim that adaptive training outperforms fixed training. No pilot result,
retention result, or student-performance number is bundled.

## D-009 — Godot validation boundary (2026-10-12)

**Decision:** Ship a Godot 4 project with a 2D default scene, local event outbox,
optional 3D presentation toggles, and a documented 30-FPS cap target. Test its
files and bundled scenario pack statically when Godot is unavailable.

**Consequence:** The source is integrated with the local API bridge, but no
runtime Godot rendering, interaction, or frame-rate result is claimed until a
Godot executable validates it on target hardware.
