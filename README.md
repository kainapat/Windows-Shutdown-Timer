# Windows Shutdown Timer

A lightweight, modern Windows shutdown, restart, sleep, and hibernate scheduler built with Python and PySide6. It features a responsive, customizable "Ethereal Glass" dark-mode interface with automatic window size and position persistence.

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.4+-green.svg)](https://doc.qt.io/qtforpython-6/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Key Features

### 1. Flexible Operations
- **Shutdown**: Powers off the computer.
- **Restart**: Reboots the system.
- **Sleep**: Suspends the session to low-power state.
- **Hibernate**: Saves session state to disk and powers off.

### 2. Precise Scheduling
- **Quick Presets**: Rapidly schedule events for 15 minutes, 30 minutes, 1 hour, or 2 hours.
- **Specific Time**: Pick a precise calendar date and target time.
- **Countdown Timer**: Specify custom intervals down to hours, minutes, or seconds (up to 24 hours).

### 3. "Ethereal Glass" Interface
- **Window Geometry Persistence**: Automatically records your custom window dimensions and desktop coordinates on exit, restoring them on the next launch.
- **Monospace Countdown**: Monospace typography prevents digit layout jitter during real-time countdown updates.
- **Dynamic Accent Colors**: Adjusts the interface's color accents dynamically according to the selected power action.
- **Integrated Toast Overlay**: Custom non-overlapping status notifications with built-in memory management.

### 4. Robust Safety Defaults
- **Atomic File Serialization**: Settings are written to temporary files before replacing active configurations to avoid disk write corruption.
- **Shorter Command Locks**: Automatically cancels existing active Windows shutdown tasks prior to initiating new ones to prevent conflict.
- **Silent Signal Handling**: Gracefully handles terminal interrupt signals (`Ctrl+C` or `Ctrl+Break`) to abort active jobs silently, bypassing blocking graphical dialog prompts.

---

## System Requirements

- **OS**: Windows 7 / 8 / 10 / 11
- **Python**: 3.12 or higher (to run from source)
- **Dependencies**:
  - `PySide6 >= 6.4.0`

---

## Installation & Setup

### Standalone Executable (Recommended for General Users)
1. Download the latest pre-compiled `.exe` file from the [Releases](../../releases) tab.
2. Double-click to open. No Python installation required.

### Developer Setup (Running from Source)
1. **Clone the repository**:
   ```bash
   git clone https://github.com/kainapat/Windows-Shutdown-Timer.git
   cd Windows-Shutdown-Timer
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Launch the application**:
   ```bash
   python shutdown_timer.py
   ```

---

## Building the Executable

To compile the application into a standalone executable using PyInstaller:

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Generate the build**:
   ```bash
   pyinstaller --onefile --windowed --name="Windows Shutdown Timer" --icon=icon.ico shutdown_timer.py
   ```

3. Find the compiled output in `dist/Windows Shutdown Timer.exe`.

---

## Project Structure

```
Windows Shutdown Timer/
├── shutdown_timer.py          # Primary application source code
├── requirements.txt           # Dependencies listing
├── icon.ico                   # Executable application icon
├── off.png                    # Graphic interface asset
├── Windows Shutdown Timer.spec # PyInstaller compilation spec sheet
├── timer_config.json          # Active timer configuration (runtime generated)
└── window_config.json         # Window size and positioning configs
```

---

## How It Works

Under the hood, the application invokes native Windows Command Line utilities:
- **Shutdown**: `shutdown /s /t [seconds]`
- **Restart**: `shutdown /r /t [seconds]`
- **Sleep**: `rundll32.exe powrprof.dll,SetSuspendState 0,1,0`
- **Hibernate**: `rundll32.exe powrprof.dll,SetSuspendState 1,1,0`
- **Cancel**: `shutdown /a`

---

## Configuration Details

Timer inputs and window dimensions are isolated into separate configuration files:
- **`timer_config.json`** records scheduling variables and is cleaned up on exit.
- **`window_config.json`** tracks UI geometries and persists permanently across sessions.

---

## Changelog

### v1.5.1 (June 2026) - Graceful Terminal Interrupt
- **Silent Interrupt Handling**: Aborts schedules silently on `Ctrl+C` or `Ctrl+Break` terminal signals, skipping blocking confirmation message popups.

### v1.5.0 (June 2026) - Resizable Window & Settings Separation
- **Ethereal Glass Theme**: Restyled UI to OLED-black (#09090b) background with glowing dynamic accents, concentric boundaries, and custom glass button presets.
- **Resizable Layout & Constraints**: Unlocked resizability above a fixed minimum threshold of 600x680px.
- **Geometry Persistence**: Saves window dimensions and positions into `window_config.json` on close, reloading them on startup.

### v1.4.0 (March 2026) - Terminal Logging & Code Cleanup
- **Terminal Logging**: Added timestamped logs (`HH:MM:SS │ message`) featuring context-specific emoji symbols.
- **Code Optimization**: Removed unused Qt widget imports and dead code variables to slim compiler output.

### v1.3.0 (March 2026) - UI/UX Improvements
- **Action Icons**: Streamlined dropdown options with flat emoji indicators (🔌, 🔄, 😴, 🌙).
- **Monospace Countdown**: Stabilized countdown timers via monospace font family selectors.

### v1.2.0 (March 2026) - Bug Fixes & Stability
- **Memory Leak Fix**: Stopped active QTimer instances on window close to avoid orphaned background tasks.
- **Atomic File Config**: Resolved cross-drive filesystem copy errors via local directory atomic rename processes.

---

## License

This project is licensed under the **MIT License**. Feel free to use, modify, and distribute it.
