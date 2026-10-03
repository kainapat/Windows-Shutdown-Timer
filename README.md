<div align="center">
  <br/>
  <img src="off.png" width="96" alt="Windows Shutdown Timer icon" />
  <br/><br/>

  <h1>Windows Shutdown Timer</h1>

  <p>Schedule Windows shutdown or restart, or trigger sleep / hibernate immediately.<br/>
  Modern Raycast / Linear Precision interface. Zero emoji clutter. Bilingual (EN | TH). Fixed utility footprint. No background bloat.</p>

  <br/>

  [![Python](https://img.shields.io/badge/Python-3.10+-4f8ef7?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)&nbsp;
  [![PySide6](https://img.shields.io/badge/PySide6-6.4+-43b89c?style=flat-square&logo=qt&logoColor=white)](https://doc.qt.io/qtforpython-6/)&nbsp;
  [![Windows](https://img.shields.io/badge/Windows-Desktop-0078D4?style=flat-square&logo=windows&logoColor=white)](https://www.microsoft.com/windows)&nbsp;
  [![License](https://img.shields.io/badge/License-MIT-f5c518?style=flat-square)](#license)

  <br/><br/>

  <a href="#getting-started">Get Started</a>
  &nbsp;·&nbsp;
  <a href="#highlights">Highlights</a>
  &nbsp;·&nbsp;
  <a href="#architecture-at-a-glance">Architecture</a>
  &nbsp;·&nbsp;
  <a href="#explore-the-architecture">Diagram Gallery</a>
  &nbsp;·&nbsp;
  <a href="#building-a-standalone-exe">Build</a>

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

> Requires Python 3.10+ on Windows. Exact OS compatibility depends on the installed PySide6 / Qt release.

---

## Highlights

| Capability | Current behavior |
|---|---|
| **Shutdown / Restart** | Schedule by relative duration or absolute clock time, with a live countdown |
| **Sleep / Hibernate** | Execute immediately after confirmation; no countdown is created |
| **Quick Presets** | `15m`, `30m`, `1h`, `2h` for Shutdown / Restart only |
| **Timer Mode** | Hours, minutes, and seconds with a 72-hour scheduling limit |
| **Clock Mode** | Calendar date + hour + minute target |
| **Localization** | Instant English / Thai UI switching |
| **Themes** | Eye-comfort Light and Deep Zinc Dark |
| **Runtime** | Native PySide6 desktop app; no Electron, web backend, driver, or background service |

> **Cancel and Reset are intentionally different.** **Cancel** aborts an active Windows shutdown / restart request. **Reset** only clears the UI/configuration. Closing the app stops the local countdown display but does not cancel a shutdown / restart already handed to Windows.

---

## Architecture at a Glance

The architecture view now separates ownership explicitly: **Desktop User** is an external actor, **PySide6 UI / Scheduler Controller / Countdown Engine / Settings Repository / Windows Power Gateway** are responsibilities inside the desktop application, and **Microsoft Windows** is the external platform that performs the final power operation.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./diagram/architecture-diagram-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./diagram/architecture-diagram-light.svg">
    <img src="./diagram/architecture-diagram-light.svg" width="100%" alt="Windows Shutdown Timer architecture diagram">
  </picture>
</p>

<p align="center">
  <a href="diagram/architecture-diagram-light.svg">Light SVG</a>
  &nbsp;·&nbsp;
  <a href="diagram/architecture-diagram-dark.svg">Dark SVG</a>
  &nbsp;·&nbsp;
  <a href="diagram/architecture-diagram-light.html">HTML artifact</a>
</p>

---

## Under the Hood

The app delegates power operations to Windows directly — no driver and no background service:

| Action | Current runtime path |
|---|---|
| **Shutdown** | `shutdown /s /t <seconds>` |
| **Restart** | `shutdown /r /t <seconds>` |
| **Sleep** | `rundll32.exe powrprof.dll,SetSuspendState 0,1,0` — immediate |
| **Hibernate** | `rundll32.exe powrprof.dll,SetSuspendState 1,1,0` — immediate |
| **Cancel scheduled shutdown/restart** | `shutdown /a` |

Runtime flow for a scheduled Shutdown / Restart:

```text
Desktop User
  → PySide6 UI
  → Scheduler Controller
  → confirm scheduled action
  → validate Timer / Clock target (future, non-zero, max 72h)
  → Windows Power Gateway
      → shutdown /a
      → shutdown /s|/r /t <seconds>
  → Microsoft Windows
  → start 1-second QTimer countdown
  → save timer settings with atomic JSON replacement
  → update status / progress in the UI
```

Runtime flow for immediate Sleep / Hibernate:

```text
Desktop User
  → PySide6 UI
  → Scheduler Controller
  → branch before Timer / Clock validation
  → confirm immediate action
  → Windows Power Gateway
      → rundll32.exe powrprof.dll,SetSuspendState ...
  → Microsoft Windows
  → update executing status in the UI
```

A few reliability details:
- Timer settings use temp-file + `os.replace()` atomic writes.
- Any existing Windows shutdown request is aborted before a new Shutdown / Restart schedule is created.
- `Ctrl+C` / `Ctrl+Break` calls `cancel_timer(confirm=False)` when the app still tracks an active schedule.
- **Reset is not Cancel**: Reset clears fields/configuration but does not issue `shutdown /a`.
- Closing the GUI stops the local QTimer and deletes the timer config, but a Shutdown / Restart already scheduled in Windows continues unless explicitly cancelled.
- Backward-compatibility proxies (`SpinBoxProxy`, `DateTimeProxy`, legacy aliases) preserve older configuration access patterns.

---

## Building a Standalone `.exe`

The included PyInstaller spec bundles all icon and SVG assets into a single standalone executable:

```bash
pip install pyinstaller
pyinstaller "Windows Shutdown Timer.spec" --clean
```

Output lands at `dist/Windows Shutdown Timer.exe`.

---

## Explore the Architecture

### Archify source artifact

The repository includes an Archify-generated interactive runtime architecture artifact with **7 semantic nodes** across the application and Windows platform boundaries. It supports node focus, verified source links, Node Finder, Semantic Lens, PATH Route Probe, deep links, Light/Dark themes, and canonical exports.

The primary authored route is:

```text
Desktop User
  → PySide6 UI
  → Scheduler Controller
  → Windows Power Gateway
  → Microsoft Windows
```

Countdown and Settings Repository remain separate responsibilities connected to the controller/UI rather than being treated as external platform services.

> GitHub displays repository HTML files as source. The Archify artifact is available at [`diagram/interactive/index.html`](diagram/interactive/index.html), with repository evidence pinned in [`diagram/interactive/candidate.json`](diagram/interactive/candidate.json).

### Diagram Guide

Each diagram answers a different architecture question. The set intentionally avoids using one diagram type to explain everything.

| Diagram | Standard / style | Scope | What it answers |
|---|---|---|---|
| **Architecture** | Layered runtime architecture | Actor → application responsibilities → Windows platform | Where runtime responsibility lives |
| **Component** | C4-style component view | Logical components inside the PySide6 desktop application | Which component depends on which |
| **Context** | DFD Context / Level 0 | Whole app as one process + external entities | What crosses the application boundary |
| **Data Flow** | DFD Level 1 | Processes 1.0–5.0, D1/D2 stores, external entities | How requests, state, preferences, and results move |
| **Sequence** | UML interaction | Start flow with scheduled vs immediate alt branches | What happens over time when the user presses Start |
| **System Context** | C4 Level 1 | User, Windows Shutdown Timer, Microsoft Windows | Where the software system sits in its environment |

### Diagram Gallery

These SVG previews render directly in the README and automatically switch between Light and Dark variants with the viewer's GitHub theme. The images themselves are intentionally not links, so clicking a diagram does not jump to a GitHub code view.

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./diagram/component-diagram-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./diagram/component-diagram-light.svg">
    <img src="./diagram/component-diagram-light.svg" width="49%" alt="Component diagram">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./diagram/context-diagram-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./diagram/context-diagram-light.svg">
    <img src="./diagram/context-diagram-light.svg" width="49%" alt="Context diagram">
  </picture>
</p>

<p align="center">
  <strong>Component</strong>
  ·
  <a href="diagram/component-diagram-light.svg">Light SVG</a>
  ·
  <a href="diagram/component-diagram-dark.svg">Dark SVG</a>
  ·
  <a href="diagram/component-diagram-light.html">HTML artifact</a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  <strong>Context</strong>
  ·
  <a href="diagram/context-diagram-light.svg">Light SVG</a>
  ·
  <a href="diagram/context-diagram-dark.svg">Dark SVG</a>
  ·
  <a href="diagram/context-diagram-light.html">HTML artifact</a>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./diagram/data-flow-diagram-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./diagram/data-flow-diagram-light.svg">
    <img src="./diagram/data-flow-diagram-light.svg" width="49%" alt="Data flow diagram">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./diagram/sequence-diagram-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./diagram/sequence-diagram-light.svg">
    <img src="./diagram/sequence-diagram-light.svg" width="49%" alt="Sequence diagram">
  </picture>
</p>

<p align="center">
  <strong>Data Flow</strong>
  ·
  <a href="diagram/data-flow-diagram-light.svg">Light SVG</a>
  ·
  <a href="diagram/data-flow-diagram-dark.svg">Dark SVG</a>
  ·
  <a href="diagram/data-flow-diagram-light.html">HTML artifact</a>
  &nbsp;&nbsp;|&nbsp;&nbsp;
  <strong>Sequence</strong>
  ·
  <a href="diagram/sequence-diagram-light.svg">Light SVG</a>
  ·
  <a href="diagram/sequence-diagram-dark.svg">Dark SVG</a>
  ·
  <a href="diagram/sequence-diagram-light.html">HTML artifact</a>
</p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./diagram/system-context-diagram-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="./diagram/system-context-diagram-light.svg">
    <img src="./diagram/system-context-diagram-light.svg" width="72%" alt="System context diagram">
  </picture>
</p>

<p align="center">
  <strong>System Context</strong>
  ·
  <a href="diagram/system-context-diagram-light.svg">Light SVG</a>
  ·
  <a href="diagram/system-context-diagram-dark.svg">Dark SVG</a>
  ·
  <a href="diagram/system-context-diagram-light.html">HTML artifact</a>
</p>

> The **Architecture** hero above plus these five focused views form the complete static diagram set. Matching SVG, PNG, and HTML artifacts live in [`diagram/`](diagram/).

### Diagram Verification

The static diagram set is generated from [`diagram/generate_diagrams.py`](diagram/generate_diagrams.py) at a shared **1280 × 720** canvas. Light and Dark variants use the same structural geometry.

The repository includes two repeatable checks:

- [`verify_geometry.py`](diagram/verify_geometry.py) — detects text collisions, label-mask/node overlap, connector intrusion through non-endpoint nodes, and canvas overflow.
- [`verify_render_match.py`](diagram/verify_render_match.py) — verifies browser-rendered HTML, standalone SVG, and exported PNG remain visually aligned.

The current set is designed around these invariants:

- no text overlaps another label, node, border, connector, or legend;
- no connector is clipped or routed through an unrelated node;
- DFD Context and DFD Level 1 keep the same external actors and boundary flows;
- the UML Sequence follows the real scheduled/immediate branches in `shutdown_timer.py`;
- C4-style views keep application responsibilities separate from Microsoft Windows;
- README previews use SVG and switch Light/Dark automatically with the GitHub theme.

### Architecture Decisions

- [ADR 0001 — Clickable Dropdown Time Selectors](docs/adr/0001-dropdown-time-selectors.md)
- [ADR 0002 — Raycast / Linear Modern Precision UI Redesign](docs/adr/0002-linear-precision-redesign.md)
- [ADR 0003 — Eye-Comfort Light Palette & Fixed Window Dimensions](docs/adr/0003-eye-comfort-light-palette-and-fixed-window.md)

### Regenerating static diagrams

```bash
cd diagram
python generate_diagrams.py
python export_png.py
python verify_geometry.py
python verify_render_match.py
```

`export_png.py` uses Playwright with an installed Chrome/Edge executable. `verify_geometry.py` checks text collisions, label-mask/node overlap, connector intrusion, and canvas overflow. `verify_render_match.py` checks that browser-rendered HTML, standalone SVG, and PNG exports stay visually aligned.

---

## Project Layout

```text
Windows Shutdown Timer/
├── shutdown_timer.py               # PySide6 application + scheduling logic
├── requirements.txt                # Runtime Python dependencies
├── Windows Shutdown Timer.spec     # PyInstaller build definition
├── off.png / off.ico               # Application icon assets
├── chevron_dark.svg
├── chevron_light.svg
├── CONTEXT.md                      # Canonical domain vocabulary
├── docs/adr/                       # Architecture Decision Records
│   ├── 0001-dropdown-time-selectors.md
│   ├── 0002-linear-precision-redesign.md
│   └── 0003-eye-comfort-light-palette-and-fixed-window.md
└── diagram/
    ├── architecture-diagram-{light,dark}.{html,svg,png}
    ├── component-diagram-{light,dark}.{html,svg,png}
    ├── context-diagram-{light,dark}.{html,svg,png}
    ├── data-flow-diagram-{light,dark}.{html,svg,png}
    ├── sequence-diagram-{light,dark}.{html,svg,png}
    ├── system-context-diagram-{light,dark}.{html,svg,png}
    ├── generate_diagrams.py
    ├── export_png.py
    ├── verify_geometry.py
    ├── verify_render_match.py
    └── interactive/
        ├── candidate.json           # Archify source with repository evidence
        └── index.html               # Interactive Architecture Explorer
```

Runtime-generated `timer_config.json` and `window_config.json` are intentionally ignored by Git.

---

## Changelog

<details open>
<summary><strong>Documentation Update</strong> &nbsp;·&nbsp; October 2026 &nbsp;·&nbsp; <em>Standards-Aligned Architecture Diagram Set</em></summary>
<br/>

- **Six purpose-specific diagrams**: Layered Architecture, C4-style Component, DFD Context / Level 0, DFD Level 1, UML Sequence, and C4 System Context / Level 1.
- **Theme-aware SVG README previews**: Light and Dark SVGs switch automatically with the GitHub theme while keeping identical geometry.
- **Runtime-aligned semantics**: Windows Power Gateway, Settings Repository, scheduled Shutdown/Restart, and immediate Sleep/Hibernate paths now match the real code paths.
- **Geometry QA**: Added `diagram/verify_geometry.py` to catch text overlap, connector intrusion, mask collisions, and viewBox overflow.
- **Interactive architecture sync**: Archify topology now mirrors the corrected runtime boundaries and source-backed relationships.

</details>

<details>
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
