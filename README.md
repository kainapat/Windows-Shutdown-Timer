<div align="center">
  <br/>
  <img src="off.png" width="96" alt="Windows Shutdown Timer icon" />
  <br/><br/>

  <h1>Windows Shutdown Timer</h1>

  <p>Schedule a shutdown, restart, sleep, or hibernate on Windows.<br/>
  Built with Python and PySide6. No bloat. No background agents.</p>

  <br/>

  [![Python](https://img.shields.io/badge/Python-3.10+-4f8ef7?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)&nbsp;
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

> Requires Python 3.10+ on Windows 7 or later.

---

## What it does

Pick a power action and a time. The app schedules it and counts down. When the timer hits zero, Windows shuts down (or restarts, sleeps, or hibernates — whichever you chose). Cancel any time from inside the app or with `Ctrl+C` in the terminal.

**Scheduling modes**

| Mode | How it works |
|---|---|
| **Quick preset** | One click — 15 min, 30 min, 1 h, or 2 h from now |
| **Specific time** | Pick a date and exact clock time |
| **Countdown** | Set hours, minutes, seconds |

**The interface**

The UI features a **Simplified 3-Step Vertical Flow** designed with **Windows 11 Fluent Aesthetics**:
1. **Hero Countdown Display (Top)**: High-contrast monospace digits (`00:00:00`), glowing progress bar, and real-time status text.
2. **Step 1 — Select Action**: Quick segmented pill buttons for 🔌 Shutdown, 🔄 Restart, 😴 Sleep, or 🌙 Hibernate. Dynamic color accent shifts per action.
3. **Step 2 — Set Time**: Elevated Quick Preset chips + Segmented mode switcher ("Count Down" vs "Exact Time") + Spinner numeric inputs.
4. **Step 3 — System Controls**: Prominent Primary Action button + Cancel/Clear controls.

Available in both **Fluent Dark Mode** (Deep OLED black `#09090b`) and **Fluent Light Mode** (`#f8fafc`). Both modes deliver **100% WCAG AA text contrast** for effortless readability.

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

<details open>
<summary><strong>v2.0.0</strong> &nbsp;·&nbsp; August 2026 &nbsp;·&nbsp; <em>UX/UI Redesign & High Contrast Overhaul</em></summary>
<br/>

- **3-Step Vertical Flow**: Replaced 5-card Bento grid with a top-to-bottom logical flow (Hero Display -> Step 1 Action -> Step 2 Time & Presets -> Step 3 Controls).
- **100% WCAG AA Text Contrast**: Solved dark/light text readability issues across all card titles, labels, inputs, and buttons.
- **Dynamic Action Colors**: Active color accents shift automatically per action (Red for Shutdown, Orange for Restart, Blue for Sleep, Purple for Hibernate).
- **Quick Preset Chips**: Elevated `15m`, `30m`, `1h`, `2h` chips for instant 1-click scheduling.

</details>

<details>
<summary><strong>v1.9.0</strong> &nbsp;·&nbsp; July 2026 &nbsp;·&nbsp; <em>Custom Icon</em></summary>
<br/>

Converted `off.png` to `off.ico` with six embedded resolutions (16 → 256 px). Windows picks the sharpest size for each context (title bar, taskbar, Alt+Tab). A `resource_path()` helper resolves asset paths correctly in both dev and PyInstaller-frozen modes. The spec was updated to embed both icon files.

</details>

<details>
<summary><strong>v1.8.0</strong> &nbsp;·&nbsp; June 2026 &nbsp;·&nbsp; <em>Light Mode</em></summary>
<br/>

Added a theme toggle in the window header. The Light Mode uses soft pastel styling matched to the active power action. Theme choice persists across sessions.

</details>

---

## License

MIT
