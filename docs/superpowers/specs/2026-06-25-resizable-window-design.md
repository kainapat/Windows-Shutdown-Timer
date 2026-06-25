# Spec: Resizable Window & Window Position Persistence

This design spec outlines how we make the PySide6 Windows Shutdown Timer application window resizable and persist its size and position across app restarts.

## Requirements

1. Make the window resizable, removing the fixed size constraint.
2. Maintain a minimum size of 600x680 to prevent the layout from breaking or clipping.
3. Save the window's width, height, X-coordinate, and Y-coordinate when the application is closed.
4. Separate window configuration from the timer's active state configuration (`timer_config.json`), storing it in `window_config.json` so that clearing settings or timer completion does not reset the window dimensions.
5. Restore the saved width, height, and coordinates on startup.

## Architectural Changes

### 1. `window_config.json` Configuration File
A separate configuration file will be introduced to hold the window's geometry settings:
```json
{
  "width": 600,
  "height": 680,
  "x": 100,
  "y": 100
}
```

### 2. Window Resizability
In `ShutdownTimerApp.__init__`:
- Replace `self.setFixedSize(600, 680)` with `self.setMinimumSize(600, 680)`.
- Set default size using `self.resize(600, 680)`.

### 3. Load Settings
In `ShutdownTimerApp.load_settings`:
- Keep existing timer state loading.
- Add code to load `window_config.json` and call `self.resize(width, height)` and `self.move(x, y)` if stored.

### 4. Save Settings on Close
In `ShutdownTimerApp.closeEvent`:
- Capture current geometry using `self.width()`, `self.height()`, and `self.pos()`.
- Save these values into `window_config.json`.
- Do not delete `window_config.json` in `_delete_config_file()`.

## Verification Plan

### Manual Verification
1. Run the application.
2. Drag borders to resize. Verify layout expands correctly.
3. Move the window to another location on the screen.
4. Close the application.
5. Verify `window_config.json` is created with correct dimensions and coordinates.
6. Open the application again. Verify it starts at the last saved size and position.
7. Click "ล้างค่า" (Clear fields) and verify `window_config.json` is not deleted, and the window remains resizable.
