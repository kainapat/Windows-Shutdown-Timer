<div align="center">
  <br/>
  <img src="off.png" width="96" alt="Windows Shutdown Timer icon" />
  <br/><br/>

  <h1>Windows Shutdown Timer</h1>

  <p>Schedule a shutdown, restart, sleep, or hibernate on Windows.<br/>
  Built with Python and PySide6. No bloat. No tray agent running in the background.</p>

  <br/>

  [![Python](https://img.shields.io/badge/Python-3.12+-4f8ef7?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)&nbsp;
  [![PySide6](https://img.shields.io/badge/PySide6-6.4+-43b89c?style=flat-square&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython-6/)&nbsp;
  [![Windows](https://img.shields.io/badge/Windows-7%2F8%2F10%2F11-0078D4?style=flat-square&logo=windows&logoColor=white)](https://www.microsoft.com/windows)&nbsp;
  [![License](https://img.shields.io/badge/License-MIT-f5c518?style=flat-square)](LICENSE)

  <br/><br/>

</div>

---

## Getting Started

```bash
git clone https://github.com/kainapat/Windows-Shutdown-Timer.git
cd Windows-Shutdown-Timer
pip install -r requirements.txt
python shutdown_timer.py
```

> Requires Python 3.12+ on Windows 7 or later.

---

## What it does

Pick a power action and a time. The app schedules it and counts down. When the timer hits zero, Windows shuts down (or restarts, sleeps, or hibernates — whichever you chose). Cancel any time from inside the app or with `Ctrl+C` in the terminal.

**Scheduling modes**

| Mode | How it works |
|---|---|
| **Quick preset** | One click — 15 min, 30 min, 1 h, or 2 h from now |
| **Specific time** | Pick a date and clock time |
| **Countdown** | Set hours, minutes, seconds up to 24 h |

**The interface**

The UI is built around an asymmetric Bento Grid layout with an "Ethereal Glass" dark theme — OLED black background, per-action glow accents (the color shifts depending on whether you picked Shutdown, Restart, Sleep, or Hibernate), slide transitions between input panels, and spring-back physics on buttons. There's also a Light Mode if you prefer that; the choice is saved.

Everything is native PySide6. No web renderer, no Electron, no external service.

---

## Under the Hood

The app calls native Windows CLI tools directly — no drivers, no services:

```
Shutdown   →  shutdown /s /t <seconds>
Restart    →  shutdown /r /t <seconds>
Sleep      →  rundll32.exe powrprof.dll,SetSuspendState 0,1,0
Hibernate  →  rundll32.exe powrprof.dll,SetSuspendState 1,1,0
Cancel     →  shutdown /a
```

A few reliability details: config is written atomically (temp file → rename) to survive power loss mid-write. Any existing Windows shutdown task is cancelled before a new one is scheduled. `Ctrl+C` / `Ctrl+Break` aborts silently — no confirmation dialog.

---

## Building a Standalone `.exe`

The included PyInstaller spec bundles the icon assets. Run:

```bash
pip install pyinstaller
pyinstaller "Windows Shutdown Timer.spec" --clean
```

Output lands at `dist/Windows Shutdown Timer.exe`. The icon (`off.ico`, six resolutions from 16 to 256 px) is embedded in the executable itself.

---

## Project Layout

```
Windows Shutdown Timer/
├── shutdown_timer.py             # All application code
├── requirements.txt              # PySide6 >= 6.4.0
├── off.png / off.ico             # App icon — source PNG and multi-res ICO
├── Windows Shutdown Timer.spec   # PyInstaller spec
├── timer_config.json             # Runtime — cleared on exit
└── window_config.json            # Window size, position, and theme
```

---

## Changelog

<details>
<summary><strong>v1.9.0</strong> &nbsp;·&nbsp; July 2026 &nbsp;·&nbsp; <em>Custom Icon</em></summary>
<br/>

Converted `off.png` to `off.ico` with six embedded resolutions (16 → 256 px). Windows picks the sharpest size for each context (title bar, taskbar, Alt+Tab). A `resource_path()` helper resolves asset paths correctly in both dev and PyInstaller-frozen modes. The spec was updated to embed both icon files.

</details>

<details>
<summary><strong>v1.8.0</strong> &nbsp;·&nbsp; June 2026 &nbsp;·&nbsp; <em>Light Mode</em></summary>
<br/>

Added a theme toggle in the window header. The Light Mode ("Warm Premium Cream") uses soft radial pastel gradients matched to the active power action, dark stone text, and clean card shadows. Theme choice persists across sessions. Also fixed blank QPushButton rendering on startup and the Windows QMessageBox dark-text bug.

</details>

<details>
<summary><strong>v1.7.0</strong> &nbsp;·&nbsp; June 2026 &nbsp;·&nbsp; <em>Bento Grid + Motion</em></summary>
<br/>

Reworked the layout into an asymmetric Bento Grid. Added `SlidingStackedWidget` for horizontal panel transitions and physics-based compression on button clicks. Background glow color shifts per power action.

</details>

<details>
<summary><strong>v1.6.0</strong> &nbsp;·&nbsp; June 2026 &nbsp;·&nbsp; <em>Ethereal Glass Theme</em></summary>
<br/>

New dark theme: OLED black (`#09090b`), dynamic glow accents, concentric glass card borders. Added silent `Ctrl+C` / `Ctrl+Break` handling — aborts the schedule without opening a dialog.

</details>

<details>
<summary><strong>v1.5.0</strong> &nbsp;·&nbsp; June 2026 &nbsp;·&nbsp; <em>Resizable Window</em></summary>
<br/>

Window is now resizable above a 600 × 680 px minimum. Size and screen position are saved to `window_config.json` on exit and restored on next launch. Window geometry and timer settings are stored in separate files.

</details>

<details>
<summary><strong>v1.4.0 – v1.2.0</strong> &nbsp;·&nbsp; March 2026</summary>
<br/>

**v1.4.0** — Timestamped terminal logs (`HH:MM:SS │ message`). Dead code cleanup.

**v1.3.0** — Emoji indicators in the action dropdown (🔌 🔄 😴 🌙). Monospace font for the countdown to prevent digit-width jitter.

**v1.2.0** — Fixed a QTimer memory leak on window close. Fixed a cross-drive `os.rename` crash by using a local temp file for atomic writes.

</details>

---

## License

MIT
