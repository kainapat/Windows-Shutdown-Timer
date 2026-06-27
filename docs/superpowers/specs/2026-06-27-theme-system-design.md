# Design Specification: Theme System (Light Mode & Theme Toggle)

This document specifies the design and implementation plan for adding Light Mode support and a Theme Toggle button to the Windows Shutdown Timer application.

## 1. System Overview

The Windows Shutdown Timer application currently features a responsive "Ethereal Glass" dark-mode Bento Grid UI. This update introduces a **Theme Toggle** button in a new header section and a premium **Warm Premium Cream** Light Mode.

## 2. User Review Required

> [!IMPORTANT]
> The theme setting will be saved in `window_config.json` under the key `"theme"` (values: `"dark"` or `"light"`, default: `"dark"`). This ensures settings persist between launches and does not affect the active timer's configs in `timer_config.json`.

## 3. Detailed Specifications

### 3.1 Header Layout
A horizontal header is added at the top of the main window layout (above the Bento grid layout):
- **App Title**: `"Windows Shutdown Timer"` (Left-aligned, 16pt Bold, Segoe UI)
- **Theme Button**: Rounded pill button (Right-aligned, 10pt SemiBold, Segoe UI):
  - **Icon & Text**:
    - Dark Theme: `☀️ Light` (or `☀️ สว่าง` in Thai)
    - Light Theme: `🌙 Dark` (or `🌙 มืด` in Thai)

### 3.2 Color Palettes

Below is a comparison of the color tokens for Dark and Light modes:

| UI Component | Dark Mode Token | Light Mode Token |
| :--- | :--- | :--- |
| **Window Background** | `#050508` | `#faf9f6` (Warm Cream) |
| **Window Gradient End** | Action-specific dark color (e.g. `#18060a` for shutdown) | Action-specific pastel color (e.g. `#fef2f3` for shutdown) |
| **Bento Card Bg** | `rgba(18, 18, 24, 0.45)` | `rgba(255, 255, 255, 0.75)` |
| **Bento Card Border** | `rgba(255, 255, 255, 0.04)` | `rgba(0, 0, 0, 0.05)` |
| **Bento Card Glow** | `rgba({primary_rgb}, 0.08)` border highlight | `rgba({primary_rgb}, 0.12)` border highlight |
| **Main Typography** | `#e4e4e7` (Zinc 200) | `#1c1917` (Stone 900) |
| **Card Title Text** | `rgba(161, 161, 170, 0.6)` | `rgba(120, 113, 108, 0.7)` |
| **Form Inputs Bg** | `rgba(255, 255, 255, 0.03)` | `rgba(255, 255, 255, 0.9)` |
| **Form Inputs Border** | `rgba(255, 255, 255, 0.06)` | `rgba(0, 0, 0, 0.1)` |
| **Form Inputs Text** | `#f4f4f5` | `#1c1917` |

### 3.3 Action Pastel Endpoints (Light Mode Gradient)
- **Shutdown (0)**: `#fef2f3`
- **Restart (1)**: `#fff7ed`
- **Sleep (2)**: `#eff6ff`
- **Hibernate (3)**: `#faf5ff`

### 3.4 Input Dropdown Menus (QAbstractItemView)
In Light Mode, dropdown popup menus will have:
- Background: `#ffffff`
- Border: `1px solid rgba(0, 0, 0, 0.08)`
- Item Selection Background: `rgba(0, 0, 0, 0.04)`
- Text Color: `#1c1917`

### 3.5 Control Buttons
- **Start Button**: Stays primary color with solid background, text color `#ffffff` or dark `#050508` for readable contrast.
- **Cancel Button**: Transparent red background `rgba(239, 68, 68, 0.06)` with a red border and red text `#ef4444`.
- **Clear Button**: Transparent stone background `rgba(120, 113, 108, 0.06)` with a stone border and stone text `#78716c`.

### 3.6 Theme Toggle Button Visibility Bug Fix
- **Initial State Bug**: The theme switcher text is set via `update_theme_button_ui()`, which was only called during `toggle_theme()`. This caused the button to appear blank (no icon/text) on initial startup.
- **Fix**: Call `update_theme_button_ui()` automatically at the end of `apply_styles()`.
- **Contrast Enhancements**:
  - In Dark Mode, increase background opacity to `0.06` and border opacity to `0.16` (hover state: background `0.12`, border `0.25`) to ensure clean contrast on first open.
  - In Light Mode, set background opacity to `0.05` and border opacity to `0.12` (hover state: background `0.1`, border `0.2`).

---

## 4. Verification Plan

### 4.1 Visual Check
- Open app, toggle theme from Dark to Light.
- Verify readability of all text, labels, status text, and preset sublabels.
- Change Selected Action (Shutdown, Restart, Sleep, Hibernate) and ensure the radial pastel gradient updates correctly in Light Mode.
- Verify dropdown lists are readable and scrollable.

### 4.2 State Verification
- Close the app in Light Mode, reopen, and ensure it opens in Light Mode.
- Close the app in Dark Mode, reopen, and ensure it opens in Dark Mode.
- Clear settings, verify that theme choice persists (is not deleted, as it is in `window_config.json` rather than `timer_config.json`).
