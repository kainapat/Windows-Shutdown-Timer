# Windows Shutdown Timer

Desktop utility for scheduling Windows system actions (shutdown, restart, sleep, hibernate) via relative duration or absolute wall-clock time.

## Language

**Timer Mode**:
A scheduling mode where the user specifies a relative duration via a 3-column dropdown layout: Hours (0–24 hr), Minutes (0–59 min), and Seconds (0–59 sec).
_Avoid_: Countdown input mode, duration mode, relative mode

**Clock Mode**:
A scheduling mode where the user selects an absolute target time via a symmetrical 3-column layout: Date (`QDateEdit` calendar popup), Hours (00–23 dropdown), and Minutes (00–59 dropdown).
_Avoid_: DateTime mode, real-time mode, target time mode

**Time Selector**:
A dropdown-based selection interface (`QComboBox`) for picking discrete time units without keyboard text entry.
_Avoid_: Time spinbox, text time input

**Date Selector**:
A calendar popup interface (`QDateEdit` with calendar popup enabled) allowing point-and-click date selection without text typing.
_Avoid_: Date text field, manual date input

**Preset**:
A one-click shortcut button (15 Min, 30 Min, 1 Hr, 2 Hrs) that sets a pre-configured duration and initiates scheduling with confirmation.
_Avoid_: Quick button, template, shortcut pill
