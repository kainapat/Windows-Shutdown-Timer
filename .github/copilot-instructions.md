# Project Guidelines

## Project Context
- Windows desktop app built with Python + PySide6.
- Main code is in `shutdown_timer.py` (single-file architecture).
- This project controls Windows power actions (shutdown/restart/sleep/hibernate) through system commands.

## Build And Run
- Install dependencies:
  - `pip install -r requirements.txt`
- Run app from source:
  - `python shutdown_timer.py`
- Build executable (README/workflow pattern):
  - `pip install pyinstaller`
  - `pyinstaller --onefile --windowed --name="Windows Shutdown Timer" --icon=icon.ico shutdown_timer.py`

## Testing
- There is no automated test suite in this repository.
- Validate changes manually by running the app and checking:
  - timer start/cancel flows
  - all 4 actions (shutdown/restart/sleep/hibernate)
  - all timer modes (datetime/hours/minutes/seconds)
  - save/load/clear settings behavior

## Architecture
- UI + logic live in `shutdown_timer.py`.
- Main classes:
  - `PresetCard`: quick preset button UI.
  - `Toast`: animated top notification.
  - `ShutdownTimerApp`: app state, UI wiring, timer logic, system command execution.
- Persistent settings file is `timer_config.json` (`CONFIG_FILE`).

## Conventions And Behavior Notes
- Action index mapping must stay consistent:
  - `0` shutdown
  - `1` restart
  - `2` sleep
  - `3` hibernate
- `PRESETS` are intended for shutdown/restart only. Sleep/hibernate are blocked in preset flow.
- Sleep and hibernate currently execute immediately after confirmation (not delayed countdown actions).
- Current behavior deletes `timer_config.json` on close via `closeEvent` + `_delete_config_file()`.

## Safe Change Guidelines
- Keep Windows command execution changes minimal and verify on Windows before release.
- Preserve mode ID mapping with `QButtonGroup` and `QStackedWidget` index alignment.
- Prefer small focused edits in `shutdown_timer.py`; avoid broad refactors unless requested.
- When changing user-visible behavior, update `README.md` and `.github/workflows/build-release.yml` if build or usage steps change.