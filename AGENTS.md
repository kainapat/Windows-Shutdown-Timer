# AGENTS.md - Development Guide

## Overview

Windows desktop app using Python + PySide6 (Qt) for scheduling shutdown/restart/sleep/hibernate.

## Project Structure

```
shutdown_timer.py     # Main app (~1155 lines, single file)
requirements.txt      # PySide6>=6.4.0
Windows Shutdown Timer.spec  # PyInstaller config
icon.ico              # App icon
.github/workflows/    # CI/CD (auto-build on tag push)
build/, dist/        # Build artifacts
```

## Commands

### Install & Run
```bash
pip install -r requirements.txt
python shutdown_timer.py
```

### Build Executable
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="Windows Shutdown Timer" --icon=icon.ico shutdown_timer.py
# Output: dist/Windows Shutdown Timer.exe
```

### CI/CD Release
```bash
git tag v1.0.0 && git push origin v1.0.0
```

### Testing
- **No test suite currently exists**
- If adding tests: use `pytest`, mock `subprocess.run`, use `pytest-qt` for UI
- Run single test: `pytest tests/test_file.py::test_function_name`

## Code Style

### Python 3.12+ | Single-file app | Follow existing patterns

### Imports (shutdown_timer.py:3-53)
```python
# Stdlib first
import sys, os, json, subprocess
from datetime import datetime, timedelta

# Third-party (PySide6)
from PySide6.QtWidgets import (...)
from PySide6.QtCore import (...)
from PySide6.QtGui import (...)
```

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Classes | PascalCase | `ShutdownTimerApp`, `PresetCard`, `Toast` |
| Methods | camelCase | `start_timer`, `update_countdown` |
| Constants | UPPER_SNAKE | `CONFIG_FILE`, `ACTION_COLORS` |
| Private | _camelCase | `_execute_sleep_hibernate` |

### Type Hints
Not currently used. If added: `def start_timer(self) -> None:`

### Error Handling
```python
try:
    subprocess.run(["shutdown", cmd, "/t", str(secs)], check=True)
    self.show_toast("Success", "success")
except Exception as e:
    self.show_toast(f"Failed: {e}", "error")
```

### Qt Patterns
```python
# Widget
self.label = QLabel("--:--:--")
self.label.setAlignment(Qt.AlignCenter)

# Timer
self.timer = QTimer()
self.timer.timeout.connect(self.update_countdown)
self.timer.start(1000)

# Layout
layout = QVBoxLayout(widget)
layout.setSpacing(18)
layout.setContentsMargins(24, 24, 24, 24)
```
Use full Qt enums: `Qt.PointingHandCursor`, not integers.

### String Formatting
Use f-strings: `f"{hours:02d}:{minutes:02d}:{seconds:02d}"`

### File I/O
Always use `encoding="utf-8"`, wrap in try/except.

## Key Classes

| Class | Purpose |
|-------|---------|
| `ShutdownTimerApp` | Main window, UI + timer logic |
| `PresetCard` | Glassmorphism preset button |
| `Toast` | Notification popup |

## Important Methods

`init_ui()` | `apply_styles()` | `update_theme_colors()` | `start_timer()` | `cancel_timer()` | `update_countdown()` | `show_toast()` | `save_settings()` / `load_settings()`

## Configuration

- Saves to `timer_config.json` on timer start
- Deleted on: app close, clear button, timer completion
- Platform: Windows-only (uses `shutdown` command)
- App ID: `"mycompany.myproduct.subproduct.version"` (ctypes.windll)

## Optional Linting

```bash
pip install ruff
ruff check shutdown_timer.py
ruff format shutdown_timer.py
```

## Adding Features

### New Timer Mode
1. Add radio button in `init_ui()`
2. Add page to `time_stack`
3. Handle in `start_timer()`

### New Theme Color
1. Add to `ACTION_COLORS` dict
2. Update `update_theme_colors()`

## Troubleshooting

- **Won't start**: `pip install -r requirements.txt`
- **Timer fails**: Run as Administrator
- **Build fails**: Ensure PyInstaller + icon.ico

## Notes

- Single-file app - all code in `shutdown_timer.py`
- No tests exist - add `pytest` tests for new features
- Thai UI text used
- Dark theme (Catppuccin-inspired)
- Subprocess calls handle actual power operations
