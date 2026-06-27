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

### 3. "Ethereal Glass" Bento Grid Dashboard
- **Bento Grid Layout**: Organizes the interface into a modern asymmetric grid of cards (Bento boxes) separating setup parameters from active countdowns.
- **Theme Switcher (Dark/Light Modes)**: Toggle seamlessly between the classic "Ethereal Glass" dark theme and a premium "Warm Premium Cream" light theme. The selected theme mode is stored persistently in `window_config.json` and restored automatically on next launch.
- **Cinematic Motion**: Implements horizontal slide transitions for input method switching and spring-back click physics on interactive buttons.
- **Window Geometry & Position Persistence**: Automatically records your custom window dimensions and desktop coordinates on exit, restoring them on the next launch (minimum bounds adjusted to 650x580px for optimal grid rendering).
- **Monospace Countdown**: Monospace typography prevents digit layout jitter during real-time countdown updates.
- **Dynamic Glow Accents**: Adjusts the interface's color accents and radial glow backgrounds dynamically according to the selected power action.
- **Integrated Toast Overlay**: Custom non-blocking status notifications with entry slide-down and exit fade animations.

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

### v1.8.0 (June 2026) - Theme Switcher & Warm Premium Cream Light Mode
- **Theme Toggle Button**: Added an elegant top-level theme toggle switch in the new window header layout.
- **Warm Premium Cream Light Mode**: Created a high-end editorial light theme featuring soft radial pastel gradients matched to the active shutdown action, dark stone text, and clean card shadows.
- **Theme Persistence**: Extends window settings to save the chosen theme mode, restoring it dynamically on application start.
- **Startup Visibility & Contrast Fixes**: Resolved blank button rendering on launch by initializing the toggle button text immediately, and increased QPushButton#themeButton contrast in both modes.
- **Bento Card Contrast & QMessageBox Fixes**: Enhanced bento card borders contrast (opacity up from 0.04 to 0.12) in dark mode for easier readability, and resolved the Windows QMessageBox dark-text bug by converting messages to plain text.

### v1.7.0 (June 2026) - Bento Grid UI & Cinematic Motion Redesign
- **Asymmetric Bento Grid Layout**: Rearranged the dashboard widgets into concentric Bento Box panels to optimize visual hierarchy.
- **Cinematic Slide & Haptic Motion**: Integrated custom `SlidingStackedWidget` slide transitions and physics-based button compression on clicks.
- **Glow & Accent System**: Re-tuned neon gradients and radial background glows to change fluidly with each action theme.

### v1.6.0 (June 2026) - Ethereal Glass UI/UX & Silent Interrupts
- **Ethereal Glass Theme**: Restyled UI to OLED-black (#09090b) background with glowing dynamic accents, concentric boundaries, and custom glass button presets.
- **Silent Interrupt Handling**: Aborts schedules silently on `Ctrl+C` or `Ctrl+Break` terminal signals, skipping blocking confirmation message popups.

### v1.5.0 (June 2026) - Resizable UI & Geometry Persistence
- **Resizable Layout & Constraints**: Unlocked window resizability above a fixed minimum threshold of 600x680px.
- **Geometry Persistence**: Saves window dimensions and position coordinates into `window_config.json` on exit, restoring the window state on the next launch.
- **Settings Separation**: Isolated layout geometries from timer settings, ensuring window sizes are preserved when clearing user timer inputs.

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
