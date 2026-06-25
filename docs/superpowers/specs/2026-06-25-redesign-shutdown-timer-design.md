# Design Spec: Redesign Windows Shutdown Timer (Ethereal Glass Bento UI)

**Date:** 2026-06-25  
**Status:** Draft  
**Author:** Vanguard UI Architect  
**Objective:** Upgrade the existing Windows Shutdown Timer PySide6 application into a high-end, premium "Ethereal Glass" Bento Grid dashboard. The interface will feature haptic micro-interactions, smooth kinetic animations, and a polished modular code structure completely free of "AI slop" or generic templates.

---

## 1. Visual Design System

We will implement a premium Dark-Tech design system optimized for PySide6 styling capabilities.

### 1.1 Color Palette
- **System Background:** Pure Vantablack/OLED Dark (`#050505`) with a subtle radial glow towards the bottom right using the active theme color (`#0c0c14` to `#140a0f` depending on action).
- **Cards (Glass Panels):** Multi-layered translucent panels (`rgba(15, 15, 20, 0.6)`) with `backdrop-filter: blur(25px)`.
- **Borders (Double-Bezel):**
  - **Outer Border:** `rgba(255, 255, 255, 0.04)` on the surrounding card frame.
  - **Inner Highlight Border:** `rgba(255, 255, 255, 0.08)` on the active card content area.
- **Dynamic Accents (Desaturated < 80% saturation for premium feel):**
  - **Shutdown (Red):** `Primary: #ff5277` (Muted Rose), `Secondary: #ff94ab`, `Glow: rgba(255, 82, 119, 0.15)`
  - **Restart (Orange):** `Primary: #ff9130` (Amber Tangerine), `Secondary: #ffc28d`, `Glow: rgba(255, 145, 48, 0.15)`
  - **Sleep (Blue):** `Primary: #3a86ff` (Slate Cyan/Sapphire), `Secondary: #8eb7ff`, `Glow: rgba(58, 134, 255, 0.15)`
  - **Hibernate (Purple):** `Primary: #a855f7` (Amethyst), `Secondary: #d8b4fe`, `Glow: rgba(168, 85, 247, 0.15)`

### 1.2 Typography
- **UI controls & labels:** `Segoe UI` or system Sans-Serif. Use weights `Light (300)`, `Regular (400)`, `Medium (500)`, `SemiBold (600)` to establish clear hierarchy.
- **Countdown clock:** `JetBrains Mono` or `Consolas` (fixed-width) to prevent layout shifting during clock ticks. Font size increased to `46pt` with subtle letter-spacing.

---

## 2. Layout Architecture (Asymmetrical Bento Grid)

Instead of the classic top-to-bottom stack, we will layout elements in a balanced, modern Bento Grid using a custom layout strategy:

```
+------------------------------------+------------------------------------+
|               PANEL A              |               PANEL B              |
|        Action & Time Mode          |          Time Input Stack          |
|  [Action Dropdown (Custom Styled)] |  [Stacked Widget for time settings|
|  [Radio buttons as custom pills]   |   - Datetime / Hours / Mins / Secs]|
|                                    |                                    |
+------------------------------------+------------------------------------+
|               PANEL C                                                   |
|           Active Monitor & Countdown Dashboard                          |
|  +-------------------------------------------------------------------+  |
|  |                          --:--:-- (JetBrains Mono)                |  |
|  |                 [Progress Bar - Muted Dynamic Gradient]           |  |
|  |                    "Status: Waiting for Timer"                    |  |
|  +-------------------------------------------------------------------+  |
+------------------------------------+------------------------------------+
|               PANEL D              |               PANEL E              |
|            Quick Presets           |           Control Actions          |
|  [15m]   [30m]   [1h]   [2h]        |  [Start Timer]  [Cancel]   [Clear] |
|  (Dynamic glass cards with hover)  |  (Pill buttons with haptic click)  |
+------------------------------------+------------------------------------+
```

### 2.1 Component Breakdown
- **Panel A (Action & Mode Selector):** Customized glass panel. QComboBox styled with a custom dropdown list, custom arrows, and glowing borders.
- **Panel B (Time Configuration Panel):** QStackedWidget integrated into a glass panel, displaying inputs based on the selected mode. Transition between stacks is accompanied by a slide-fade animation.
- **Panel C (Hero Countdown):** Spans the entire width of the dashboard. Features the massive monospace timer and a sleek gradient progress bar with micro-shadowing.
- **Panel D (Presets Board):** Grid of glass button cards with interactive hover effects.
- **Panel E (Control Board):** Custom styled action buttons. The "Start" button transitions dynamically according to the chosen theme accent color.

---

## 3. Motion & Animation Choreography (Cinematic Motion)

We will implement smooth native Qt animations using `QPropertyAnimation` and custom graphics effects:
1. **Time Mode Transition:** When switching time modes (e.g. from Datetime to Countdown), the input controls will slide horizontally and fade in/out using a cubic-bezier-like easing curve (`QEasingCurve.OutCubic`).
2. **Button Click Physics (Haptic Press):** Buttons will shrink slightly on press (`QGraphicsScale` or offset animation) and spring back on release to simulate physical hardware.
3. **Theme Color Cross-Fade:** When the active action changes (e.g. Shutdown -> Sleep), the stylesheet accent colors will transition smoothly rather than snapping instantly, using a timer-based color interpolation or localized QSS transitions.
4. **Toast Overlay Slide:** The notification toast will slide in smoothly from the top, hover, and fade out on completion.

---

## 4. Anti-AI Slop Standards

To ensure the codebase is robust, maintainable, and reflects senior-level engineering:
- **Clean Stylesheet Management:** Style sheets (QSS) will be structured cleanly, separating layout details from theme color assets. Avoid inline stylesheets inside widget creation.
- **Precise Layout Constraints:** Never hardcode coordinates; always use proper layouts (`QGridLayout`, `QHBoxLayout`, `QVBoxLayout`) with proportional stretch values.
- **Resource Lifecycle Management:** Active timers and animations will be explicitly stopped and disposed of during window closure to prevent memory leaks and background CPU utilization.
- **Strict Error Boundaries:** External `shutdown.exe` commands will be wrapped in try-except blocks, with concrete Windows API error code checking (e.g., handling Access Denied, No active timer to cancel).

---

## 5. Verification & Compilation Plan

### 5.1 Manual UI Audits
- Check that the window adjusts gracefully when resized (minimum size set to `650x580`).
- Verify digit positioning on the countdown clock (no jitter).
- Test all hover/press states on preset cards and control buttons.

### 5.2 Build Executable
- Use `pyinstaller` to compile the script into a standalone `.exe`:
  ```bash
  pyinstaller --onefile --windowed --name="Windows Shutdown Timer" --icon=icon.ico shutdown_timer.py
  ```
- Run the compiled `.exe` to verify all components initialize correctly, settings persist in `window_config.json`, and scheduled operations execute successfully.
