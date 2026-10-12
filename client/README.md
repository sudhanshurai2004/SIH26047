# Godot client skeleton

The Godot 4 project begins in Stage 3. The required module directories are
present now so ownership is clear:

- `2d/` — Stage 3 playback, radar plan view, and abstract trainee controls.
- `scenes3d/` — Stage 7 3D scenes; this must not replace the 2D mode.
- `replay/` — deterministic replay presentation.

No executable Godot scene is included in Stage 1 because the frozen contracts
must be completed before client event-recording code is introduced.
