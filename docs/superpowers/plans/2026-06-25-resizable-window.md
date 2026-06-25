# Resizable Window Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the main window resizable, keeping a minimum size of 600x680, and persist its size and position across app launches using a separate `window_config.json` file.

**Architecture:** We will change the window sizing constraint from fixed to minimum resizable, and override `closeEvent` to save the window's position and size to `window_config.json`. We will load this configuration file on startup to restore the window's last position and size.

**Tech Stack:** Python 3, PySide6 (Qt for Python)

## Global Constraints
* The application must support Windows environment.
* Minimum size must be 600x680.
* Window state (size and position) must be saved into a separate configuration file `window_config.json`.

---

### Task 1: Allow Resizing & Set Minimum Window Size

**Files:**
- Modify: [shutdown_timer.py](file:///d:/Windows%20Shutdown%20Timer/shutdown_timer.py)

**Interfaces:**
- Consumes: None
- Produces: None

- [ ] **Step 1: Modify ShutdownTimerApp initialization to allow resizing**

Edit [shutdown_timer.py](file:///d:/Windows%20Shutdown%20Timer/shutdown_timer.py) at line 265. Change:
```python
        self.setFixedSize(600, 680)
```
to:
```python
        self.setMinimumSize(600, 680)
        self.resize(600, 680)
```

- [ ] **Step 2: Manually run the application to verify resizing works**

Run:
```powershell
python shutdown_timer.py
```
Expected: The app opens. The user can drag window edges to resize the window larger, but cannot shrink it below 600x680. Close the app.

- [ ] **Step 3: Commit the changes**

Run:
```powershell
git add shutdown_timer.py
git commit -m "feat: make window resizable with a minimum size of 600x680"
```

---

### Task 2: Implement Size & Position Persistence via `window_config.json`

**Files:**
- Modify: [shutdown_timer.py](file:///d:/Windows%20Shutdown%20Timer/shutdown_timer.py)

**Interfaces:**
- Consumes: None
- Produces: Save/load methods for `window_config.json`

- [ ] **Step 1: Define window config file constant and save/load helper functions**

In [shutdown_timer.py](file:///d:/Windows%20Shutdown%20Timer/shutdown_timer.py), define the constant `WINDOW_CONFIG_FILE = "window_config.json"` near `CONFIG_FILE`.
Add the following methods to `ShutdownTimerApp` class:

```python
    def save_window_settings(self):
        """Save window size and position to JSON file"""
        settings = {
            "width": self.width(),
            "height": self.height(),
            "x": self.x(),
            "y": self.y(),
        }
        try:
            temp_path = "window_config.json.tmp"
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
            os.replace(temp_path, "window_config.json")
            logger.info("💾 Window size and position saved")
        except Exception as e:
            logger.error(f"💾❌ Could not save window settings: {e}")

    def load_window_settings(self):
        """Load window size and position from JSON file"""
        if not os.path.exists("window_config.json"):
            return
        try:
            with open("window_config.json", "r", encoding="utf-8") as f:
                settings = json.load(f)
            
            # Load and set size
            width = settings.get("width", 600)
            height = settings.get("height", 680)
            self.resize(width, height)
            
            # Load and set position
            x = settings.get("x")
            y = settings.get("y")
            if x is not None and y is not None:
                self.move(x, y)
                logger.info(f"📂 Window size ({width}x{height}) and position ({x}, {y}) restored")
        except Exception as e:
            logger.error(f"📂❌ Could not load window settings: {e}")
```

- [ ] **Step 2: Update `closeEvent` and class initialization to load/save settings**

In [shutdown_timer.py](file:///d:/Windows%20Shutdown%20Timer/shutdown_timer.py):
Modify `__init__` method to load window settings. Add `self.load_window_settings()` after `self.init_ui()`.
Modify `closeEvent` method to call `self.save_window_settings()`.

Specifically, update `closeEvent`:
```python
    def closeEvent(self, event):
        """Called when closing the application"""
        logger.info("👋 Application closing... Bye!")
        self.countdown_timer.stop()
        self.save_window_settings()  # Save window state before closing
        self._delete_config_file()
        super().closeEvent(event)
```

- [ ] **Step 3: Manually verify persistence**

Run:
```powershell
python shutdown_timer.py
```
Expected: The app opens.
1. Move the window to a different position and resize it to be larger (e.g. 700x800).
2. Close the app.
3. Check that `window_config.json` exists and contains correct values.
4. Run the app again.
5. Verify it opens with the exact same size and position as when closed.
6. Click "ล้างค่า" (Clear fields) or set/cancel a timer. Close the app.
7. Re-open and verify it still remembers the size and position.

- [ ] **Step 4: Commit changes**

Run:
```powershell
git add shutdown_timer.py
git commit -m "feat: persist window size and position to window_config.json"
```
