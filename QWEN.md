# Windows Shutdown Timer - Project Context

## Project Overview

A beautiful, user-friendly Windows shutdown/restart/sleep/hibernate timer application built with **Python** and **PySide6**. Features a modern dark mode UI with dynamic color themes, toast notifications, and automatic settings persistence.

**Key Features:**
- Four action modes: Shutdown, Restart, Sleep, Hibernate
- Quick preset buttons (15min, 30min, 1hr, 2hr)
- Multiple timer modes: Specific datetime, countdown (hours/minutes/seconds)
- Real-time progress bar with percentage + remaining time display
- Toast notifications with proper memory management
- Auto-save/load configuration (`timer_config.json`)
- Dynamic color themes per action (Red/Orange/Blue/Purple)

## Tech Stack

- **Language:** Python 3.12+
- **GUI Framework:** PySide6 (Qt6) >= 6.4.0
- **Build Tool:** PyInstaller 6.16+
- **Platform:** Windows 7/8/10/11 only

## Project Structure

```
Windows Shutdown Timer/
├── shutdown_timer.py          # Main application (1230 lines)
├── requirements.txt           # Python dependencies
├── Windows Shutdown Timer.spec # PyInstaller spec file
├── icon.ico                   # Application icon
├── off.png                    # Additional resource
├── timer_config.json          # Runtime config (auto-generated, gitignored)
├── .github/workflows/
│   └── build-release.yml      # GitHub Actions for auto build/release
├── build/                     # Build artifacts (gitignored)
└── dist/                      # Compiled executable (gitignored)
```

## Building and Running

### Run from Source
```bash
pip install -r requirements.txt
python shutdown_timer.py
```

### Build Executable (.exe)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name="Windows Shutdown Timer" --icon=icon.ico shutdown_timer.py
```
Output: `dist/Windows Shutdown Timer.exe`

### Auto-Build via GitHub Actions
- Push a tag `v*` (e.g., `v1.3.0`) to trigger automatic build and release
- Workflow builds `.exe` and creates GitHub Release with artifact

## Development Conventions

### Code Style
- **Imports:** Standard library → PySide6 imports grouped by module
- **Naming:** `snake_case` for functions/variables, `PascalCase` for classes
- **Constants:** `UPPER_CASE` (e.g., `CONFIG_FILE`, `ACTION_COLORS`, `PRESETS`)
- **Docstrings:** Present for class methods with clear parameter descriptions

### Architecture Patterns
- **Main Class:** `ShutdownTimerApp(QMainWindow)` - single-file architecture
- **Custom Widgets:** `PresetCard(QPushButton)`, `Toast(QWidget)`
- **State Management:** Instance variables track timer state (`is_timer_active`, `target_shutdown_time`, etc.)
- **Dynamic Styling:** Theme colors applied via `update_theme_colors()` triggered by action combo box

### Color System
Actions have themed colors defined in `ACTION_COLORS` dict:
| Index | Action | Primary | Icon |
|-------|--------|---------|------|
| 0 | Shutdown | Red (`#f38ba8`) | 🔌 |
| 1 | Restart | Orange (`#fab387`) | 🔄 |
| 2 | Sleep | Blue (`#89b4fa`) | 😴 |
| 3 | Hibernate | Purple (`#cba6f7`) | 🌙 |

### Testing Practices
- Manual testing via GUI interaction
- Error handling for subprocess calls (shutdown commands)
- Logger for debugging (`logging.INFO` level)

### Key Implementation Details

#### Timer Commands (Windows API)
```python
# Shutdown: shutdown /s /t [seconds]
# Restart:  shutdown /r /t [seconds]
# Sleep:    rundll32.exe powrprof.dll,SetSuspendState 0,1,0
# Hibernate: rundll32.exe powrprof.dll,SetSuspendState 1,1,0
# Cancel:   shutdown /a
```

#### Configuration File Format
```json
{
    "action": 0,
    "mode": 1,
    "date": "2026-03-02",
    "time": "20:00",
    "hours": 2,
    "minutes": 30,
    "seconds": 0
}
```

#### Safety Features
- Atomic file writes for config (temp file + `os.replace()`)
- Input validation (max 24 hours)
- Auto-cancel previous schedules before new ones
- Proper QTimer cleanup in `closeEvent()`
- Toast memory leak prevention (`deleteLater()` pattern)

#### UI/UX Highlights
- Fixed-pitch monospace font for countdown (prevents digit jiggling)
- Glassmorphism preset cards with hover shadow effects
- Slide-in/out toast animations
- Progress bar shows `% - เหลือ MM:SS` format
- Thai language UI throughout

## Common Tasks

### Adding New Actions
1. Add entry to `ACTION_COLORS` dict with color scheme
2. Add combo box item in `init_ui()`
3. Update `action_map` in `start_timer()`

### Modifying Timer Logic
- Core countdown: `update_countdown()` method (called every 1000ms)
- Timer start: `start_timer()` or `start_preset_timer()`
- Timer cancel: `cancel_timer()`

### Styling Changes
- Base styles: `apply_styles()` method
- Dynamic theme: `update_theme_colors()` method
- Color values: `ACTION_COLORS` dict at module level

## Known Limitations
- Windows-only (uses `shutdown` command)
- Sleep/Hibernate execute immediately (no countdown)
- Requires Administrator privileges for some shutdown operations
- Fixed window size (600×680px)

## Version History
- **v1.3.0** (March 2026): UI/UX improvements, emoji icons, progress bar enhancements
- **v1.2.0**: Bug fixes (memory leaks, race conditions, config file errors)
- **v1.1.0**: UI polish (progress bar color, font improvements)
- **v1.0.0**: Initial release
