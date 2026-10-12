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

**Consequence:** Stage 2 must read scoring weights and permitted abstract
responses exclusively from this validated YAML contract, not hard-code them.

## D-004 — Blueprint golden-scenario limitation (2026-10-12)

**Context:** The Execution Blueprint PDF was attached for Stage 2, but its
reported `/home/user/uploads/` path was not mounted in this workspace. When
asked how to proceed, the user selected **“Proceed from the prompt only.”**

**Decision:** Implement T3–T5 from the explicit Stage 2 summary and add
hand-checked tests for the generic demo doctrine, without claiming those tests
are Blueprint golden scenarios. Do not invent G1–G10 inputs, scores, or
benchmark data.

**Consequence:** The required Blueprint G1–G10 golden-fixture suite remains
unmeasured and must be added from the supplied source material before MVP lock.

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
