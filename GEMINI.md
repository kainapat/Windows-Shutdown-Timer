# GEMINI.md - Project Context & Instructions

## Project Overview
**Windows Shutdown Timer** is a Python-based desktop application designed for scheduling system power actions (Shutdown, Restart, Sleep, Hibernate) on Windows. It features a modern, dark-mode GUI built with **PySide6** and supports quick presets, countdown timers, and scheduled date/time triggers.

- **Primary Language:** Python 3.12+
- **GUI Framework:** PySide6 (Qt for Python)
- **Architecture:** Single-file monolithic application (`shutdown_timer.py`).
- **Target Platform:** Windows only (utilizes the native `shutdown` command and `rundll32.exe`).
- **Key Features:** Dark Mode UI, Toast Notifications, Progress Bar, Quick Presets, and Auto-save configuration.

## Building and Running

### Development Environment
1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Run Application:**
   ```bash
   python shutdown_timer.py
   ```

### Production Build
The project uses **PyInstaller** to create a standalone executable.
- **Build Command:**
  ```bash
  pyinstaller --onefile --windowed --name="Windows Shutdown Timer" --icon=icon.ico shutdown_timer.py
  ```
- **Output:** The compiled executable will be located in the `dist/` directory.

### CI/CD
A GitHub Actions workflow (`.github/workflows/build-release.yml`) is configured to automatically build and release the executable when a new tag (e.g., `v1.0.0`) is pushed.

## Development Conventions

### Coding Style & Patterns
- **Monolith:** The entire application logic resides in `shutdown_timer.py`. Maintain this structure unless a refactor is explicitly requested.
- **Naming Conventions:**
  - **Classes:** PascalCase (e.g., `ShutdownTimerApp`, `Toast`).
  - **Methods/Functions:** camelCase (e.g., `start_timer`, `update_countdown`).
  - **Constants:** UPPER_SNAKE_CASE (e.g., `CONFIG_FILE`, `ACTION_COLORS`).
  - **Private Methods:** Prefixed with an underscore and camelCase (e.g., `_execute_sleep_hibernate`).
- **UI/UX:**
  - **Styling:** Uses Qt Style Sheets (QSS) for a dark theme (Catppuccin-inspired).
  - **Language:** The UI uses Thai text for labels and notifications.
  - **Icons:** Uses Unicode characters for icons (e.g., `⏻`, `▶`, `✕`).
- **Configuration:** Settings are persisted in `timer_config.json` at runtime and cleaned up upon exit or reset.

### Key Components
- `ShutdownTimerApp`: The main window class handling UI setup and core timer logic.
- `PresetCard`: Custom QPushButton for quick-access timer presets.
- `Toast`: Custom QWidget for overlay notifications.

### Error Handling & Safety
- **Subprocess calls:** Power commands are executed via `subprocess.run`. Always wrap these in try/except blocks and provide user feedback via `show_toast`.
- **User Confirmation:** Always prompt the user for confirmation before scheduling a power action or cancelling an active timer.

## Testing Strategy
Currently, the project **does not have an automated test suite**. 
- **Recommendation:** If adding tests, use `pytest` with `pytest-qt` for UI testing.
- **Mocking:** `subprocess.run` must be mocked to prevent actual system shutdowns during testing.

## Instruction for Gemini CLI
- When modifying the UI, ensure consistency with the existing dark-mode QSS styles.
- When adding new power actions, verify the corresponding Windows CLI command (e.g., `shutdown /s`, `shutdown /r`).
- Always use `encoding="utf-8"` for file operations.
- Prefer `f-strings` for string formatting.
