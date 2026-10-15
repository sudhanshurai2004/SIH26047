# Limitations and non-claims

This is an offline, **training-only** prototype for SIH 2026 PS **26247**. It
has no weapon control, targeting hardware interface, real doctrine, real
sensor feed, real electronic-warfare interface, cloud dependency, telemetry, or
claim of operational suitability.

## Blueprint and evaluation status

- The governing execution blueprint is available in this checkout as
  `docs/input/SIH 26247 Execution Blueprint.md`; it is planning/design input,
  not proof that all of its acceptance targets are met.
- The G1–G10 files are an explicitly **proposed hand-authored reference spec**,
  not recovered canonical Blueprint fixtures or real doctrine. The production
  adapter runs G1–G9's translatable portions through v1 scoring; its non-v1
  policy remains sidecar logic. G10 validates rejection/active-doctrine
  retention rather than scoring a scenario.
- There is no collected pilot study, no target-user usability study, no
  measured training transfer, and no claim that adaptive selection improves
  real-world or in-simulator outcomes.

## Doctrine and synthetic cues

- `doctrine/generic_demo.yaml` is a generic placeholder. It is not approved by
  DSSC or any operational authority and must be replaced only through the
  validated upload/review process.
- Classes, trajectories, visibility, noise, dropouts, night/rain effects, and
  response choices are abstract training data. They are not calibrated radar,
  optical, acoustic, or electronic-warfare models.
- Frozen contract v1 cannot natively express the proposed pack's protected
  zones, class-specific response matrix, critical penalties, friendly cap, or
  aggregate policy. A future approved requirement needs a versioned contract
  and doctrine migration—not hidden production rules.

## Godot and performance

- Godot 4 was **not installed** in the validation environment on 2026-10-15.
  The Godot project, 2D interaction, 3D scene, local bridge at runtime,
  rendering, startup time, and FPS are therefore **not verified**.
- The optional 3D presentation is not a release claim. The 2D scene is the
  intended fallback. Follow `docs/GODOT_CHECKLIST.md` on the actual target
  laptop and preserve recordings before making any runtime or FPS statement.
- The Blueprint's 30 FPS, under-30-second startup, 50-target generation, and
  clean-laptop performance targets have not been measured here.

## Deployment and data boundaries

- The packaging script produces a local source folder and launchers, not a
  signed installer, bundled Python runtime, vendored wheelhouse, or Godot
  export. An air-gapped laptop still needs a vetted preinstalled Python
  environment/dependency wheelhouse; actual clean-laptop execution remains a
  user validation action.
- SQLite data and backups are local. OS disk encryption, endpoint management,
  identity policy, retention, and approval for any real deployment are outside
  this repository.
- Public demo credentials are intentionally disposable and must not be used for
  any real person or retained database. No production account is seeded by
  application startup.

See `docs/READINESS.md` for executed evidence and `docs/DECISIONS.md` for the
reasons behind these boundaries.
