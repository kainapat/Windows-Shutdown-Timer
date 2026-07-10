<div align="center">

<img src="off.png" alt="Windows Shutdown Timer" width="108" />

# Windows Shutdown Timer

A power-management scheduler for Windows built with Python and PySide6.

<br/>

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-4f8ef7?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.4%2B-43b89c?style=flat-square&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython-6/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?style=flat-square&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-f5c518?style=flat-square)](LICENSE)

</div>

---

Schedule a shutdown, restart, sleep, or hibernate — pick a time, walk away. The interface runs on PySide6 with an "Ethereal Glass" dark theme (asymmetric Bento Grid, per-action glow accents, slide transitions) and a Light Mode toggle if you prefer that.

## Features

**Power operations** — Shutdown, Restart, Sleep, Hibernate.

**Three scheduling modes:**
- Quick presets: 15 min / 30 min / 1 h / 2 h
- Specific date and clock time
- Countdown (up to 24 hours, any h/m/s combo)

**UI details worth mentioning:**
- Dark ↔ Light theme toggle, preference survives restarts
- Per-action color accents and radial background glow
- Monospace countdown digits — no layout jitter
- Window size and position remembered across sessions
- Non-blocking toast notifications

**Under the hood:**
- Delegates to native Windows commands (`shutdown /s`, `shutdown /r`, `rundll32 powrprof.dll` for sleep/hibernate)
- Atomic config writes to avoid corruption on sudden power loss
- Clears existing Windows shutdown tasks before scheduling a new one
- `Ctrl+C` / `Ctrl+Break` aborts silently without a dialog

---

## Getting Started

```bash
git clone https://github.com/kainapat/Windows-Shutdown-Timer.git
cd Windows-Shutdown-Timer
pip install -r requirements.txt
python shutdown_timer.py
```

Requires **Python 3.12+** and **Windows 7 or later**.

---

## Building a Standalone Executable

Uses PyInstaller. The included spec file bundles the icon assets automatically.

```bash
pip install pyinstaller
pyinstaller "Windows Shutdown Timer.spec" --clean
```

Output: `dist/Windows Shutdown Timer.exe`

---

## How the Commands Work

| Action | Windows command |
|--------|----------------|
| Shutdown | `shutdown /s /t <seconds>` |
| Restart | `shutdown /r /t <seconds>` |
| Sleep | `rundll32.exe powrprof.dll,SetSuspendState 0,1,0` |
| Hibernate | `rundll32.exe powrprof.dll,SetSuspendState 1,1,0` |
| Cancel | `shutdown /a` |

---

## Project Files

```
Windows Shutdown Timer/
├── shutdown_timer.py            # All application code lives here
├── requirements.txt
├── off.png / off.ico            # App icon (source + multi-res ICO)
├── Windows Shutdown Timer.spec  # PyInstaller build spec
├── timer_config.json            # Written at runtime, cleared on exit
└── window_config.json           # Window geometry + theme preference
```

---

## Changelog

### v1.9.0 — July 2026

Added a custom application icon. `off.png` was converted to `off.ico` with six resolutions (16 → 256 px) so Windows picks the right size per context. The spec was updated to embed both files; a `resource_path()` helper resolves them correctly whether running from source or frozen by PyInstaller.

### v1.8.0 — June 2026

Added a Light Mode. The toggle sits in the window header and switches between the original Ethereal Glass dark theme and a new Warm Premium Cream light theme (soft radial pastels, stone text, clean shadows). Theme choice is written to `window_config.json` and restored on next launch. Also fixed blank button rendering on startup and the Windows QMessageBox dark-text bug.

### v1.7.0 — June 2026

Reworked the layout into an asymmetric Bento Grid. Added `SlidingStackedWidget` for horizontal input transitions and physics-based button compression. Background glows now shift color per power action.

### v1.6.0 — June 2026

New Ethereal Glass theme — OLED black (`#09090b`), dynamic glow accents, concentric glass card borders. Added silent `Ctrl+C` / `Ctrl+Break` handling so terminal aborts don't pop a dialog.

### v1.5.0 — June 2026

Made the window resizable (min 600 × 680 px). Window size and position are now saved to `window_config.json` on exit and restored on launch. Timer config and window config are separate files.

### v1.4.0 — March 2026

Added timestamped terminal logs (`HH:MM:SS │ message`). Removed unused Qt imports and dead variables.

### v1.3.0 — March 2026

Dropdown now shows emoji indicators (🔌 🔄 😴 🌙). Countdown display switched to a monospace font to prevent digit-width jitter.

### v1.2.0 — March 2026

Fixed a QTimer memory leak on window close. Fixed a cross-drive `os.rename` error by using a local temp file for atomic writes.

---

## License

MIT — do whatever you want with it.
