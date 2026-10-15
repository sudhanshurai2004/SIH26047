# Godot/laptop validation checklist

**Status:** not verified in this repository environment. On 2026-10-15,
`command -v godot4` and `command -v godot` found no Godot 4 executable, so no
Godot scene, interaction, rendering path, or FPS result is claimed here.

Use this checklist on the actual demonstration laptop before claiming native
client readiness or performance.

## Before the run

1. Record the date, laptop make/model, CPU, integrated/discrete GPU, RAM, OS
   version, display resolution, power mode, and exact Godot 4.x version in the
   demo evidence log.
2. Copy the release folder locally; disconnect/disable Wi-Fi if validating the
   offline claim. Do not use a real doctrine or operational data.
3. Start the local API/dashboard with `./launch.sh` (Linux/macOS) or
   `launch.bat` (Windows), then confirm `http://127.0.0.1:8000/api/health`
   returns `offline_only: true`.
4. In Godot Project Manager, import `client/project.godot` (or the packaged
   `godot/project.godot`). Confirm the default scene is `res://2d/Main2D.tscn`.

## Functional smoke run

1. Run `Main2D.tscn` with blank `LocalApiBridge` credentials. Confirm the
   bundled scenario loads, the Play control advances the logical clock, target
   markers render, and each abstract decision creates a local outbox entry.
2. Seed the disposable demo database (`make demo-seed`) and configure the
   bridge with `demo-trainee`, PIN `262472`, and the documented session UUID.
   Confirm the session loads from the local API, actions synchronize, duplicate
   retry does not double-record, and completion succeeds.
3. Sign in locally as `demo-instructor` (PIN `262471`) in the dashboard, score
   the completed session, and verify the per-node AAR/timeline/replay appear.
4. Repeat with the night/rain demo scenario. Record any warning, visual defect,
   event-delivery issue, or crash rather than treating it as passed.

## FPS and interaction evidence

1. Close unrelated applications, connect AC power, use the intended display
   resolution, and record those conditions.
2. In the Godot editor run the 2D scene, open **Debugger → Monitors** and record
   the `Performance` FPS monitor during a 60-second representative playback.
   Capture a screen recording that includes the scene and monitor.
3. If checking the optional scene, separately run
   `client/scenes3d/Main3D.tscn`; toggle its available day/night, haze, and
   terrain presentation controls. Again record a 60-second capture with the
   FPS monitor visible. The configured frame cap is not a measured result.
4. Save raw evidence (video filename, monitor screenshots, min/median/max FPS
   observed, resolution, Godot version, and laptop details) outside Git or in a
   suitably approved evidence store. Do not round results up.
5. Only after the recorded 3D run meets the stated target should material say
   "30 FPS verified on [specified laptop]". Otherwise say **not verified**.

## Exit criteria

- The 2D functional smoke run, local event/AAR round trip, and offline API
  health check each have a dated result.
- Any 3D rendering/FPS claim names the exact target laptop and preserves its
  recording. Without that evidence, 3D and FPS remain not verified.
- Clear the disposable demo database and known demo PINs before any
  non-demonstration deployment.
