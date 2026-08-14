# Windows Shutdown Timer Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Refactor the Windows Shutdown Timer PySide6 application UI into a high-contrast, modern, 3-Step Vertical Flow with Windows 11 Fluent styling.

**Architecture:** Replace the 5-card Bento grid in `shutdown_timer.py` with a top-to-bottom layout (Hero Countdown Display -> Step 1 Action Selector -> Step 2 Time & Presets -> Step 3 Action Controls). Overhaul all QSS stylesheets to fix text contrast 100% in Dark and Light modes.

**Tech Stack:** Python 3.10+, PySide6 (Qt for Python), Custom QSS, QPropertyAnimation.

## Global Constraints
- High contrast: WCAG AA compliant text colors (`#f4f4f5` dark mode, `#1e293b` light mode).
- Retain 100% of existing shutdown, restart, sleep, hibernate, toast, system tray, and config saving features.
- Single file modification: `shutdown_timer.py`.

---

### Task 1: Color Palette & Custom Widget High-Contrast Styling Refactor

**Files:**
- Modify: `shutdown_timer.py:73-125` (Theme dictionary and constants)
- Modify: `shutdown_timer.py:210-233` (`BentoCard` widget contrast styling)

**Interfaces:**
- Consumes: PySide6 `QFrame`, `QLabel`, `QGraphicsDropShadowEffect`
- Produces: `ACTION_COLORS` updated dictionary with high-contrast surface and text tokens

- [ ] **Step 1: Update `ACTION_COLORS` dictionary**

Update `ACTION_COLORS` in `shutdown_timer.py` to use high-contrast text and vibrant Fluent accents:

```python
ACTION_COLORS = {
    0: {  # Shutdown - Red Accent
        "name": "shutdown",
        "primary": "#ff3b5c",
        "secondary": "#ff8599",
        "accent": "#e6002e",
        "bg_gradient_end": "#18060a",
        "progress": "#ff3b5c",
        "icon": "🔌",
        "label": "ปิดเครื่อง",
    },
    1: {  # Restart - Orange Accent
        "name": "restart",
        "primary": "#ff9500",
        "secondary": "#ffc470",
        "accent": "#d67d00",
        "bg_gradient_end": "#180c05",
        "progress": "#ff9500",
        "icon": "🔄",
        "label": "รีสตาร์ท",
    },
    2: {  # Sleep - Blue Accent
        "name": "sleep",
        "primary": "#007aff",
        "secondary": "#70b4ff",
        "accent": "#0056b3",
        "bg_gradient_end": "#050c18",
        "progress": "#007aff",
        "icon": "😴",
        "label": "พักเครื่อง",
    },
    3: {  # Hibernate - Purple Accent
        "name": "hibernate",
        "primary": "#a855f7",
        "secondary": "#d8b4fe",
        "accent": "#7e22ce",
        "bg_gradient_end": "#120518",
        "progress": "#a855f7",
        "icon": "🌙",
        "label": "จำศีล",
    },
}
```

- [ ] **Step 2: Update `BentoCard` class for guaranteed text contrast**

In `shutdown_timer.py`, update `BentoCard` title label styling so title text is crisp `#f4f4f5` (dark) or `#1e293b` (light) instead of dark low-contrast colors:

```python
class BentoCard(QFrame):
    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("bentoCard")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(12)
        
        if title:
            self.title_label = QLabel(title)
            self.title_label.setObjectName("bentoCardTitle")
            font = QFont("Segoe UI Variable Display", 11, QFont.DemiBold)
            self.title_label.setFont(font)
            self.layout.addWidget(self.title_label)
```

- [ ] **Step 3: Test python compilation**

Run: `python -m py_compile shutdown_timer.py`
Expected: Return 0 with no syntax errors.

- [ ] **Step 4: Commit**

```bash
git add shutdown_timer.py
git commit -m "refactor: update ACTION_COLORS and BentoCard title styling for high contrast"
```

---

### Task 2: Refactor UI Architecture to 3-Step Vertical Flow in `ShutdownTimerApp`

**Files:**
- Modify: `shutdown_timer.py:425-650` (`ShutdownTimerApp.init_ui`)

**Interfaces:**
- Consumes: PySide6 `QVBoxLayout`, `QHBoxLayout`, `QButtonGroup`, `QSpinBox`, `QPushButton`
- Produces: Clean 3-step vertical flow layout

- [ ] **Step 1: Re-architect `init_ui` layout structure**

Replace the 5-card grid layout with:
1. **Header Layout**: Title + Dark/Light Theme Button
2. **Hero Card**: Monospace Countdown Digits (`00:00:00`), Progress Bar, Status Label
3. **Step 1 Card (เลือกการกระทำ)**: Action Pill Buttons (Shutdown, Restart, Sleep, Hibernate)
4. **Step 2 Card (กำหนดเวลา)**: Quick Preset Chips + Mode Switcher + SpinBox Inputs
5. **Step 3 Card (ควบคุมระบบ)**: Large Primary Start Button + Cancel / Clear

- [ ] **Step 2: Connect signals and handlers**

Wire preset chip clicks, action pill changes, spinbox value updates, and start/cancel buttons.

- [ ] **Step 3: Test python compilation & launch GUI**

Run: `python -m py_compile shutdown_timer.py`
Expected: Return 0 with no syntax errors.

- [ ] **Step 4: Commit**

```bash
git add shutdown_timer.py
git commit -m "feat: refactor ShutdownTimerApp UI to 3-step vertical flow"
```

---

### Task 3: Comprehensive QSS QStyleSheet Overhaul & Verification

**Files:**
- Modify: `shutdown_timer.py:800-1100` (`ShutdownTimerApp.apply_styles` and `update_theme_colors`)

**Interfaces:**
- Consumes: PySide6 QSS engine
- Produces: Clean, accessible Fluent QSS theme rules for Dark and Light modes

- [ ] **Step 1: Rewrite QSS rules in `apply_styles`**

Ensure:
- Card backgrounds: Dark `#18181b` (border `#27272a`), Light `#ffffff` (border `#e2e8f0`)
- Title labels (`#bentoCardTitle`): Dark `#f4f4f5`, Light `#1e293b`
- SpinBoxes / ComboBoxes / LineEdits: Dark `#27272a` bg with `#f4f4f5` text, Light `#f1f5f9` bg with `#0f172a` text
- Preset chips: Elevated pill buttons with hover scale
- Primary CTA Start button: Accent color background with white bold text

- [ ] **Step 2: Verify application launch and test UI manually**

Run: `python shutdown_timer.py`
- Verify Dark mode contrast & Light mode contrast
- Verify Preset chip clicks
- Verify Countdown start, pause, cancel

- [ ] **Step 3: Commit**

```bash
git add shutdown_timer.py
git commit -m "style: overhaul QSS stylesheets for 100% high contrast in Dark and Light modes"
```
