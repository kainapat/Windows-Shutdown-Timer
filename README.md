<div align="center">

<img src="off.png" alt="Windows Shutdown Timer" width="110" />

# Windows Shutdown Timer

**A precision power-management scheduler for Windows — built with Python & PySide6.**
*Elegant. Lightweight. Cinematic.*

<br/>

[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-4f8ef7?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.4%2B-43b89c?style=for-the-badge&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython-6/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D4?style=for-the-badge&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-f5c518?style=for-the-badge)](LICENSE)
[![Release](https://img.shields.io/github/v/release/kainapat/Windows-Shutdown-Timer?style=for-the-badge&color=7c3aed&logo=github)](../../releases)

</div>

---

## ✨ Overview

Windows Shutdown Timer is a **lightweight, modern power scheduler** that gives you full control over when your PC shuts down, restarts, sleeps, or hibernates. Wrapped in a **"Ethereal Glass" dark-mode UI** — an asymmetric Bento Grid dashboard with cinematic motion, dynamic glow accents, and buttery-smooth animations — it's the kind of utility that actually feels good to use.

> **ดาวน์โหลดใช้งานได้ทันที — ไม่ต้องติดตั้ง Python**  
> Grab the latest `.exe` from [Releases](../../releases) and run it directly.

---

## 🚀 Key Features
*ความสามารถหลัก*

### ⚡ Flexible Power Operations
| Action | Description |
|--------|-------------|
| 🔌 **Shutdown** | Powers off the computer completely |
| 🔄 **Restart** | Reboots the system cleanly |
| 😴 **Sleep** | Suspends to a low-power state instantly |
| 🌙 **Hibernate** | Saves the full session to disk and powers off |

### ⏱️ Precise Scheduling Modes
- **Quick Presets** — Schedule in one click: 15 min · 30 min · 1 hr · 2 hr
- **Specific Date & Time** — Pick an exact calendar date and target time
- **Countdown Timer** — Set custom intervals (hours · minutes · seconds, up to 24 h)

### 🎨 "Ethereal Glass" Bento Grid Dashboard
- **Asymmetric Bento Layout** — Organizes controls into a modern, multi-panel grid separating configuration from live countdowns
- **Dark / Light Theme Switcher** — Toggle between *Ethereal Glass* (OLED black) and *Warm Premium Cream* at any time; preference is restored on next launch
- **Cinematic Motion** — Horizontal slide transitions for input switching; spring-back physics on button clicks
- **Dynamic Glow Accents** — Color palettes and radial background glows shift fluidly per power action
- **Monospace Countdown** — Digit-stable typography prevents layout jitter during live updates
- **Window Geometry Persistence** — Size and position are restored exactly as you left them (min 650 × 580 px)
- **Integrated Toast Overlay** — Non-blocking status notifications with slide-in / fade-out animations

### 🛡️ Robust Safety & Reliability
- **Atomic File Writes** — Config is written to a temp file then swapped atomically to prevent corruption
- **Conflict Prevention** — Cancels any existing Windows shutdown task before scheduling a new one
- **Silent Signal Handling** — `Ctrl+C` / `Ctrl+Break` aborts schedules gracefully without blocking dialogs

---

## 💻 System Requirements
*ข้อกำหนดระบบ*

| Requirement | Minimum |
|-------------|---------|
| **OS** | Windows 7 / 8 / 10 / 11 |
| **Python** *(source only)* | 3.12 or higher |
| **Dependency** | `PySide6 >= 6.4.0` |

---

## 📦 Installation & Setup
*การติดตั้ง*

### 🖥️ Standalone Executable *(Recommended)*
> Zero dependencies — just download and run.

1. Go to the [**Releases**](../../releases) tab
2. Download the latest `Windows Shutdown Timer.exe`
3. Double-click to launch — no Python required

### 🛠️ Developer Setup *(Run from Source)*

```bash
# 1. Clone the repository
git clone https://github.com/kainapat/Windows-Shutdown-Timer.git
cd Windows-Shutdown-Timer

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the application
python shutdown_timer.py
```

---

## 🔨 Building the Executable
*การ build เป็น .exe*

Compile a standalone executable with [PyInstaller](https://pyinstaller.org/):

```bash
# Install PyInstaller
pip install pyinstaller

# Build using the included spec file (recommended)
pyinstaller "Windows Shutdown Timer.spec" --clean
```

The compiled output is placed at `dist/Windows Shutdown Timer.exe`.

> **Note:** The spec file automatically bundles `off.png` and `off.ico` so the icon renders correctly in both dev mode and the frozen executable — no extra files needed alongside the `.exe`.

---

## 🗂️ Project Structure
*โครงสร้างโปรเจกต์*

```
Windows Shutdown Timer/
├── shutdown_timer.py            # Primary application source
├── requirements.txt             # Python dependencies
├── off.png                      # Source icon image
├── off.ico                      # Multi-resolution icon (16–256 px)
├── icon.ico                     # Legacy icon (kept for reference)
├── Windows Shutdown Timer.spec  # PyInstaller build spec
├── timer_config.json            # Active timer config (runtime-generated)
└── window_config.json           # Window geometry persistence
```

---

## ⚙️ How It Works
*หลักการทำงาน*

The app delegates power operations to native Windows CLI utilities — no third-party drivers required:

| Action | Command |
|--------|---------|
| Shutdown | `shutdown /s /t [seconds]` |
| Restart | `shutdown /r /t [seconds]` |
| Sleep | `rundll32.exe powrprof.dll,SetSuspendState 0,1,0` |
| Hibernate | `rundll32.exe powrprof.dll,SetSuspendState 1,1,0` |
| Cancel | `shutdown /a` |

---

## 🗃️ Configuration Files

| File | Purpose | Lifetime |
|------|---------|----------|
| `timer_config.json` | Scheduling variables (action, time, mode) | Cleared on exit |
| `window_config.json` | UI geometry, position & theme preference | Persists across sessions |

---

## 📋 Changelog

### `v1.9.0` — July 2026 · *Custom Application Icon*
- 🎨 **Multi-Resolution Icon** — Converted `off.png` → `off.ico` with six sizes (16 · 32 · 48 · 64 · 128 · 256 px); Windows always picks the sharpest for each context
- 🔗 **Runtime Icon Loading** — `setWindowIcon()` via `resource_path()` helper that resolves paths correctly in both dev and PyInstaller frozen mode
- 📦 **Executable Embedding** — Updated spec to embed `off.ico` as exe icon and bundle both assets as runtime data

### `v1.8.0` — June 2026 · *Theme Switcher & Warm Premium Cream Light Mode*
- ☀️ **Theme Toggle Button** — Elegant top-level toggle in the new window header
- 🌅 **Warm Premium Cream Light Theme** — High-end editorial light mode: soft radial pastel gradients, dark stone text, clean card shadows
- 💾 **Theme Persistence** — Chosen theme is saved and restored on next launch
- 🐛 **Startup & Contrast Fixes** — Resolved blank button rendering, increased QPushButton contrast, fixed QMessageBox dark-text on Windows

### `v1.7.0` — June 2026 · *Bento Grid UI & Cinematic Motion Redesign*
- 🏗️ **Asymmetric Bento Grid** — Concentric Bento Box panels for optimal visual hierarchy
- 🎬 **Cinematic Slide & Haptic Motion** — `SlidingStackedWidget` transitions and physics-based button compression
- ✨ **Glow & Accent System** — Neon gradients and radial glows shift with each power action

### `v1.6.0` — June 2026 · *Ethereal Glass UI/UX & Silent Interrupts*
- 🌑 **Ethereal Glass Theme** — OLED-black (`#09090b`) background, dynamic glowing accents, concentric glass boundaries
- 🔇 **Silent Interrupt Handling** — Graceful abort on `Ctrl+C` / `Ctrl+Break` without blocking popups

### `v1.5.0` — June 2026 · *Resizable UI & Geometry Persistence*
- 🔓 **Resizable Window** — Unlocked above 600 × 680 px minimum
- 💾 **Geometry Persistence** — Position & dimensions saved to `window_config.json` on exit
- 🗂️ **Settings Separation** — Layout geometry isolated from timer settings

### `v1.4.0` — March 2026 · *Terminal Logging & Code Cleanup*
- 📟 **Timestamped Logs** — `HH:MM:SS │ message` format with context emoji
- 🧹 **Code Cleanup** — Removed unused imports and dead variables

### `v1.3.0` — March 2026 · *UI/UX Improvements*
- 🏷️ **Action Icons** — Streamlined dropdown with flat emoji indicators (🔌 🔄 😴 🌙)
- 🔢 **Monospace Countdown** — Digit-stable countdown via monospace font selectors

### `v1.2.0` — March 2026 · *Bug Fixes & Stability*
- 🩹 **Memory Leak Fix** — Active QTimer instances stopped on window close
- 🔒 **Atomic File Config** — Fixed cross-drive filesystem errors with local atomic rename

---

## 📄 License

This project is licensed under the **[MIT License](LICENSE)** — free to use, modify, and distribute.

<div align="center">

Made with ☕ and too many late nights · [kainapat](https://github.com/kainapat)

</div>
