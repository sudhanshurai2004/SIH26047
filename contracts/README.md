# Frozen contracts — Stage 1

These three JSON Schema Draft 2020-12 files are the Stage 1 wire contracts:

- `scenario.schema.json` — deterministic playback data and precomputed target trajectories.
- `event.schema.json` — idempotent trainee actions at logical session offsets.
- `doctrine.schema.json` — editable, abstract training scoring/decision-tree data.

`contracts/samples/*valid*` must validate and `*invalid*` must fail. The test suite validates both the schemas themselves and every sample. YAML doctrine files are parsed with `yaml.safe_load` before validation.

## Compatibility rule

The `contract_version` value `1.0` is frozen after Stage 1. A breaking change requires a new contract version and migration path; do not silently alter the existing schemas or samples. Structural schema validation lives here. Cross-record semantic validation (such as monotonic trajectory times, decision-tree references, and score-weight totals) is intentionally deferred to the Stage 2 generator/scoring implementation.

All time fields are logical millisecond offsets. Scenario generation and scoring must not add wall-clock timestamps to a contract payload.
