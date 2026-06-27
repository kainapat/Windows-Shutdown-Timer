# Theme System & Light Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a Theme Toggle button and a premium "Warm Premium Cream" Light Mode to the Windows Shutdown Timer application, with state persistence.

**Architecture:** 
- Persist the current theme mode (`"dark"` or `"light"`) in `window_config.json` via a new `self.current_theme_mode` attribute on the `ShutdownTimerApp` class.
- Add a new Header Bar widget layout above the Bento Grid layout, hosting the Title and the Theme Toggle Button.
- Refactor the stylesheets in `apply_styles` and `update_theme_colors` to dynamically apply either Light or Dark base CSS and action-specific highlights.

**Tech Stack:** PySide6, Python 3.12+

## Global Constraints
- Do not break existing timer logic.
- Retain the Bento Grid structure.
- Follow existing patterns for window configuration saving and loading.
- Always write user-facing explanations in Thai.

---

### Task 1: Theme State Configuration & Persistence

**Files:**
- Modify: [shutdown_timer.py](file:///d:/Windows%20Shutdown%20Timer/shutdown_timer.py)

**Interfaces:**
- Consumes: JSON config files
- Produces: `self.current_theme_mode` attribute (`"dark"` or `"light"`)

- [ ] **Step 1: Update `__init__` constructor**
  Initialize `self.current_theme_mode = "dark"` in `ShutdownTimerApp.__init__` before UI initialization.
  ```python
  # In class ShutdownTimerApp:
  def __init__(self):
      super().__init__()
      # ... existing state variables ...
      self.current_theme_mode = "dark" # Default theme
  ```

- [ ] **Step 2: Update `load_window_settings` to restore theme mode**
  Update `load_window_settings` to read the `"theme"` key from `window_config.json`.
  ```python
  # In ShutdownTimerApp.load_window_settings:
  self.current_theme_mode = settings.get("theme", "dark")
  logger.info(f"📂 Theme mode '{self.current_theme_mode}' loaded")
  ```

- [ ] **Step 3: Update `save_window_settings` to write theme mode**
  Update `save_window_settings` to include the `"theme"` key.
  ```python
  # In ShutdownTimerApp.save_window_settings:
  settings = {
      "width": self.width(),
      "height": self.height(),
      "x": self.x(),
      "y": self.y(),
      "theme": self.current_theme_mode,
  }
  ```

- [ ] **Step 4: Commit Task 1**
  Run: `git commit -am "feat: add theme setting state persistence"`

---

### Task 2: Header UI & Theme Toggle Button

**Files:**
- Modify: [shutdown_timer.py](file:///d:/Windows%20Shutdown%20Timer/shutdown_timer.py)

**Interfaces:**
- Consumes: `self.current_theme_mode`
- Produces: `header_layout` with title and toggle button; `toggle_theme()` method

- [ ] **Step 1: Modify `init_ui` to add Header Bar**
  Insert a horizontal header layout at the start of `init_ui`, above the Bento Grid layout.
  ```python
  # In ShutdownTimerApp.init_ui:
  header_layout = QHBoxLayout()
  header_layout.setContentsMargins(4, 0, 4, 4)

  self.title_label = QLabel("Windows Shutdown Timer")
  title_font = QFont("Segoe UI", 16, QFont.Bold)
  self.title_label.setFont(title_font)
  header_layout.addWidget(self.title_label)

  # Spacer between title and button
  header_layout.addStretch()

  self.theme_button = QPushButton()
  self.theme_button.setCursor(Qt.PointingHandCursor)
  self.theme_button.setFixedWidth(100)
  self.theme_button.setMinimumHeight(32)
  self.theme_button.clicked.connect(self.toggle_theme)
  header_layout.addWidget(self.theme_button)

  main_layout.addLayout(header_layout) # Added before grid_layout
  main_layout.addLayout(grid_layout)
  ```

- [ ] **Step 2: Implement `toggle_theme` and update button visual state**
  Add the `toggle_theme` method to handle theme state switching, updating button text/icon, and re-applying styles.
  ```python
  # In ShutdownTimerApp:
  def toggle_theme(self):
      """Switch between light and dark themes"""
      if self.current_theme_mode == "dark":
          self.current_theme_mode = "light"
      else:
          self.current_theme_mode = "dark"
          
      logger.info(f"🌓 Theme toggled to {self.current_theme_mode}")
      self.update_theme_button_ui()
      self.apply_styles()
      self.update_theme_colors(self.action_combo.currentIndex())
      self.save_window_settings()

  def update_theme_button_ui(self):
      """Update theme button label based on current theme"""
      if self.current_theme_mode == "light":
          self.theme_button.setText("🌙 Dark Mode")
      else:
          self.theme_button.setText("☀️ Light Mode")
  ```

- [ ] **Step 3: Call button update in `init_ui`**
  Make sure to update the button's text/icon on app launch. Call `self.update_theme_button_ui()` in `init_ui` or at the end of window loading.
  ```python
  # In ShutdownTimerApp.init_ui call at the end:
  self.update_theme_button_ui()
  ```

- [ ] **Step 4: Commit Task 2**
  Run: `git commit -am "feat: implement header UI and theme toggle button"`

---

### Task 3: Light & Dark Stylesheets Refactoring

**Files:**
- Modify: [shutdown_timer.py](file:///d:/Windows%20Shutdown%20Timer/shutdown_timer.py)

**Interfaces:**
- Consumes: `self.current_theme_mode`
- Produces: Visual theme transformation of PySide6 widgets

- [ ] **Step 1: Update `apply_styles` to load conditional CSS**
  Redefine `apply_styles` to branch based on `self.current_theme_mode`. Include separate base stylesheets for dark and light.
  
  ```python
  def apply_styles(self):
      """Apply base stylesheet based on light or dark theme"""
      if self.current_theme_mode == "light":
          base_style = """
              QMainWindow {
                  background-color: #faf9f6;
              }
              QWidget {
                  color: #1c1917;
                  font-family: 'Segoe UI', sans-serif;
                  font-size: 11pt;
              }
              #BentoCard {
                  background-color: rgba(255, 255, 255, 0.75);
                  border: 1px solid rgba(0, 0, 0, 0.05);
                  border-radius: 20px;
              }
              #BentoCardTitle {
                  color: rgba(120, 113, 108, 0.7);
                  text-transform: uppercase;
                  letter-spacing: 1px;
                  font-size: 8pt;
                  font-weight: bold;
                  margin-bottom: 2px;
              }
              QLabel {
                  color: #1c1917;
                  background-color: transparent;
              }
              QComboBox, QDateTimeEdit {
                  background-color: rgba(255, 255, 255, 0.9);
                  border: 1px solid rgba(0, 0, 0, 0.1);
                  border-radius: 12px;
                  padding: 8px 14px;
                  color: #1c1917;
                  min-width: 80px;
              }
              QComboBox:hover, QDateTimeEdit:hover {
                  border-color: rgba(0, 0, 0, 0.2);
                  background-color: rgba(0, 0, 0, 0.02);
              }
              QComboBox::drop-down, QDateTimeEdit::drop-down {
                  border: none;
                  width: 30px;
              }
              QComboBox::down-arrow, QDateTimeEdit::down-arrow {
                  image: none;
                  border-left: 5px solid transparent;
                  border-right: 5px solid transparent;
                  border-top: 5px solid rgba(0, 0, 0, 0.6);
                  margin-right: 8px;
              }
              QComboBox QAbstractItemView {
                  background-color: #ffffff;
                  border: 1px solid rgba(0, 0, 0, 0.1);
                  border-radius: 12px;
                  padding: 6px;
                  selection-background-color: rgba(0, 0, 0, 0.05);
                  selection-color: #000000;
                  outline: none;
                  color: #1c1917;
              }
              QRadioButton {
                  color: #78716c;
                  spacing: 6px;
                  font-size: 10pt;
                  background-color: rgba(0, 0, 0, 0.02);
                  border: 1px solid rgba(0, 0, 0, 0.04);
                  border-radius: 12px;
                  padding: 8px 12px;
              }
              QRadioButton::indicator {
                  width: 0px;
                  height: 0px;
              }
              QRadioButton:hover {
                  border-color: rgba(0, 0, 0, 0.12);
                  color: #1c1917;
              }
              AnimatedButton {
                  background-color: rgba(0, 0, 0, 0.02);
                  border: 1px solid rgba(0, 0, 0, 0.06);
                  border-radius: 14px;
                  padding: 12px 18px;
                  font-weight: bold;
                  font-size: 13px;
                  color: #1c1917;
              }
              AnimatedButton[hovered="true"] {
                  background-color: rgba(0, 0, 0, 0.05);
              }
              AnimatedButton[pressed_state="true"] {
                  background-color: rgba(0, 0, 0, 0.01);
                  padding-top: 14px;
                  padding-bottom: 10px;
              }
              AnimatedButton:disabled {
                  background-color: rgba(0, 0, 0, 0.01);
                  color: #a8a29e;
                  border-color: rgba(0, 0, 0, 0.02);
              }
              QProgressBar {
                  border: 1px solid rgba(0, 0, 0, 0.04);
                  border-radius: 8px;
                  text-align: center;
                  background-color: rgba(0, 0, 0, 0.05);
                  color: #57534e;
                  font-weight: bold;
                  font-size: 10px;
              }
              QProgressBar::chunk {
                  border-radius: 6px;
                  margin: 1px;
              }
              QCalendarWidget QWidget {
                  background-color: #ffffff;
                  color: #1c1917;
              }
              QCalendarWidget QAbstractItemView:enabled {
                  background-color: #ffffff;
                  color: #1c1917;
                  selection-background-color: rgba(0, 0, 0, 0.06);
                  selection-color: #000000;
              }
              QCalendarWidget QAbstractItemView:disabled {
                  color: #a8a29e;
              }
              QPushButton#themeButton {
                  background-color: rgba(0, 0, 0, 0.03);
                  border: 1px solid rgba(0, 0, 0, 0.08);
                  border-radius: 10px;
                  color: #1c1917;
                  font-weight: 600;
              }
              QPushButton#themeButton:hover {
                  background-color: rgba(0, 0, 0, 0.08);
                  border-color: rgba(0, 0, 0, 0.15);
              }
          """
      else:
          # Dark mode CSS (Existing style, but style self.theme_button as well)
          base_style = """
              QMainWindow {
                  background-color: #050508;
              }
              QWidget {
                  color: #e4e4e7;
                  font-family: 'Segoe UI', sans-serif;
                  font-size: 11pt;
              }
              #BentoCard {
                  background-color: rgba(18, 18, 24, 0.45);
                  border: 1px solid rgba(255, 255, 255, 0.04);
                  border-radius: 20px;
              }
              #BentoCardTitle {
                  color: rgba(161, 161, 170, 0.6);
                  text-transform: uppercase;
                  letter-spacing: 1px;
                  font-size: 8pt;
                  font-weight: bold;
                  margin-bottom: 2px;
              }
              QLabel {
                  color: #e4e4e7;
                  background-color: transparent;
              }
              QComboBox, QDateTimeEdit {
                  background-color: rgba(255, 255, 255, 0.03);
                  border: 1px solid rgba(255, 255, 255, 0.06);
                  border-radius: 12px;
                  padding: 8px 14px;
                  color: #f4f4f5;
                  min-width: 80px;
              }
              QComboBox:hover, QDateTimeEdit:hover {
                  border-color: rgba(255, 255, 255, 0.15);
                  background-color: rgba(255, 255, 255, 0.05);
              }
              QComboBox::drop-down, QDateTimeEdit::drop-down {
                  border: none;
                  width: 30px;
              }
              QComboBox::down-arrow, QDateTimeEdit::down-arrow {
                  image: none;
                  border-left: 5px solid transparent;
                  border-right: 5px solid transparent;
                  border-top: 5px solid rgba(255, 255, 255, 0.6);
                  margin-right: 8px;
              }
              QComboBox QAbstractItemView {
                  background-color: #0d0d11;
                  border: 1px solid rgba(255, 255, 255, 0.08);
                  border-radius: 12px;
                  padding: 6px;
                  selection-background-color: rgba(255, 255, 255, 0.06);
                  selection-color: #ffffff;
                  outline: none;
                  color: #e4e4e7;
              }
              QRadioButton {
                  color: #8a8a93;
                  spacing: 6px;
                  font-size: 10pt;
                  background-color: rgba(255, 255, 255, 0.02);
                  border: 1px solid rgba(255, 255, 255, 0.04);
                  border-radius: 12px;
                  padding: 8px 12px;
              }
              QRadioButton::indicator {
                  width: 0px;
                  height: 0px;
              }
              QRadioButton:hover {
                  border-color: rgba(255, 255, 255, 0.1);
                  color: #d1d1d6;
              }
              AnimatedButton {
                  background-color: rgba(255, 255, 255, 0.03);
                  border: 1px solid rgba(255, 255, 255, 0.06);
                  border-radius: 14px;
                  padding: 12px 18px;
                  font-weight: bold;
                  font-size: 13px;
                  color: #e4e4e7;
              }
              AnimatedButton[hovered="true"] {
                  background-color: rgba(255, 255, 255, 0.06);
              }
              AnimatedButton[pressed_state="true"] {
                  background-color: rgba(255, 255, 255, 0.01);
                  padding-top: 14px;
                  padding-bottom: 10px;
              }
              AnimatedButton:disabled {
                  background-color: rgba(255, 255, 255, 0.01);
                  color: #52525b;
                  border-color: rgba(255, 255, 255, 0.02);
              }
              QProgressBar {
                  border: 1px solid rgba(255, 255, 255, 0.04);
                  border-radius: 8px;
                  text-align: center;
                  background-color: rgba(0, 0, 0, 0.4);
                  color: #a1a1aa;
                  font-weight: bold;
                  font-size: 10px;
              }
              QProgressBar::chunk {
                  border-radius: 6px;
                  margin: 1px;
              }
              QCalendarWidget QWidget {
                  background-color: #0d0d11;
                  color: #e4e4e7;
              }
              QCalendarWidget QAbstractItemView:enabled {
                  background-color: #0d0d11;
                  color: #e4e4e7;
                  selection-background-color: rgba(255, 255, 255, 0.08);
                  selection-color: #ffffff;
              }
              QCalendarWidget QAbstractItemView:disabled {
                  color: #52525b;
              }
              QPushButton#themeButton {
                  background-color: rgba(255, 255, 255, 0.03);
                  border: 1px solid rgba(255, 255, 255, 0.08);
                  border-radius: 10px;
                  color: #e4e4e7;
                  font-weight: 600;
              }
              QPushButton#themeButton:hover {
                  background-color: rgba(255, 255, 255, 0.08);
                  border-color: rgba(255, 255, 255, 0.15);
              }
          """
      self.setStyleSheet(base_style)
  ```
  Set object name on theme button in `init_ui`: `self.theme_button.setObjectName("themeButton")` so the style applies correctly.

- [ ] **Step 2: Update `update_theme_colors` for Light Mode specific gradients and highlights**
  Refactor `update_theme_colors` to handle both Dark and Light theme styling:
  
  ```python
  def update_theme_colors(self, action_index):
      """Update theme colors based on selected action with smooth visual transitions"""
      self.current_theme = ACTION_COLORS.get(action_index, ACTION_COLORS[0])
      primary = self.current_theme["primary"]
      secondary = self.current_theme["secondary"]
      accent = self.current_theme["accent"]
      
      # Determine background gradient endpoint and widget highlights based on active theme mode
      if self.current_theme_mode == "light":
          # Pastel backgrounds
          light_bg_ends = {
              0: "#fef2f3", # Shutdown - light pink
              1: "#fff7ed", # Restart - light orange
              2: "#eff6ff", # Sleep - light blue
              3: "#faf5ff", # Hibernate - light purple
          }
          bg_end = light_bg_ends.get(action_index, "#fef2f3")
          
          # Update countdown label color to primary
          self.countdown_label.setStyleSheet(
              f"background: transparent; color: {primary}; letter-spacing: 2px;"
          )
          
          dynamic_style = f"""
              QMainWindow {{
                  background: qradialgradient(cx:0.5, cy:0.5, radius:1.0, fx:0.5, fy:0.5,
                      stop:0 #faf9f6,
                      stop:1 {bg_end});
              }}
              #BentoCard {{
                  border-color: rgba({self.hex_to_rgb(primary)}, 0.12);
              }}
              QComboBox::down-arrow, QDateTimeEdit::down-arrow {{
                  border-top-color: {primary};
              }}
              QRadioButton:checked {{
                  background-color: rgba({self.hex_to_rgb(primary)}, 0.12);
                  border-color: rgba({self.hex_to_rgb(primary)}, 0.4);
                  color: #000000;
                  font-weight: bold;
              }}
              QProgressBar::chunk {{
                  background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                      stop:0 {primary},
                      stop:1 {secondary});
              }}
          """
          
          # Preset cards
          preset_btn_style = f"""
              AnimatedButton {{
                  background-color: rgba(255, 255, 255, 0.8);
                  border: 1px solid rgba(0, 0, 0, 0.05);
                  border-radius: 16px;
              }}
              AnimatedButton[hovered="true"] {{
                  background-color: rgba({self.hex_to_rgb(primary)}, 0.06);
                  border-color: rgba({self.hex_to_rgb(primary)}, 0.35);
              }}
              AnimatedButton[pressed_state="true"] {{
                  background-color: rgba({self.hex_to_rgb(primary)}, 0.02);
              }}
          """
          
          # Start Button
          start_btn_style = f"""
              AnimatedButton {{
                  background-color: {primary};
                  border: 1px solid {primary};
                  border-radius: 12px;
                  font-weight: bold;
                  font-size: 13px;
                  color: #ffffff;
              }}
              AnimatedButton[hovered="true"] {{
                  background-color: {secondary};
                  border-color: {secondary};
              }}
              AnimatedButton[pressed_state="true"] {{
                  background-color: {accent};
                  border-color: {accent};
                  padding-top: 14px;
                  padding-bottom: 10px;
              }}
          """
          
          # Cancel Button
          cancel_btn_style = f"""
              AnimatedButton {{
                  background-color: rgba(239, 68, 68, 0.05);
                  border: 1px solid rgba(239, 68, 68, 0.15);
                  border-radius: 12px;
                  font-weight: bold;
                  font-size: 13px;
                  color: #ef4444;
              }}
              AnimatedButton[hovered="true"] {{
                  background-color: rgba(239, 68, 68, 0.12);
                  border-color: rgba(239, 68, 68, 0.25);
              }}
              AnimatedButton[pressed_state="true"] {{
                  background-color: rgba(239, 68, 68, 0.03);
                  padding-top: 14px;
                  padding-bottom: 10px;
              }}
              AnimatedButton:disabled {{
                  background-color: rgba(0, 0, 0, 0.01);
                  color: #a8a29e;
                  border-color: rgba(0, 0, 0, 0.02);
              }}
          """
          
          # Clear Button
          clear_btn_style = f"""
              AnimatedButton {{
                  background-color: rgba(0, 0, 0, 0.02);
                  border: 1px solid rgba(0, 0, 0, 0.06);
                  border-radius: 12px;
                  font-weight: bold;
                  font-size: 13px;
                  color: #78716c;
              }}
              AnimatedButton[hovered="true"] {{
                  background-color: rgba(0, 0, 0, 0.05);
                  border-color: rgba(0, 0, 0, 0.12);
                  color: #1c1917;
              }}
              AnimatedButton[pressed_state="true"] {{
                  background-color: rgba(0, 0, 0, 0.01);
                  padding-top: 14px;
                  padding-bottom: 10px;
              }}
          """
      else:
          # Dark mode colors (Original implementation)
          bg_end = self.current_theme["bg_gradient_end"]
          
          self.countdown_label.setStyleSheet(
              f"background: transparent; color: {primary}; letter-spacing: 2px;"
          )
          
          dynamic_style = f"""
              QMainWindow {{
                  background: qradialgradient(cx:0.5, cy:0.5, radius:1.0, fx:0.5, fy:0.5,
                      stop:0 #050508,
                      stop:1 {bg_end});
              }}
              #BentoCard {{
                  border-color: rgba({self.hex_to_rgb(primary)}, 0.08);
              }}
              QComboBox::down-arrow, QDateTimeEdit::down-arrow {{
                  border-top-color: {primary};
              }}
              QRadioButton:checked {{
                  background-color: rgba({self.hex_to_rgb(primary)}, 0.12);
                  border-color: rgba({self.hex_to_rgb(primary)}, 0.4);
                  color: #ffffff;
              }}
              QProgressBar::chunk {{
                  background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                      stop:0 {primary},
                      stop:1 {secondary});
              }}
          """
          
          preset_btn_style = f"""
              AnimatedButton {{
                  background-color: rgba(255, 255, 255, 0.02);
                  border: 1px solid rgba(255, 255, 255, 0.04);
                  border-radius: 16px;
              }}
              AnimatedButton[hovered="true"] {{
                  background-color: rgba({self.hex_to_rgb(primary)}, 0.05);
                  border-color: rgba({self.hex_to_rgb(primary)}, 0.3);
              }}
              AnimatedButton[pressed_state="true"] {{
                  background-color: rgba({self.hex_to_rgb(primary)}, 0.02);
              }}
          """
          
          start_btn_style = f"""
              AnimatedButton {{
                  background-color: {primary};
                  border: 1px solid {primary};
                  border-radius: 12px;
                  font-weight: bold;
                  font-size: 13px;
                  color: #050508;
              }}
              AnimatedButton[hovered="true"] {{
                  background-color: {secondary};
                  border-color: {secondary};
              }}
              AnimatedButton[pressed_state="true"] {{
                  background-color: {accent};
                  border-color: {accent};
                  padding-top: 14px;
                  padding-bottom: 10px;
              }}
          """
          
          cancel_btn_style = f"""
              AnimatedButton {{
                  background-color: rgba(239, 68, 68, 0.08);
                  border: 1px solid rgba(239, 68, 68, 0.15);
                  border-radius: 12px;
                  font-weight: bold;
                  font-size: 13px;
                  color: #ef4444;
              }}
              AnimatedButton[hovered="true"] {{
                  background-color: rgba(239, 68, 68, 0.16);
                  border-color: rgba(239, 68, 68, 0.3);
              }}
              AnimatedButton[pressed_state="true"] {{
                  background-color: rgba(239, 68, 68, 0.05);
                  padding-top: 14px;
                  padding-bottom: 10px;
              }}
              AnimatedButton:disabled {{
                  background-color: rgba(255, 255, 255, 0.01);
                  color: #52525b;
                  border-color: rgba(255, 255, 255, 0.02);
              }}
          """
          
          clear_btn_style = f"""
              AnimatedButton {{
                  background-color: rgba(255, 255, 255, 0.02);
                  border: 1px solid rgba(255, 255, 255, 0.06);
                  border-radius: 12px;
                  font-weight: bold;
                  font-size: 13px;
                  color: #a1a1aa;
              }}
              AnimatedButton[hovered="true"] {{
                  background-color: rgba(255, 255, 255, 0.06);
                  border-color: rgba(255, 255, 255, 0.15);
                  color: #f4f4f5;
              }}
              AnimatedButton[pressed_state="true"] {{
                  background-color: rgba(255, 255, 255, 0.02);
                  padding-top: 14px;
                  padding-bottom: 10px;
              }}
          """

      current_style = self.styleSheet()
      if "/* DYNAMIC */" in current_style:
          base = current_style.split("/* DYNAMIC */")[0]
      else:
          base = current_style

      self.setStyleSheet(base + "/* DYNAMIC */" + dynamic_style)

      # Apply styles to buttons
      for btn in self.preset_buttons:
          btn.setStyleSheet(preset_btn_style)

      self.start_button.setStyleSheet(start_btn_style)
      self.cancel_button.setStyleSheet(cancel_btn_style)
      self.clear_button.setStyleSheet(clear_btn_style)
  ```

- [ ] **Step 3: Modify PresetCard Text Colors dynamically**
  Update `PresetCard` so that it doesn't hardcode text styles to light white/gray.
  In `PresetCard.__init__`:
  Instead of hardcoded:
  ```python
  value_label.setStyleSheet("background: transparent; color: #f4f4f5;")
  unit_label.setStyleSheet("background: transparent; color: #a1a1aa;")
  ```
  Omit the color stylesheets so that they inherit the custom font colors applied to `QWidget` in the main stylesheet (`#1c1917` for light mode, `#e4e4e7` for dark mode):
  ```python
  value_label.setStyleSheet("background: transparent;")
  unit_label.setStyleSheet("background: transparent;")
  ```
  Wait! Let's check how `value_label` and `unit_label` can be made to look good in both dark and light mode. Inheriting color from the parent is perfect, or we can use custom color selectors in the base stylesheet for `PresetCard QLabel` or adjust styling. Inheriting color is the cleanest and most `ponytail` (lazy but highly correct) approach.

- [ ] **Step 4: Verify UI loading & persistence**
  Run: `python shutdown_timer.py`
  Verify that the application launches, changes theme, is visually correct in Light mode, saves settings to `window_config.json`, and loads back up in the correct theme on next launch.

- [ ] **Step 5: Commit Task 3**
  Run: `git commit -am "feat: update stylesheets for light and dark modes"`

---

### Task 4: Documentation & Final Cleanup

**Files:**
- Modify: [README.md](file:///d:/Windows%20Shutdown%20Timer/README.md)

- [ ] **Step 1: Update Feature list in `README.md`**
  Add details about the Theme Toggle button and "Warm Premium Cream" Light Mode in the features section.

- [ ] **Step 2: Update Changelog in `README.md`**
  Add a new changelog entry for v1.8.0 under `## Changelog` detailing the theme support, header layout, and Light mode implementation.

- [ ] **Step 3: Run git commit and push**
  Commit README.md changes.
  ```bash
  git commit -am "docs: update README with theme system changes"
  ```

---

### Task 5: Theme Toggle Button Initializer & Contrast Patch

**Files:**
- Modify: [shutdown_timer.py](file:///d:/Windows%20Shutdown%20Timer/shutdown_timer.py)

- [ ] **Step 1: Modify `apply_styles` to call `update_theme_button_ui()`**
  At the end of `apply_styles()`, add `self.update_theme_button_ui()` to ensure the toggle button's text is loaded immediately when the app starts.
  ```python
  # In ShutdownTimerApp.apply_styles:
  self.setStyleSheet(base_style)
  self.update_theme_button_ui()
  ```

- [ ] **Step 2: Update contrast styling of QPushButton#themeButton in base stylesheets**
  Enhance background and border opacities of `QPushButton#themeButton` in `apply_styles()` for both light and dark CSS strings.
  - In dark mode CSS:
    - `background-color`: from `0.03` to `0.06`
    - `border`: from `0.08` to `0.16`
    - `hover background-color`: from `0.08` to `0.12`
    - `hover border-color`: from `0.15` to `0.25`
  - In light mode CSS:
    - `background-color`: set to `rgba(0, 0, 0, 0.05)`
    - `border`: set to `rgba(0, 0, 0, 0.12)`
    - `hover background-color`: set to `rgba(0, 0, 0, 0.1)`
    - `hover border-color`: set to `rgba(0, 0, 0, 0.2)`

- [ ] **Step 3: Verify toggle text is visible on first startup**
  Run: `python shutdown_timer.py`
  Verify that the button displays "☀️ Light Mode" when opening in dark mode, and "🌙 Dark Mode" when opening in light mode.

- [ ] **Step 4: Re-compile the standalone executable**
  Run PyInstaller: `pyinstaller --noconfirm --clean "Windows Shutdown Timer.spec"`
  Verify new build succeeds.

- [ ] **Step 5: Commit changes**
  Run: `git commit -am "fix: resolve theme toggle visibility bug and update contrast"`

---

### Task 6: Dark Mode Bento Border Opacity & QMessageBox Rich Text Fix

**Files:**
- Modify: [shutdown_timer.py](file:///d:/Windows%20Shutdown%20Timer/shutdown_timer.py)

- [ ] **Step 1: Increase base Bento Card border opacity in dark mode**
  In `apply_styles()`, locate the dark mode style definition for `#BentoCard` and change `border: 1px solid rgba(255, 255, 255, 0.04);` to `rgba(255, 255, 255, 0.12)`.

- [ ] **Step 2: Increase active theme glow border opacity in dark mode**
  In `update_theme_colors()`, locate the block for dark mode styling and change `border-color: rgba({self.hex_to_rgb(primary)}, 0.08);` to `rgba({self.hex_to_rgb(primary)}, 0.25);`.

- [ ] **Step 3: Remove markdown formatting from QMessageBox strings**
  Locate confirmation dialog strings containing `**โปรดบันทึกงานของคุณก่อนดำเนินการครับ!**` and remove the `**` asterisks so that Qt interprets the strings as Plain Text, avoiding the Windows HTML black-text color bug.
  - Fix in `start_timer()` confirmation dialog
  - Fix in `start_preset_timer()` confirmation dialog
  - Fix in `immediate_action()` confirmation dialog

- [ ] **Step 4: Verify bento card borders and QMessageBox text colors**
  Run `python shutdown_timer.py` and trigger timer/presets. Verify that bento card borders are clearly visible in dark mode, and that confirmation dialog text is fully readable in both light and dark modes.

- [ ] **Step 5: Re-compile the standalone executable**
  Run PyInstaller: `pyinstaller --noconfirm --clean "Windows Shutdown Timer.spec"`
  Verify new build succeeds.

- [ ] **Step 6: Commit changes**
  Run: `git commit -am "fix: enhance dark mode bento card borders and resolve QMessageBox text visibility"`

---

### Task 7: Global QMessageBox QSS Styling & Segoe UI Variable Font Upgrade

**Files:**
- Modify: [shutdown_timer.py](file:///d:/Windows%20Shutdown%20Timer/shutdown_timer.py)

- [ ] **Step 1: Upgrade to Segoe UI Variable font stack**
  - Update all `QFont` calls to use `"Segoe UI Variable Display"` (headers, card title, presets values) and `"Segoe UI Variable Text"` (descriptions, units, status label).
  - Update CSS stylesheets `font-family` to `'Segoe UI Variable Display', 'Segoe UI Variable Text', 'Segoe UI', -apple-system, sans-serif;` for `QWidget`, `QLabel`, `QMessageBox`, etc.

- [ ] **Step 2: Add explicit QMessageBox QSS styling rules**
  In `apply_styles()`, add styling rules for `QMessageBox`, `QMessageBox QLabel`, and `QMessageBox QPushButton` for both Light and Dark mode stylesheets. Include rounded corners, borders, backgrounds, and appropriate readable text colors.

- [ ] **Step 3: Apply styles to global QApplication instance**
  In `apply_styles()`, call `QApplication.instance().setStyleSheet(base_style)` right after `self.setStyleSheet(base_style)`.

- [ ] **Step 4: Delay currentIndexChanged signal connection**
  In `init_ui()`, remove `self.action_combo.currentIndexChanged.connect(...)`. Connect it in `__init__` right after `self.load_settings()`.

- [ ] **Step 5: Verify QMessageBox readability and font aesthetics**
  Run `python shutdown_timer.py` in both Light and Dark modes. Trigger confirmation dialogs and verify QMessageBox text is fully readable (proper background and white/charcoal text) and that fonts look premium.

- [ ] **Step 6: Re-compile the standalone executable**
  Run PyInstaller: `pyinstaller --onefile --windowed --name="Windows Shutdown Timer" --icon=icon.ico shutdown_timer.py --noconfirm --clean`
  Verify new build succeeds.

- [ ] **Step 7: Commit changes**
  Run: `git commit -am "fix: style QMessageBox globally, upgrade to Segoe UI Variable font stack, and optimize signal connections"`
