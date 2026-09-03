# Post-Mortem: Clickable Dropdown Time Selectors Refactor (Windows Shutdown Timer)

## 1. Summary
In Windows Shutdown Timer v2.2.0, time selection in both **Timer Mode** and **Clock Mode** relied on free-form keyboard text entry controls (`QSpinBox` and `QDateTimeEdit`), forcing users to manually type numerical values instead of clicking to select. This was fixed by replacing these controls with discrete dropdown menus (`QComboBox` for Hours, Minutes, Seconds) and a calendar popup (`QDateEdit`), unified into a symmetrical 3-column layout with complete backward compatibility via proxy adapters (`SpinBoxProxy`, `DateTimeProxy`).

## 2. Symptom
- In **Clock Mode (ระบุเวลาจริง)**, clicking the calendar button on `self.date_edit` (`QDateTimeEdit`) only allowed selecting the date. Setting the target hour and minute required clicking into the small text edit area and typing the digits on the keyboard.
- In **Timer Mode (นับถอยหลัง)**, `self.spin_hours`, `self.spin_minutes`, and `self.spin_seconds` (`QSpinBox`) required manual typing or clicking tiny 18px stepper arrows, creating high interaction friction on desktop and touch environments.

## 3. Root Cause
1. **Control Modality Mismatch**: The widget selection in commit `17c6be0` prioritized compact text inputs (`QSpinBox` and `QDateTimeEdit`) over discrete selection widgets (`QComboBox`), assuming users preferred keyboard entry.
2. **QDateTimeEdit Calendar Limitation**: Qt's `QDateTimeEdit.setCalendarPopup(True)` only provides a GUI calendar picker for the date component. The time component (`HH:mm`) has no native dropdown menu or time-wheel picker within `QDateTimeEdit`.
3. **Layout Asymmetry**: Clock Mode had a single horizontal row (`clockLabel` + `dateTimeEdit`) while Timer Mode had 3 columns (`h_layout`, `m_layout`, `s_layout`), causing visual layout shifting during sliding mode transitions in `SlidingStackedWidget`.

## 4. Why It Produced the Symptom
`QDateTimeEdit` is architecturally an inline line-editor combined with spin arrows. Because Qt does not bundle an interactive clock popup into `QDateTimeEdit`, desktop users without immediate keyboard focus had to double-click each field (day, month, year, hour, minute) and type numbers manually.

## 5. Fix
1. **Symmetrical 3-Column Dropdowns**:
   - **Timer Mode (`Page 0`)**: Replaced `QSpinBox` with 3 `QComboBox` dropdowns:
     - `self.hours_combo`: `0 hr` to `24 hr` (25 discrete items)
     - `self.minutes_combo`: `0 min` to `59 min` (60 discrete items)
     - `self.seconds_combo`: `0 sec` to `59 sec` (60 discrete items)
   - **Clock Mode (`Page 1`)**: Replaced `QDateTimeEdit` with a 3-column composite selector:
     - `self.date_picker`: `QDateEdit` with `setCalendarPopup(True)` and format `"ddd d MMM yyyy"`
     - `self.time_hours_combo`: `QComboBox` populated with `00` to `23` (24 discrete items)
     - `self.time_minutes_combo`: `QComboBox` populated with `00` to `59` (60 discrete items)
2. **Backward-Compatible Proxy Adapters**:
   - Implemented [`SpinBoxProxy`](file:///d:/Windows%20Shutdown%20Timer/shutdown_timer.py) wrapping `self.hours_combo`, `self.minutes_combo`, and `self.seconds_combo` to fulfill `.value()` and `.setValue()` calls seamlessly.
   - Implemented [`DateTimeProxy`](file:///d:/Windows%20Shutdown%20Timer/shutdown_timer.py) wrapping `self.date_picker`, `self.time_hours_combo`, and `self.time_minutes_combo` to fulfill `.dateTime()`, `.date()`, `.time()`, and `.setDateTime()` calls.
3. **Preset & Default Time Synchronization**:
   - Updated `apply_preset()` to switch to Timer mode and synchronize dropdown values.
   - Initialized Clock default to `now + 1 hour` via `reset_clock_to_default()` to prevent immediate past-time validation warnings.
4. **QSS Stylesheet Overhaul**:
   - Updated Dark and Light stylesheets to support `QDateEdit` and added custom styled vertical scrollbars (`QComboBox QAbstractItemView QScrollBar:vertical`) for smooth scrolling through 60-item minute lists.

## 6. How It Was Found
- User report: *"อยากแก้ตรงระบุเวลาจริงเป็นแบบกดเลือกอ่ะ อันนี้มันต้องพิมพ์เอง และของ Timer ด้วย"* (User requested clickable point-and-click selection for both Clock and Timer modes instead of typing).
- Codebase inspection confirmed `QDateTimeEdit` and `QSpinBox` usage in `shutdown_timer.py` lines 650–740.

## 7. Why It Slipped Through
- **Interaction Testing Assumption**: Automated tests and developers often verify functionality via programmatic setters (`setValue()`, `setDateTime()`) rather than evaluating mouse-only / point-and-click usability.
- **Spec Drift**: The earlier refactor to 3-step vertical flow simplified layout count from 5 boxes to 3, but replaced dropdowns with spinboxes without evaluating user text-entry friction.

## 8. Validation
- **Automated Smoke Tests (`py -3.12`)**:
  - Verified item counts: `hours_combo` (25), `minutes_combo` (60), `seconds_combo` (60), `time_hours_combo` (24), `time_minutes_combo` (60).
  - Verified `SpinBoxProxy` and `DateTimeProxy` bidirectional reads and writes.
  - Verified default clock time calculation (`now + 1 hour`).
  - Verified preset application and `clear_fields()` reset logic.
- **Visual Settled Verification**:
  - Captured rendered snapshots in `scratch/settled_timer_dark.png`, `scratch/settled_clock_dark.png`, `scratch/settled_timer_light.png`, and `scratch/settled_clock_light.png`. All confirmed WCAG AA contrast, exact 3-column symmetry, and clean typography.
- **Standalone Build Verification**:
  - Executable compiled via PyInstaller into `dist/Windows Shutdown Timer.exe`.

## 9. Action Items
- [x] Replace `QSpinBox` and `QDateTimeEdit` with symmetrical 3-column `QComboBox` / `QDateEdit` dropdowns.
- [x] Implement `SpinBoxProxy` and `DateTimeProxy` for zero regression.
- [x] Document domain model in [`CONTEXT.md`](file:///d:/Windows%20Shutdown%20Timer/CONTEXT.md) and ADR in [`docs/adr/0001-dropdown-time-selectors.md`](file:///d:/Windows%20Shutdown%20Timer/docs/adr/0001-dropdown-time-selectors.md).
- [x] Rebuild standalone executable `dist/Windows Shutdown Timer.exe`.
