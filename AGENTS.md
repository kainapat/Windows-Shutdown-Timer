# AGENTS.md

## Overview

- Windows-only desktop app built with Python + PySide6 for scheduling shutdown, restart, sleep, and hibernate.
- Main implementation is in `shutdown_timer.py` (single-file app).
- Some power operations may require Administrator privileges.

## Build and Test

- Install and run:
    - `pip install -r requirements.txt`
    - `python shutdown_timer.py`
- Build executable (PyInstaller):
    - `pip install pyinstaller`
    - `pyinstaller --onefile --windowed --name="Windows Shutdown Timer" --icon=icon.ico shutdown_timer.py`
- Release:
    - `git tag vX.Y.Z && git push origin vX.Y.Z`
    - CI workflow: `.github/workflows/build-release.yml`
- Testing:
    - No test suite currently exists.
    - Recommended approach: `pytest` + `pytest-qt`, with `subprocess.run` mocked for power-command paths.

## Code Style

- Python 3.12+, keep changes focused and minimal.
- Naming conventions:
    - Classes: `PascalCase`
    - Methods/functions: `snake_case`
    - Private methods/functions: `_snake_case`
    - Constants: `UPPER_SNAKE_CASE`
- Prefer f-strings and explicit Qt enums (for example `Qt.PointingHandCursor`).
- Use `encoding="utf-8"` for file I/O and wrap external command calls in `try/except`.

## Architecture

- Key files:
    - `shutdown_timer.py` (UI, timer flow, command execution)
    - `requirements.txt`
    - `Windows Shutdown Timer.spec`
    - `.github/workflows/build-release.yml`
- Critical methods in `shutdown_timer.py`:
    - `init_ui`
    - `apply_styles`
    - `update_theme_colors`
    - `start_timer`
    - `cancel_timer`
    - `update_countdown`
    - `start_preset_timer`
    - `save_settings`
    - `load_settings`
    - `_execute_sleep_hibernate`
    - `_delete_config_file`
- Config lifecycle:
    - `timer_config.json` is saved when a timer starts.
    - `timer_config.json` is deleted on app close, clear, or timer completion.

## Conventions and Pitfalls

- UI text includes Thai; preserve existing wording and layout intent.
- App uses a dark theme; keep new UI changes visually consistent.
- This app depends on Windows `shutdown` behavior; avoid adding non-Windows assumptions.
- Validate timer cancel/complete paths when changing countdown or command logic.
