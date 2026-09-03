<div align="center">
  <br/>
  <img src="off.png" width="96" alt="Windows Shutdown Timer icon" />
  <br/><br/>

  <h1>Windows Shutdown Timer</h1>

  <p>Schedule a shutdown, restart, sleep, or hibernate on Windows.<br/>
  Modern Raycast / Linear Precision interface. Zero emoji clutter. Bilingual (EN | TH). Fixed utility footprint. No background bloat.</p>

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

> Requires Python 3.10+ on Windows 7, 8, 10, or 11.

---

## What it does

Pick a power action and a duration or specific clock time. The app schedules it and counts down. When the timer hits zero, Windows executes the selected action (Shutdown, Restart, Sleep, or Hibernate). Cancel anytime from inside the app or with `Ctrl+C` in the terminal.

**Scheduling Modes**

| Mode | How it works |
|---|---|
| **Quick Presets** | Instant one-click chips: `15m`, `30m`, `1h`, or `2h` from now |
| **Timer (นับถอยหลัง)** | Precision discrete dropdowns for Hours (`0`–`24 hr`), Minutes (`0`–`59 min`), and Seconds (`0`–`59 sec`) |
| **Clock (ระบุเวลาจริง)** | Interactive date picker (calendar popup) + discrete hour (`00`–`23`) and minute (`00`–`59`) dropdowns |

**The Interface (Raycast / Linear Precision Style)**

1. **Precision Countdown Chronometer (Hero Card)**: High-contrast monospace digits (`00:00:00`), live LED status indicator dot (green when running), and a slim 3px micro-progress line.
2. **Action Selector (`ACTION`)**: Sleek pill buttons for `Shutdown`, `Restart`, `Sleep`, and `Hibernate` with monochrome vector SVG icons and desaturated semantic color accents.
3. **Duration & Mode (`DURATION`)**: Minimalist preset chips (`15m`, `30m`, `1h`, `2h`), segmented pill tab switch (`Timer` vs `Clock`) with zero native radio artifacts, and dropdown pickers with custom vector chevrons.
4. **Ergonomic Bottom Action Bar**: Unified bottom controls featuring secondary `Cancel` and `Reset` buttons on the left, and a prominent `Start Countdown` button on the right.
5. **Fixed Utility Footprint (520 × 560 px)**: Dedicated utility window sizing (similar to Windows Calculator / native widgets) that prevents awkward vertical stretching or detached buttons on high-resolution displays.

**Themes & Eye-Comfort Palette**

- **Eye-Comfort Light Mode**: Soft concrete grey canvas (`#D8D8D8`) with pure white layered cards (`#FFFFFF`) and subtle `#C0C0C0` borders to eliminate harsh glare and eye strain.
- **Deep Zinc Dark Mode**: Modern GitHub/Linear-inspired dark canvas (`#0d1117`) with `#161b22` card surfaces and `#30363d` subtle 1px borders.
- **Dedicated Dynamic Localization (`EN` | `TH`)**: Quick toggle button in the header cleanly switches the entire interface between English and Thai without messy parenthetical stacking.
- **Zero Emoji Slop**: 100% crisp vector SVG icons rendered via `PySide6.QtSvg` at High-DPI.

Everything is native PySide6. No web renderer, no Electron, no external background service.

---

## Under the Hood

The app calls native Windows CLI tools directly — no drivers, no background services:

```
Shutdown   →  shutdown /s /t <seconds>
Restart    →  shutdown /r /t <seconds>
Sleep      →  rundll32.exe powrprof.dll,SetSuspendState 0,1,0
Hibernate  →  rundll32.exe powrprof.dll,SetSuspendState 1,1,0
Cancel     →  shutdown /a
```

A few reliability details:
- Configuration is written atomically (temp file → atomic replace) to survive sudden power cut or crash mid-write.
- Any existing Windows shutdown task is automatically cancelled before scheduling a new one.
- `Ctrl+C` / `Ctrl+Break` aborts silently and cancels active schedules cleanly.
- Full backward-compatibility proxies (`SpinBoxProxy`, `DateTimeProxy`, legacy aliases) ensure 100% compatibility with older configs.

---

## Building a Standalone `.exe`

The included PyInstaller spec bundles all icon and SVG assets into a single standalone executable:

```bash
pip install pyinstaller
pyinstaller "Windows Shutdown Timer.spec" --clean
```

Output lands at `dist/Windows Shutdown Timer.exe`.

---

## Architecture & Documentation

- **Architecture Decision Records (ADRs)**: Located in [`docs/adr/`](docs/adr/):
  - [ADR 0001: Clickable Dropdown Time Selectors](docs/adr/0001-dropdown-time-selectors.md)
  - [ADR 0002: Raycast / Linear Modern Precision UI Redesign](docs/adr/0002-linear-precision-redesign.md)
  - [ADR 0003: Eye-Comfort Light Palette (#D8D8D8) & Fixed Window Dimensions](docs/adr/0003-eye-comfort-light-palette-and-fixed-window.md)
- **Architecture Diagrams**: Located in [`diagram/`](diagram/):
  - [`Component Diagram`](diagram/component-diagram.html): 3-Tier internal architecture
  - [`Context Diagram (Level 0)`](diagram/context-diagram.html): System boundary and interactions
  - [`Data Flow Diagram (DFD)`](diagram/data-flow-diagram.html): State lifecycle
  - [`Sequence Diagram`](diagram/sequence-diagram.html): Chronological execution & cancellation sequence

---

## Project Layout

```
Windows Shutdown Timer/
├── shutdown_timer.py             # Application code
├── requirements.txt              # PySide6 >= 6.4.0
├── off.png / off.ico             # App icon — PNG and multi-res ICO
├── chevron_dark.svg              # Dark theme vector caret
├── chevron_light.svg             # Light theme vector caret
├── Windows Shutdown Timer.spec   # PyInstaller spec
├── timer_config.json             # Runtime config — cleared on exit
├── window_config.json            # Window position, theme, and language
├── docs/adr/                     # Architecture Decision Records
│   ├── 0001-dropdown-time-selectors.md
│   ├── 0002-linear-precision-redesign.md
│   └── 0003-eye-comfort-light-palette-and-fixed-window.md
└── diagram/                      # Standalone Architecture & System Diagrams (HTML)
    ├── component-diagram.html
    ├── context-diagram.html
    ├── data-flow-diagram.html
    └── sequence-diagram.html
```

---

## Changelog

<details open>
<summary><strong>v2.4.0</strong> &nbsp;·&nbsp; September 2026 &nbsp;·&nbsp; <em>Raycast / Linear Precision Redesign & Eye-Comfort Palette</em></summary>
<br/>

- **Raycast / Linear Precision Aesthetics**: Completely redesigned the UI to an editorial precision desktop utility with subtle 1px borders, quiet section headers (`ACTION`, `DURATION`), and zero textbook numbering.
- **Zero Emoji Clutter**: Replaced all emojis with sharp, dynamically recolored vector SVG icons (`power`, `restart`, `moon`, `hibernate`, `globe`, `sun`, `play`, `cancel`, `reset`).
- **Dynamic Localization Engine (`EN` | `TH`)**: Instant language switching pill in the header; eliminated ugly parenthetical bilingual stacking.
- **Precision Chronometer Hero**: Tabular monospace digits, live LED status indicator dot, and a slim 3px micro-progress line.
- **Eye-Comfort Light Palette (`#D8D8D8`)**: Non-glaring concrete grey canvas with layered pure white cards and high-contrast dark zinc text.
- **Fixed Utility Footprint (520 × 560 px)**: Established a dedicated compact utility size preventing detached buttons or awkward empty space on widescreen monitors.
- **Segmented Pill Controls**: Built custom pushbutton-based segmented tab for `Timer` vs `Clock` with zero native Windows radio indicator artifacts.

</details>

<details>
<summary><strong>v2.3.0</strong> &nbsp;·&nbsp; September 2026 &nbsp;·&nbsp; <em>Clickable Dropdown Time Selectors & Symmetrical Layout</em></summary>
<br/>

- **Clickable Dropdown Time Selectors**: Replaced manual text-typing inputs with discrete `QComboBox` dropdowns and `QDateEdit` calendar popup.
- **Symmetrical 3-Column Layout**: Aligned both `Timer` and `Clock` modes into a balanced 3-column layout.
- **Backward-Compatible Proxy Layer**: Built `SpinBoxProxy` and `DateTimeProxy` adapters.

</details>

<details>
<summary><strong>v2.2.0</strong> &nbsp;·&nbsp; August 2026 &nbsp;·&nbsp; <em>Comprehensive Architecture & System Diagrams</em></summary>
<br/>

- **System Architecture Diagrams**: Added 4 interactive editorial diagrams (`Component`, `Context`, `Data Flow`, and `Sequence`) in [`diagram/`](diagram/).

</details>

<details>
<summary><strong>v2.1.0</strong> &nbsp;·&nbsp; August 2026 &nbsp;·&nbsp; <em>Soft Slate Grey Light Mode & Bilingual Loopless UI</em></summary>
<br/>

- **Soft Slate Grey Light Mode**: Initial eye-strain reduction palette.
- **Modern Loopless Typography**: Integrated Thai loopless font stack.

</details>

<details>
<summary><strong>v2.0.0</strong> &nbsp;·&nbsp; August 2026 &nbsp;·&nbsp; <em>UX/UI Redesign & High Contrast Overhaul</em></summary>
<br/>

- **3-Step Vertical Flow**: Replaced 5-card Bento grid with top-to-bottom flow.

</details>

---

## License

MIT
