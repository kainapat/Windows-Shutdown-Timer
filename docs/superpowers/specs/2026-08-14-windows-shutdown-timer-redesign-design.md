# Windows Shutdown Timer - UX/UI Redesign Spec

## Background & Problem Statement
The current Windows Shutdown Timer UI suffers from severe readability and usability issues:
1. **Critical Text Contrast Bug**: Section headers in both Dark and Light modes use low-contrast text colors (`#1a1a24`, `#888899`), rendering them almost unreadable against card backgrounds.
2. **Fragmented 5-Card Bento Grid Layout**: Essential controls (Action, Mode, Time Input, Presets, Countdown, System Controls) are scattered across 4 corners of the screen in 5 separate cards, forcing the user's eyes to jump continuously.
3. **Complex Input Controls**: 4 separate radio buttons ("วัน/เวลา", "ชั่วโมง", "นาที", "วินาที") switch stacked widgets, making quick timer setup cumbersome.

## Target Audience & Goal
Provide a modern, intuitive, accessible, and high-end Windows 11 desktop app interface. A user should be able to set a shutdown/restart timer in **1 click** (preset) or **2 clicks** (custom time) without confusion.

---

## Design System & Aesthetic (Windows 11 Fluent)

### 1. Color Palette & Contrast Standards
All text elements strictly meet WCAG AA contrast ratio standards (minimum 4.5:1 for body text, 3.0:1 for headers).

- **Dark Mode**:
  - Main Window Background: `#09090b` (Deep OLED Black)
  - Card Containers: `#18181b` (Zinc 900) with 1px border `#27272a` (Zinc 800)
  - Primary Text: `#f4f4f5` (Zinc 100)
  - Secondary Text: `#a1a1aa` (Zinc 400)
  - Card Header / Labels: `#e4e4e7` (Zinc 200) - **High Contrast Guaranteed**

- **Light Mode**:
  - Main Window Background: `#f8fafc` (Slate 50)
  - Card Containers: `#ffffff` (Pure White) with 1px border `#e2e8f0` (Slate 200) & subtle ambient shadow
  - Primary Text: `#0f172a` (Slate 900)
  - Secondary Text: `#64748b` (Slate 500)
  - Card Header / Labels: `#1e293b` (Slate 800) - **High Contrast Guaranteed**

- **Dynamic Accent Colors (per Action)**:
  - 🔌 **Shutdown (ปิดเครื่อง)**: Crimson Red (`#ff3b5c`)
  - 🔄 **Restart (รีสตาร์ท)**: Electric Amber (`#ff9500`)
  - 😴 **Sleep (พักเครื่อง)**: Radiant Cyan/Blue (`#007aff`)
  - 🌙 **Hibernate (จำศีล)**: Royal Purple (`#a855f7`)

### 2. Typography
- **UI Fonts**: `Segoe UI Variable Display`, `Segoe UI`, `Inter`, `Sans-Serif`
- **Timer Digits**: `JetBrains Mono`, `Consolas`, `Monospace` (Fixed pitch to prevent digit shaking)

---

## Layout Architecture: 3-Step Vertical Flow

```
┌──────────────────────────────────────────────────────────┐
│  🔌 Windows Shutdown Timer                [ 🌙 Light/Dark ]│
├──────────────────────────────────────────────────────────┤
│                                                          │
│   HERO DISPLAY                                           │
│   ┌──────────────────────────────────────────────────┐   │
│   │                 00 : 30 : 00                     │   │
│   │   [======================                    ]   │   │
│   │      สถานะ: กำลังนับถอยหลังปิดเครื่องในอีก 30 นาที  │   │
│   └──────────────────────────────────────────────────┘   │
│                                                          │
│   STEP 1: เลือกการกระทำ (Action)                         │
│   [ 🔌 ปิดเครื่อง ] [ 🔄 รีสตาร์ท ] [ 😴 พักเครื่อง ] [ 🌙 จำศีล ] │
│                                                          │
│   STEP 2: กำหนดเวลา (Time Setting)                        │
│   Quick Presets:  [ ⚡ 15 นาที ] [ ⚡ 30 นาที ] [ ⏰ 1 ชม. ] [ ⏰ 2 ชม. ] │
│   โหมด: (•) นับถอยหลัง (Timer)    ( ) ระบุเวลาจริง (Clock) │
│   เวลา: [ 00 ] ชม. : [ 30 ] นาที : [ 00 ] วินาที        │
│                                                          │
│   STEP 3: ควบคุมระบบ (Controls)                          │
│   [        ▶ เริ่มนับถอยหลัง (Start Timer)         ]   │
│   [  ✕ ยกเลิก (Cancel)  ]       [  ↺ ล้างค่า (Clear)  ]  │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Component Details

1. **Header**:
   - Clean top bar with application icon, title, and sleek pill toggle button for Dark/Light theme mode.

2. **Hero Countdown Card (Top)**:
   - Displays massive monospace digits (`00:00:00`).
   - Smooth animated progress bar glowing with the active action's accent color.
   - Status text in high contrast font indicating current state.

3. **Step 1: Action Selector**:
   - Horizontal pill buttons / tab selector with icons for Shutdown, Restart, Sleep, Hibernate.
   - Clicking an action instantly updates the accent theme color of the start button, progress bar, and active highlights.

4. **Step 2: Time Setting**:
   - **Quick Presets**: 4 elevated chip buttons (`15 นาที`, `30 นาที`, `1 ชม.`, `2 ชม.`). Clicking any chip immediately populates the time inputs and can auto-highlight.
   - **Mode Switcher**: Segmented toggle between "นับถอยหลัง" (Countdown timer) and "ระบุเวลาจริง" (Target date & time).
   - **Numeric Inputs**: Clean, high-contrast SpinBox numeric controls (Hours, Minutes, Seconds) or Date/Time picker when target time mode is active.

5. **Step 3: Action Control Buttons**:
   - **Primary CTA Button**: Full-width / high-visibility start button with smooth hover scale and active push feedback.
   - **Secondary Control Buttons**: Cancel and Clear buttons with proper disabled/enabled states.

---

## Technical & File Architecture

- **Main Script**: [shutdown_timer.py](file:///d:/Windows%20Shutdown%20Timer/shutdown_timer.py)
  - Refactor `init_ui()` to build the 3-step vertical flow layout.
  - Update `apply_styles()` to replace low-contrast color rules with the new high-contrast Fluent dark/light themes.
  - Simplify time mode switching and preset handlers.
  - Ensure all PySide6 widgets use proper accessible contrast colors.

---

## Verification Plan
1. Launch PySide6 application locally (`python shutdown_timer.py`).
2. Verify Text Contrast in Dark Mode: inspect card headers, status label, input labels.
3. Verify Text Contrast in Light Mode: inspect card headers, status label, input labels.
4. Test Quick Preset buttons (15m, 30m, 1h, 2h).
5. Test Action Switching (Shutdown, Restart, Sleep, Hibernate) and confirm dynamic color shifts.
6. Test Countdown Timer functionality & progress bar update.
