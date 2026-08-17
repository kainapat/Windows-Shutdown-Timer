# Design Spec: Soft Slate Grey Light Mode & Eng(TH) Bilingual UI

## 1. Overview
The goal is to redesign the Light Mode of the Windows Shutdown Timer application from an overly bright/harsh white theme to a comfortable, modern, eye-friendly **Soft Slate Grey** aesthetic, and convert all visible text across the entire interface (labels, cards, buttons, presets, units, status messages, toasts, dialogs) into a consistent **Eng (TH)** bilingual format.

---

## 2. Visual Design & Color Architecture (Soft Slate Grey Theme)

### Light Mode Palette Specifications:
- **Main Canvas (Window Background):** `#d8dce2` (Soft Slate Grey) with subtle radial gradient transitioning towards `#ced4dc` or action accent tint in `update_theme_colors()`.
- **Bento Card Containers:** Surface `#e8ecf1`, Border `1px solid #cbd5e1` with subtle border-shadow, Header text `#0f172a` (Weight 600).
- **Preset Cards:** Surface `#f1f5f9`, Border `1px solid #cbd5e1`, Value text `#0f172a`, Sublabel `#475569`. Hover state with subtle action accent tint (`rgba(accent, 0.08)`), pressed `#cbd5e1`.
- **Action Pill Buttons (Unchecked):** Surface `#dbe0e6`, Border `1px solid #cbd5e1`, Text `#334155`, Hover `#cbd5e1`.
- **Action Pill Buttons (Checked):** Solid Action Accent color (Shutdown: `#ff3b5c`, Restart: `#ff9500`, Sleep: `#007aff`, Hibernate: `#a855f7`), Text `#ffffff`, Bold.
- **Mode Switcher Radio Buttons (Timer / Clock):** Unchecked `#dbe0e6`, Checked `#ffffff` with Action Accent border and subtle accent background tint.
- **Time Inputs (SpinBoxes & DateTimeEdit):** Background `#f8fafc` / `#ffffff`, Border `1px solid #94a3b8` (Focus: `#64748b`), Text `#0f172a`.
- **Progress Bar:** Background track `#cbd5e1`, Border `1px solid #94a3b8`, Chunk gradient with Action Primary & Secondary colors.
- **Theme Button:** Background `#e8ecf1`, Border `1px solid #cbd5e1`, Text `#0f172a`, Hover `#dfe4ea`.
- **Dialog Boxes (QMessageBox):** Background `#e8ecf1`, Text `#0f172a`, Buttons `#dbe0e6` (Hover: `#cbd5e1`).

### Dark Mode (Preserved):
- Dark mode remains intact with OLED dark / zinc aesthetic (`#09090b` canvas, `#18181b` cards, `#27272a` borders, `#f4f4f5` text).

---

## 3. Bilingual Eng(TH) Localization Map

### A. Window Header & Navigation
- **Window Title:** `Windows Shutdown Timer`
- **Theme Toggle:** `🌙 Dark (โหมดมืด)` (when in Light Mode) / `☀️ Light (โหมดสว่าง)` (when in Dark Mode)
- **Theme Button Width:** Adjusted to accommodate `Dark (โหมดมืด)` / `Light (โหมดสว่าง)` without text clipping.

### B. Countdown Hero Section
- **Card Title:** `Countdown Display (หน้าจอนับถอยหลัง)`
- **Default Status:** `Status: Ready / Idle (สถานะ: ยังไม่ได้เริ่มนับถอยหลัง)`
- **Active Status:** `Status: {Action Eng} at {HH:MM:SS} (สถานะ: จะ{Action TH}เวลา {HH:MM:SS})`
- **Immediate Action Status:** `Status: Executing {Action Eng}... (สถานะ: กำลัง{Action TH}...)`
- **Cancelled Status:** `Status: Cancelled (สถานะ: ยกเลิกการตั้งเวลาแล้ว)`
- **Progress Format:** `{progress}% - Remaining (เหลือ) {mins:02d}:{secs:02d}`

### C. Step 1: Action Selection
- **Card Title:** `1. Select Action (เลือกการกระทำ)`
- **Action Options:**
  - `🔌 Shutdown (ปิดเครื่อง)`
  - `🔄 Restart (รีสตาร์ท)`
  - `😴 Sleep (พักเครื่อง)`
  - `🌙 Hibernate (จำศีล)`

### D. Step 2: Time Settings
- **Card Title:** `2. Set Time (กำหนดเวลา)`
- **Preset Cards:**
  - `15` + `Min (นาที)`
  - `30` + `Min (นาที)`
  - `1` + `Hr (ชม.)`
  - `2` + `Hrs (ชม.)`
- **Mode Switcher:**
  - `⏱ Timer (นับถอยหลัง)`
  - `📅 Clock (ระบุเวลาจริง)`
- **SpinBox Unit Labels:**
  - `Hours (ชั่วโมง)` | Suffix: ` hr`
  - `Minutes (นาที)` | Suffix: ` min`
  - `Seconds (วินาที)` | Suffix: ` sec`
- **Target Time Label:** `Target Time (เวลาเป้าหมาย):`

### E. Step 3: Controls
- **Card Title:** `3. Controls (เริ่มการทำงาน)`
- **Start Button:** `▶ Start Countdown (เริ่มนับถอยหลัง)`
- **Cancel Button:** `✕ Cancel (ยกเลิก)`
- **Reset Button:** `↺ Reset (ล้างค่า)`
- **Tooltips:**
  - Start: `Start countdown and schedule action (เริ่มนับถอยหลังและตั้งเวลาการทำงาน)`
  - Cancel: `Cancel scheduled timer (ยกเลิกการตั้งเวลาและหยุดการนับถอยหลัง)`
  - Reset: `Reset all fields (ล้างค่าและรีเซ็ตการตั้งค่าทั้งหมด)`

### F. Dialogs & Toast Notifications
- **Preset Confirmation Dialog:**
  - Title: `Confirm Schedule (ยืนยันการตั้งเวลา)`
  - Message: `Schedule {Action Eng} in {time_str}?\n(ต้องการตั้งเวลา{Action TH}ในอีก {time_str} หรือไม่?)\n\nPlease save your work before proceeding. (โปรดบันทึกงานของคุณก่อนดำเนินการ)`
- **Timer Confirmation Dialog:**
  - Title: `Confirm Schedule (ยืนยันการตั้งเวลา)`
  - Message: `Schedule {Action Eng} at target time?\n(คุณต้องการตั้งเวลา{Action TH}หรือไม่?)\n\nPlease save your work before proceeding. (โปรดบันทึกงานของคุณก่อนดำเนินการ)`
- **Immediate Sleep/Hibernate Confirmation Dialog:**
  - Title: `Confirm {Action Eng} (ยืนยันการ{Action TH})`
  - Message: `Execute {Action Eng} immediately?\n(ต้องการ{Action TH}ทันทีหรือไม่?)\n\nPlease save your work before proceeding. (โปรดบันทึกงานของคุณก่อนดำเนินการ)`
- **Cancel Confirmation Dialog:**
  - Title: `Confirm Cancel (ยืนยันการยกเลิก)`
  - Message: `Are you sure you want to cancel the timer?\n(ต้องการยกเลิกการตั้งเวลาหรือไม่?)`
- **Toasts:**
  - Already active: `A timer is already active. Please cancel first. (มีการตั้งเวลาอยู่แล้ว กรุณายกเลิกก่อน)`
  - Presets support: `Quick Presets only support Shutdown & Restart (Quick Presets รองรับเฉพาะ Shutdown และ Restart)`
  - Scheduled success: `Scheduled {Action Eng} ({Action TH}): {time_str}`
  - Cancel success: `Timer cancelled successfully (ยกเลิกการตั้งเวลาสำเร็จ)`
  - Reset success: `All fields reset (ล้างค่าเรียบร้อย)`
  - Input > 0 error: `Please specify a duration greater than 0 (กรุณาระบุระยะเวลานับถอยหลังมากกว่า 0)`
  - Future time error: `Please select a future time (กรุณาตั้งเวลาในอนาคต)`
  - Max duration error: `Please set time within 72 hours (กรุณาตั้งเวลาไม่เกิน 72 ชั่วโมง)`

---

## 4. Verification Plan
- **UI Launch & Visual Inspection:** Run `python shutdown_timer.py` to verify:
  - Soft Slate Grey light mode looks soft, balanced, and non-glaring.
  - All texts and labels fit within buttons, cards, and headers without wrapping or clipping.
  - Action theme color switching (Shutdown, Restart, Sleep, Hibernate) updates background gradients and highlights smoothly in Soft Slate Grey mode.
  - Theme toggling between Light and Dark mode works seamlessly.
  - Timer and preset dialogs display bilingual texts clearly.
