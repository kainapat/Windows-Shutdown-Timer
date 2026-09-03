# -*- coding: utf-8 -*-

import sys
import os
import json
import logging
import subprocess
from datetime import datetime, timedelta

# PySide6 Imports
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QDateEdit,
    QDateTimeEdit,
    QMessageBox,
    QRadioButton,
    QButtonGroup,
    QGroupBox,
    QGridLayout,
    QStackedWidget,
    QGraphicsDropShadowEffect,
    QProgressBar,
    QFrame,
    QSpinBox,
    QSizePolicy,
    QLayout,
)
from PySide6.QtCore import (
    QTimer,
    QDateTime,
    Qt,
    QLocale,
    QDate,
    QTime,
    QPropertyAnimation,
    QEasingCurve,
    QPoint,
    QParallelAnimationGroup,
    QSize,
)
from PySide6.QtGui import (
    QFont,
    QColor,
    QFontDatabase,
    QIcon,
    QPixmap,
)

CONFIG_FILE = "timer_config.json"
WINDOW_CONFIG_FILE = "window_config.json"


def resource_path(relative_name: str) -> str:
    """Return absolute path to a bundled resource.

    Works in two environments:
    - Development  : resolves relative to the directory that contains this script.
    - PyInstaller  : resolves relative to sys._MEIPASS (the temp extraction dir).
    """
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_name)

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter("%(asctime)s │ %(message)s", datefmt="%H:%M:%S"))
logger.addHandler(_handler)

# --- Color Themes for Each Action ---
ACTION_COLORS = {
    0: {  # Shutdown - Red Accent
        "name": "shutdown",
        "primary": "#ff3b5c",
        "secondary": "#ff8599",
        "accent": "#e6002e",
        "bg_gradient_end": "#18060a",
        "progress": "#ff3b5c",
        "icon": "🔌",
        "label": "Shutdown (ปิดเครื่อง)",
        "label_en": "Shutdown",
        "label_th": "ปิดเครื่อง",
    },
    1: {  # Restart - Orange Accent
        "name": "restart",
        "primary": "#ff9500",
        "secondary": "#ffc470",
        "accent": "#d67d00",
        "bg_gradient_end": "#180c05",
        "progress": "#ff9500",
        "icon": "🔄",
        "label": "Restart (รีสตาร์ท)",
        "label_en": "Restart",
        "label_th": "รีสตาร์ท",
    },
    2: {  # Sleep - Blue Accent
        "name": "sleep",
        "primary": "#007aff",
        "secondary": "#70b4ff",
        "accent": "#0056b3",
        "bg_gradient_end": "#050c18",
        "progress": "#007aff",
        "icon": "😴",
        "label": "Sleep (พักเครื่อง)",
        "label_en": "Sleep",
        "label_th": "พักเครื่อง",
    },
    3: {  # Hibernate - Purple Accent
        "name": "hibernate",
        "primary": "#a855f7",
        "secondary": "#d8b4fe",
        "accent": "#7e22ce",
        "bg_gradient_end": "#120518",
        "progress": "#a855f7",
        "icon": "🌙",
        "label": "Hibernate (จำศีล)",
        "label_en": "Hibernate",
        "label_th": "จำศีล",
    },
}

# --- Unicode Icons ---
ICONS = {
    "start": "▶",
    "cancel": "✕",
    "clear": "⌫",
    "clock": "⏱",
    "calendar": "📅",
    "timer": "⏲",
}

# --- Preset Data ---
PRESETS = [
    {"value": 15, "unit": "minutes", "icon": "⚡", "label": "15", "sublabel": "Min (นาที)", "unit_en": "mins", "unit_th": "นาที"},
    {"value": 30, "unit": "minutes", "icon": "⚡", "label": "30", "sublabel": "Min (นาที)", "unit_en": "mins", "unit_th": "นาที"},
    {"value": 1, "unit": "hours", "icon": "⏰", "label": "1", "sublabel": "Hr (ชม.)", "unit_en": "hour", "unit_th": "ชั่วโมง"},
    {"value": 2, "unit": "hours", "icon": "⏰", "label": "2", "sublabel": "Hrs (ชม.)", "unit_en": "hours", "unit_th": "ชั่วโมง"},
]


def get_modern_font_name():
    """Return the most modern, loopless Thai sans-serif font available on the system."""
    try:
        families = QFontDatabase.families()
    except Exception:
        families = []
    for candidate in [
        "IBM Plex Sans Thai",
        "Kanit",
        "Leelawadee UI",
        "Segoe UI Variable Display",
        "Segoe UI",
        "sans-serif",
    ]:
        if candidate in families:
            return candidate
    return "sans-serif"


def get_modern_font(size=10, weight=QFont.Normal, bold=False):
    """Create a QFont instance using the preferred modern loopless typeface."""
    font = QFont(get_modern_font_name(), size)
    if bold:
        font.setBold(True)
    elif weight != QFont.Normal:
        font.setWeight(weight)
    return font


class AnimatedButton(QPushButton):
    """Button with smooth scale physics and accent hover glow"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)
        
        # Shadow / Glow setup
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(12)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.shadow.setOffset(0, 4)
        self.setGraphicsEffect(self.shadow)

    def enterEvent(self, event):
        self.shadow.setBlurRadius(18)
        self.shadow.setOffset(0, 5)
        self.setProperty("hovered", True)
        self.style().unpolish(self)
        self.style().polish(self)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.shadow.setBlurRadius(12)
        self.shadow.setOffset(0, 4)
        self.setProperty("hovered", False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.setProperty("pressed_state", True)
        self.style().unpolish(self)
        self.style().polish(self)
        self.shadow.setOffset(0, 1)
        self.shadow.setBlurRadius(6)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setProperty("pressed_state", False)
        self.style().unpolish(self)
        self.style().polish(self)
        self.shadow.setOffset(0, 4)
        self.shadow.setBlurRadius(12)
        super().mouseReleaseEvent(event)


class PresetCard(AnimatedButton):
    """Glassmorphism preset card button with scale hover feedback"""

    def __init__(self, icon, label, sublabel, parent=None):
        super().__init__("", parent)
        self.setObjectName("presetCard")
        self.setMinimumHeight(70)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(6, 6, 6, 6)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setObjectName("presetIcon")
        icon_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        value_label = QLabel(label)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setFont(get_modern_font(15, bold=True))
        value_label.setObjectName("presetValue")
        value_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        unit_label = QLabel(sublabel)
        unit_label.setAlignment(Qt.AlignCenter)
        unit_label.setFont(get_modern_font(9))
        unit_label.setObjectName("presetUnit")
        unit_label.setAttribute(Qt.WA_TransparentForMouseEvents)

        layout.addWidget(icon_label)
        layout.addWidget(value_label)
        layout.addWidget(unit_label)

    def sizeHint(self):
        return QSize(80, 72)

    def minimumSizeHint(self):
        return QSize(60, 70)


class BentoCard(QFrame):
    """Machined glass-like enclosure representing Bento grid sections"""

    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("bentoCard")
        
        self.card_layout = QVBoxLayout(self)
        self.card_layout.setContentsMargins(16, 14, 16, 14)
        self.card_layout.setSpacing(10)
        self.card_layout.setSizeConstraint(QLayout.SetMinimumSize)

        if title:
            self.title_label = QLabel(title)
            self.title_label.setObjectName("bentoCardTitle")
            self.title_label.setFont(get_modern_font(11, weight=QFont.DemiBold))
            self.card_layout.addWidget(self.title_label)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(18)
        shadow.setColor(QColor(0, 0, 0, 45))
        shadow.setOffset(0, 6)
        self.setGraphicsEffect(shadow)

    @property
    def layout(self):
        return self.card_layout

    def sizeHint(self):
        return self.card_layout.sizeHint()

    def minimumSizeHint(self):
        return self.card_layout.minimumSize()


class SlidingStackedWidget(QStackedWidget):
    """QStackedWidget with smooth horizontal slide transition animation"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_speed = 250
        self.m_easing = QEasingCurve.OutCubic
        self.m_active = False

    def slide_to_index(self, idx):
        if self.m_active or self.currentIndex() == idx:
            return
            
        self.m_active = True
        offsetx = self.width()
        
        idx_curr = self.currentIndex()
        idx_next = idx
        
        w_curr = self.widget(idx_curr)
        w_next = self.widget(idx_next)
        
        w_next.setGeometry(0, 0, self.width(), self.height())
        
        # Determine slide direction
        if idx_next > idx_curr:
            p_curr_start = QPoint(0, 0)
            p_curr_end = QPoint(-offsetx, 0)
            p_next_start = QPoint(offsetx, 0)
            p_next_end = QPoint(0, 0)
        else:
            p_curr_start = QPoint(0, 0)
            p_curr_end = QPoint(offsetx, 0)
            p_next_start = QPoint(-offsetx, 0)
            p_next_end = QPoint(0, 0)
            
        w_next.move(p_next_start)
        w_next.show()
        w_next.raise_()
        
        self.anim_curr = QPropertyAnimation(w_curr, b"pos")
        self.anim_curr.setDuration(self.m_speed)
        self.anim_curr.setEasingCurve(self.m_easing)
        self.anim_curr.setStartValue(p_curr_start)
        self.anim_curr.setEndValue(p_curr_end)
        
        self.anim_next = QPropertyAnimation(w_next, b"pos")
        self.anim_next.setDuration(self.m_speed)
        self.anim_next.setEasingCurve(self.m_easing)
        self.anim_next.setStartValue(p_next_start)
        self.anim_next.setEndValue(p_next_end)
        
        self.anim_group = QParallelAnimationGroup(self)
        self.anim_group.addAnimation(self.anim_curr)
        self.anim_group.addAnimation(self.anim_next)
        
        def on_finished():
            self.setCurrentIndex(idx_next)
            w_curr.hide()
            w_curr.move(0, 0)
            self.m_active = False
            
        self.anim_group.finished.connect(on_finished)
        self.anim_group.start()


class SpinBoxProxy:
    """Proxy providing QSpinBox API compatibility over a QComboBox."""

    def __init__(self, combo: QComboBox, max_val: int = 59):
        self._combo = combo
        self._max_val = max_val

    def value(self) -> int:
        return self._combo.currentIndex()

    def setValue(self, val: int):
        safe_val = max(0, min(int(val), self._max_val))
        self._combo.setCurrentIndex(safe_val)

    def setRange(self, min_val: int, max_val: int):
        self._max_val = max_val

    def __getattr__(self, name):
        return getattr(self._combo, name)


class DateTimeProxy:
    """Proxy providing QDateTimeEdit API compatibility over QDateEdit and Hour/Minute QComboBoxes."""

    def __init__(self, date_picker: QDateEdit, hour_combo: QComboBox, min_combo: QComboBox):
        self._date_picker = date_picker
        self._hour_combo = hour_combo
        self._min_combo = min_combo

    def dateTime(self) -> QDateTime:
        d = self._date_picker.date()
        h = self._hour_combo.currentIndex()
        m = self._min_combo.currentIndex()
        return QDateTime(d, QTime(h, m, 0))

    def date(self) -> QDate:
        return self._date_picker.date()

    def time(self) -> QTime:
        h = self._hour_combo.currentIndex()
        m = self._min_combo.currentIndex()
        return QTime(h, m, 0)

    def setDateTime(self, dt: QDateTime):
        if isinstance(dt, QDateTime) and dt.isValid():
            self._date_picker.setDate(dt.date())
            self._hour_combo.setCurrentIndex(max(0, min(dt.time().hour(), 23)))
            self._min_combo.setCurrentIndex(max(0, min(dt.time().minute(), 59)))

    def setDate(self, d: QDate):
        if isinstance(d, QDate) and d.isValid():
            self._date_picker.setDate(d)

    def setTime(self, t: QTime):
        if isinstance(t, QTime) and t.isValid():
            self._hour_combo.setCurrentIndex(max(0, min(t.hour(), 23)))
            self._min_combo.setCurrentIndex(max(0, min(t.minute(), 59)))

    def __getattr__(self, name):
        return getattr(self._date_picker, name)


class Toast(QWidget):
    """Modern toast notification with cinematic entry & exit animation"""

    def __init__(self, parent, message, duration=3000, type_="info"):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        configs = {
            "info":    {"bg": "rgba(30, 102, 245, 0.92)", "fg": "#ffffff", "icon": "ℹ️"},
            "success": {"bg": "rgba(46, 140, 34, 0.92)", "fg": "#ffffff", "icon": "✅"},
            "warning": {"bg": "rgba(217, 119, 6, 0.92)", "fg": "#ffffff", "icon": "⚠️"},
            "error":   {"bg": "rgba(220, 38, 38, 0.92)", "fg": "#ffffff", "icon": "❌"},
        }
        cfg = configs.get(type_, configs["info"])

        self.setStyleSheet(f"""
            QWidget#toastBody {{
                background-color: {cfg['bg']};
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 12px;
            }}
            QLabel {{
                background: transparent;
                color: {cfg['fg']};
                font-size: 12.5px;
                font-weight: bold;
                font-family: 'IBM Plex Sans Thai', 'Kanit', 'Segoe UI Variable Display', 'Segoe UI Variable Text', 'Leelawadee UI', 'Prompt', 'Segoe UI', -apple-system, sans-serif;
            }}
        """)

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        body = QWidget()
        body.setObjectName("toastBody")

        shadow = QGraphicsDropShadowEffect(body)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 4)
        body.setGraphicsEffect(shadow)

        layout = QHBoxLayout(body)
        layout.setContentsMargins(16, 10, 16, 10)
        layout.setSpacing(8)

        icon_label = QLabel(cfg["icon"])
        icon_label.setStyleSheet("font-size: 15px;")
        layout.addWidget(icon_label)

        self.label = QLabel(message)
        layout.addWidget(self.label)

        outer.addWidget(body)

        self.duration = duration

    def showEvent(self, event):
        super().showEvent(event)
        self.adjustSize()
        parent = self.parent()
        if parent:
            x = parent.width() // 2 - self.width() // 2
            y = 20
            self.move(x, y)

        # Slide down & fade entry
        self.anim_pos = QPropertyAnimation(self, b"pos")
        self.anim_pos.setDuration(300)
        self.anim_pos.setEasingCurve(QEasingCurve.OutBack)
        self.anim_pos.setStartValue(QPoint(self.x(), self.y() - 30))
        self.anim_pos.setEndValue(QPoint(self.x(), self.y()))
        self.anim_pos.start()

        self.anim_opacity = QPropertyAnimation(self, b"windowOpacity")
        self.anim_opacity.setDuration(200)
        self.anim_opacity.setStartValue(0.0)
        self.anim_opacity.setEndValue(1.0)
        self.anim_opacity.start()

        QTimer.singleShot(self.duration, self.hide_animation)

    def hide_animation(self):
        self.anim_fade = QPropertyAnimation(self, b"windowOpacity")
        self.anim_fade.setDuration(250)
        self.anim_fade.setStartValue(1.0)
        self.anim_fade.setEndValue(0.0)
        self.anim_fade.finished.connect(self.close)
        self.anim_fade.start()


class ShutdownTimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows Shutdown Timer")

        # Set application / taskbar icon (prefer .ico for multi-resolution support)
        icon_path = resource_path("off.ico")
        if not os.path.isfile(icon_path):
            icon_path = resource_path("off.png")
        if os.path.isfile(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setMinimumSize(580, 750)
        self.resize(600, 760)

        # State variables
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.target_shutdown_time = None
        self.is_timer_active = False
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.current_theme = ACTION_COLORS[0]
        self.current_toast = None
        self.current_theme_mode = "dark"

        self.init_ui()
        self.load_window_settings()
        self.load_settings()
        self.action_combo.currentIndexChanged.connect(self.on_action_changed)
        self.apply_styles()
        self.update_theme_colors(self.action_combo.currentIndex())
        logger.info("🚀 Application started with 3-Step Vertical Flow design")

    def init_ui(self):
        """Create and arrange widgets in a 3-Step Vertical Flow architecture"""
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(12)
        main_layout.setContentsMargins(18, 16, 18, 16)

        # --- 1. Header Layout ---
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(4, 0, 4, 2)

        self.title_label = QLabel("Windows Shutdown Timer")
        self.title_label.setObjectName("appTitle")
        self.title_label.setFont(get_modern_font(16, bold=True))
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        self.theme_button = QPushButton()
        self.theme_button.setObjectName("themeButton")
        self.theme_button.setCursor(Qt.PointingHandCursor)
        self.theme_button.setFixedWidth(135)
        self.theme_button.setMinimumHeight(32)
        self.theme_button.setFont(get_modern_font(9, weight=QFont.DemiBold))
        self.theme_button.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_button)

        main_layout.addLayout(header_layout)

        # --- 2. Hero Section (Hero Card - Top) ---
        self.card_countdown = BentoCard("Countdown Display (หน้าจอนับถอยหลัง)", self)
        card_c_layout = self.card_countdown.layout
        card_c_layout.setSpacing(10)

        self.countdown_label = QLabel("00:00:00")
        self.countdown_label.setObjectName("countdownLabel")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        available_fonts = QFontDatabase().families()
        countdown_font_name = "JetBrains Mono" if "JetBrains Mono" in available_fonts else \
                              "Consolas" if "Consolas" in available_fonts else \
                              "Courier New"
        countdown_font = QFont(countdown_font_name, 44, QFont.Bold)
        countdown_font.setFixedPitch(True)
        self.countdown_label.setFont(countdown_font)
        self.countdown_label.setStyleSheet("background: transparent; letter-spacing: 2px;")

        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setMinimumHeight(14)
        self.progress_bar.setMaximumHeight(14)

        self.status_label = QLabel("Status: Ready / Idle (สถานะ: ยังไม่ได้เริ่มนับถอยหลัง)")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(get_modern_font(10))

        card_c_layout.addWidget(self.countdown_label)
        card_c_layout.addWidget(self.progress_bar)
        card_c_layout.addWidget(self.status_label)
        main_layout.addWidget(self.card_countdown)

        # --- 3. Step 1 Card: Action Selector ---
        self.card_action = BentoCard("1. Select Action (เลือกการกระทำ)", self)
        card_action_layout = self.card_action.layout
        card_action_layout.setSpacing(8)

        # Hidden combo box preserved for state & legacy API compatibility
        self.action_combo = QComboBox()
        self.action_combo.addItem(f"{ACTION_COLORS[0]['icon']} {ACTION_COLORS[0]['label']}")
        self.action_combo.addItem(f"{ACTION_COLORS[1]['icon']} {ACTION_COLORS[1]['label']}")
        self.action_combo.addItem(f"{ACTION_COLORS[2]['icon']} {ACTION_COLORS[2]['label']}")
        self.action_combo.addItem(f"{ACTION_COLORS[3]['icon']} {ACTION_COLORS[3]['label']}")
        self.action_combo.setVisible(False)

        action_row = QHBoxLayout()
        action_row.setSpacing(8)

        self.action_buttons = []
        self.action_button_group = QButtonGroup(self)
        self.action_button_group.setExclusive(True)

        for i in range(4):
            info = ACTION_COLORS[i]
            btn = QPushButton(f"{info['icon']} {info['label']}")
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(38)
            btn.setObjectName("actionPill")
            btn.setFont(get_modern_font(9.5, weight=QFont.DemiBold))
            btn.clicked.connect(lambda checked, idx=i: self.action_combo.setCurrentIndex(idx))
            self.action_button_group.addButton(btn, i)
            self.action_buttons.append(btn)
            action_row.addWidget(btn)

        self.action_buttons[0].setChecked(True)
        card_action_layout.addLayout(action_row)
        main_layout.addWidget(self.card_action)

        # Backward compatibility alias
        self.card_action_mode = self.card_action

        # --- 4. Step 2 Card: Set Time ---
        self.card_time = BentoCard("2. Set Time (กำหนดเวลา)", self)
        card_time_layout = self.card_time.layout
        card_time_layout.setSpacing(10)

        # Sub-layout A: Quick Presets (Horizontal row)
        presets_row = QHBoxLayout()
        presets_row.setSpacing(8)

        self.preset_buttons = []
        for i, preset in enumerate(PRESETS):
            btn = PresetCard(preset["icon"], preset["label"], preset["sublabel"])
            btn.clicked.connect(
                lambda checked,
                v=preset["value"],
                u=preset["unit"]: self.start_preset_timer(v, u)
            )
            self.preset_buttons.append(btn)
            presets_row.addWidget(btn)

        card_time_layout.addLayout(presets_row)

        # Sub-layout B: Mode Switcher (Pill Radio buttons)
        mode_switcher_layout = QHBoxLayout()
        mode_switcher_layout.setSpacing(8)

        self.mode_button_group = QButtonGroup(self)
        self.radio_timer = QRadioButton("⏱ Timer (นับถอยหลัง)")
        self.radio_timer.setObjectName("modeRadio")
        self.radio_clock = QRadioButton("📅 Clock (ระบุเวลาจริง)")
        self.radio_clock.setObjectName("modeRadio")

        self.mode_button_group.addButton(self.radio_timer, 0)
        self.mode_button_group.addButton(self.radio_clock, 1)
        self.mode_button_group.idToggled.connect(self.on_mode_toggled)

        self.radio_timer.setChecked(True)

        # Backward compatibility aliases
        self.radio_datetime = self.radio_clock
        self.radio_hours = self.radio_timer
        self.radio_minutes = self.radio_timer
        self.radio_seconds = self.radio_timer

        mode_switcher_layout.addWidget(self.radio_timer)
        mode_switcher_layout.addWidget(self.radio_clock)
        card_time_layout.addLayout(mode_switcher_layout)

        # Sub-layout C: Time Inputs (Sliding Stacked Widget)
        self.time_stack = SlidingStackedWidget()

        # Page 0: Timer mode with Dropdowns (3-column layout)
        self.timer_page = QWidget()
        timer_input_layout = QHBoxLayout(self.timer_page)
        timer_input_layout.setContentsMargins(4, 2, 4, 2)
        timer_input_layout.setSpacing(10)

        # Hours Dropdown
        h_layout = QVBoxLayout()
        h_layout.setSpacing(2)
        lbl_h = QLabel("Hours (ชั่วโมง)")
        lbl_h.setObjectName("timeUnitLabel")
        lbl_h.setAlignment(Qt.AlignCenter)
        self.hours_combo = QComboBox()
        self.hours_combo.setObjectName("timeComboBox")
        self.hours_combo.addItems([f"{i} hr" for i in range(25)])
        self.hours_combo.setCurrentIndex(0)
        self.hours_combo.setMinimumHeight(38)
        h_layout.addWidget(lbl_h)
        h_layout.addWidget(self.hours_combo)

        # Minutes Dropdown
        m_layout = QVBoxLayout()
        m_layout.setSpacing(2)
        lbl_m = QLabel("Minutes (นาที)")
        lbl_m.setObjectName("timeUnitLabel")
        lbl_m.setAlignment(Qt.AlignCenter)
        self.minutes_combo = QComboBox()
        self.minutes_combo.setObjectName("timeComboBox")
        self.minutes_combo.addItems([f"{i} min" for i in range(60)])
        self.minutes_combo.setCurrentIndex(30)
        self.minutes_combo.setMinimumHeight(38)
        m_layout.addWidget(lbl_m)
        m_layout.addWidget(self.minutes_combo)

        # Seconds Dropdown
        s_layout = QVBoxLayout()
        s_layout.setSpacing(2)
        lbl_s = QLabel("Seconds (วินาที)")
        lbl_s.setObjectName("timeUnitLabel")
        lbl_s.setAlignment(Qt.AlignCenter)
        self.seconds_combo = QComboBox()
        self.seconds_combo.setObjectName("timeComboBox")
        self.seconds_combo.addItems([f"{i} sec" for i in range(60)])
        self.seconds_combo.setCurrentIndex(0)
        self.seconds_combo.setMinimumHeight(38)
        s_layout.addWidget(lbl_s)
        s_layout.addWidget(self.seconds_combo)

        timer_input_layout.addLayout(h_layout)
        timer_input_layout.addLayout(m_layout)
        timer_input_layout.addLayout(s_layout)

        # Compatibility proxies for legacy spinbox access
        self.spin_hours = SpinBoxProxy(self.hours_combo, 24)
        self.spin_minutes = SpinBoxProxy(self.minutes_combo, 59)
        self.spin_seconds = SpinBoxProxy(self.seconds_combo, 59)

        # Page 1: Clock mode with Date picker + Hour/Minute dropdowns (Symmetrical 3-column layout)
        self.clock_page = QWidget()
        clock_layout = QHBoxLayout(self.clock_page)
        clock_layout.setContentsMargins(4, 2, 4, 2)
        clock_layout.setSpacing(10)

        # Column 1: Date Picker with Calendar Popup
        date_col_layout = QVBoxLayout()
        date_col_layout.setSpacing(2)
        lbl_date = QLabel("Date (วันที่)")
        lbl_date.setObjectName("timeUnitLabel")
        lbl_date.setAlignment(Qt.AlignCenter)
        self.date_picker = QDateEdit()
        self.date_picker.setObjectName("datePicker")
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDisplayFormat("ddd d MMM yyyy")
        self.date_picker.setMinimumHeight(38)
        self.date_picker.setAlignment(Qt.AlignCenter)
        date_col_layout.addWidget(lbl_date)
        date_col_layout.addWidget(self.date_picker)

        # Column 2: Hours Dropdown
        clock_h_layout = QVBoxLayout()
        clock_h_layout.setSpacing(2)
        lbl_clock_h = QLabel("Hours (ชั่วโมง)")
        lbl_clock_h.setObjectName("timeUnitLabel")
        lbl_clock_h.setAlignment(Qt.AlignCenter)
        self.time_hours_combo = QComboBox()
        self.time_hours_combo.setObjectName("timeComboBox")
        self.time_hours_combo.addItems([f"{i:02d}" for i in range(24)])
        self.time_hours_combo.setMinimumHeight(38)
        clock_h_layout.addWidget(lbl_clock_h)
        clock_h_layout.addWidget(self.time_hours_combo)

        # Column 3: Minutes Dropdown
        clock_m_layout = QVBoxLayout()
        clock_m_layout.setSpacing(2)
        lbl_clock_m = QLabel("Minutes (นาที)")
        lbl_clock_m.setObjectName("timeUnitLabel")
        lbl_clock_m.setAlignment(Qt.AlignCenter)
        self.time_minutes_combo = QComboBox()
        self.time_minutes_combo.setObjectName("timeComboBox")
        self.time_minutes_combo.addItems([f"{i:02d}" for i in range(60)])
        self.time_minutes_combo.setMinimumHeight(38)
        clock_m_layout.addWidget(lbl_clock_m)
        clock_m_layout.addWidget(self.time_minutes_combo)

        clock_layout.addLayout(date_col_layout)
        clock_layout.addLayout(clock_h_layout)
        clock_layout.addLayout(clock_m_layout)

        # Initialize Clock default to now + 1 hour
        init_dt = QDateTime.currentDateTime().addSecs(3600)
        self.date_picker.setDate(init_dt.date())
        self.time_hours_combo.setCurrentIndex(init_dt.time().hour())
        self.time_minutes_combo.setCurrentIndex(init_dt.time().minute())

        # Compatibility proxy for QDateTimeEdit access
        self.date_edit = DateTimeProxy(self.date_picker, self.time_hours_combo, self.time_minutes_combo)

        # Legacy widget aliases to ensure full backward compatibility
        self.datetime_page = self.clock_page
        self.hours_page = self.timer_page
        self.minutes_page = self.timer_page
        self.seconds_page = self.timer_page

        self.time_stack.addWidget(self.timer_page)
        self.time_stack.addWidget(self.clock_page)
        self.time_stack.setFixedHeight(68)

        card_time_layout.addWidget(self.time_stack)
        main_layout.addWidget(self.card_time)

        # Backward compatibility aliases
        self.card_time_input = self.card_time
        self.card_presets = self.card_time

        # --- 5. Step 3 Card: Action Controls ---
        self.card_controls = BentoCard("3. Controls (เริ่มการทำงาน)", self)
        card_controls_layout = self.card_controls.layout
        card_controls_layout.setSpacing(8)

        self.start_button = AnimatedButton(f"{ICONS['start']} Start Countdown (เริ่มนับถอยหลัง)")
        self.start_button.setObjectName("startButton")
        self.start_button.setMinimumHeight(44)
        self.start_button.setFont(get_modern_font(12, bold=True))
        self.start_button.setToolTip("Start countdown and schedule action (เริ่มนับถอยหลังและตั้งเวลาการทำงาน)")

        controls_row = QHBoxLayout()
        controls_row.setSpacing(8)

        self.cancel_button = AnimatedButton(f"{ICONS['cancel']} Cancel (ยกเลิก)")
        self.cancel_button.setObjectName("cancelButton")
        self.clear_button = AnimatedButton("↺ Reset (ล้างค่า)")
        self.clear_button.setObjectName("clearButton")

        self.cancel_button.setEnabled(False)
        self.cancel_button.setMinimumHeight(38)
        self.clear_button.setMinimumHeight(38)
        self.cancel_button.setFont(get_modern_font(10, weight=QFont.DemiBold))
        self.clear_button.setFont(get_modern_font(10, weight=QFont.DemiBold))

        self.cancel_button.setToolTip("Cancel scheduled timer (ยกเลิกการตั้งเวลาและหยุดการนับถอยหลัง)")
        self.clear_button.setToolTip("Reset all fields (ล้างค่าและรีเซ็ตการตั้งค่าทั้งหมด)")

        self.start_button.clicked.connect(self.start_timer)
        self.cancel_button.clicked.connect(self.cancel_timer)
        self.clear_button.clicked.connect(self.clear_fields)

        controls_row.addWidget(self.cancel_button)
        controls_row.addWidget(self.clear_button)

        card_controls_layout.addWidget(self.start_button)
        card_controls_layout.addLayout(controls_row)
        main_layout.addWidget(self.card_controls)

    def apply_styles(self):
        """Apply base stylesheet based on light or dark theme"""
        if self.current_theme_mode == "light":
            base_style = """
                QMainWindow, QWidget#centralWidget {
                    background-color: #d8dce2;
                }
                QWidget {
                    color: #334155;
                    font-family: 'IBM Plex Sans Thai', 'Kanit', 'Segoe UI Variable Display', 'Segoe UI Variable Text', 'Leelawadee UI', 'Prompt', 'Segoe UI', -apple-system, sans-serif;
                    font-size: 11pt;
                }
                QFrame#bentoCard, #bentoCard, #BentoCard {
                    background-color: #e8ecf1;
                    border: 1px solid #cbd5e1;
                    border-radius: 12px;
                }
                QLabel#bentoCardTitle, #bentoCardTitle, #BentoCardTitle {
                    color: #0f172a;
                    font-size: 13px;
                    font-weight: 600;
                    letter-spacing: 0.3px;
                    margin-bottom: 2px;
                    background: transparent;
                }
                QLabel {
                    color: #334155;
                    background-color: transparent;
                }
                QLabel#appTitle {
                    color: #0f172a;
                    font-size: 16px;
                    font-weight: bold;
                    background: transparent;
                }
                QLabel#statusLabel {
                    color: #475569;
                    font-size: 13px;
                    background: transparent;
                }
                QLabel#timeUnitLabel {
                    color: #475569;
                    font-size: 11px;
                    font-weight: 600;
                    background: transparent;
                }
                QLabel#clockLabel {
                    color: #334155;
                    font-size: 13px;
                    font-weight: 500;
                    background: transparent;
                }
                QSpinBox, QComboBox, QDateTimeEdit, QDateEdit {
                    background-color: #f8fafc;
                    border: 1px solid #94a3b8;
                    color: #0f172a;
                    border-radius: 6px;
                    padding: 4px 8px;
                    font-size: 13px;
                    min-width: 60px;
                }
                QSpinBox:hover, QComboBox:hover, QDateTimeEdit:hover, QDateEdit:hover {
                    border-color: #64748b;
                    background-color: #ffffff;
                }
                QSpinBox:focus, QComboBox:focus, QDateTimeEdit:focus, QDateEdit:focus {
                    border-color: #334155;
                    background-color: #ffffff;
                }
                QComboBox::drop-down, QDateTimeEdit::drop-down, QDateEdit::drop-down {
                    border: none;
                    width: 24px;
                }
                QComboBox::down-arrow, QDateTimeEdit::down-arrow, QDateEdit::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 5px solid #475569;
                    margin-right: 6px;
                }
                QSpinBox::up-button, QSpinBox::down-button {
                    border: none;
                    width: 18px;
                    background: transparent;
                }
                QSpinBox::up-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-bottom: 5px solid #475569;
                    width: 0;
                    height: 0;
                }
                QSpinBox::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 5px solid #475569;
                    width: 0;
                    height: 0;
                }
                QSpinBox::up-arrow:hover {
                    border-bottom-color: #0f172a;
                }
                QSpinBox::down-arrow:hover {
                    border-top-color: #0f172a;
                }
                QComboBox QAbstractItemView {
                    background-color: #f8fafc;
                    border: 1px solid #94a3b8;
                    border-radius: 8px;
                    padding: 4px;
                    color: #0f172a;
                    selection-background-color: #dbe0e6;
                    selection-color: #0f172a;
                    outline: none;
                }
                QComboBox QAbstractItemView QScrollBar:vertical {
                    background: transparent;
                    width: 6px;
                    margin: 2px 0 2px 0;
                }
                QComboBox QAbstractItemView QScrollBar::handle:vertical {
                    background: #cbd5e1;
                    border-radius: 3px;
                    min-height: 20px;
                }
                QComboBox QAbstractItemView QScrollBar::add-line:vertical,
                QComboBox QAbstractItemView QScrollBar::sub-line:vertical {
                    height: 0px;
                }
                QPushButton#actionPill {
                    background-color: #dbe0e6;
                    border: 1px solid #cbd5e1;
                    border-radius: 8px;
                    padding: 8px 10px;
                    color: #334155;
                    font-weight: 600;
                    font-size: 11.5px;
                }
                QPushButton#actionPill:hover {
                    background-color: #cbd5e1;
                    border-color: #94a3b8;
                    color: #0f172a;
                }
                QPushButton#actionPill:checked {
                    color: #ffffff;
                    font-weight: bold;
                }
                QRadioButton {
                    color: #334155;
                    spacing: 6px;
                    font-size: 12px;
                    background-color: #dbe0e6;
                    border: 1px solid #cbd5e1;
                    border-radius: 8px;
                    padding: 8px 14px;
                    font-weight: 500;
                }
                QRadioButton::indicator {
                    width: 0px;
                    height: 0px;
                }
                QRadioButton:hover {
                    border-color: #94a3b8;
                    color: #0f172a;
                    background-color: #cbd5e1;
                }
                QRadioButton:checked {
                    color: #0f172a;
                    font-weight: bold;
                    background-color: #ffffff;
                }
                AnimatedButton#presetCard, QPushButton#presetCard {
                    background-color: #f1f5f9;
                    border: 1px solid #cbd5e1;
                    border-radius: 16px;
                    color: #0f172a;
                }
                AnimatedButton#presetCard[hovered="true"], QPushButton#presetCard:hover {
                    background-color: #e2e8f0;
                    border-color: #94a3b8;
                }
                AnimatedButton#presetCard[pressed_state="true"], QPushButton#presetCard:pressed {
                    background-color: #cbd5e1;
                }
                #presetCard QLabel {
                    background: transparent;
                }
                #presetIcon {
                    font-size: 16px;
                    background: transparent;
                }
                #presetValue {
                    color: #0f172a;
                    font-size: 15px;
                    font-weight: bold;
                    background: transparent;
                }
                #presetUnit {
                    color: #475569;
                    font-size: 9pt;
                    background: transparent;
                }
                AnimatedButton {
                    background-color: #dbe0e6;
                    border: 1px solid #cbd5e1;
                    border-radius: 8px;
                    padding: 8px 14px;
                    font-weight: bold;
                    font-size: 13px;
                    color: #334155;
                }
                AnimatedButton[hovered="true"] {
                    background-color: #cbd5e1;
                    border-color: #94a3b8;
                    color: #0f172a;
                }
                AnimatedButton[pressed_state="true"] {
                    background-color: #94a3b8;
                    padding-top: 10px;
                    padding-bottom: 6px;
                }
                AnimatedButton:disabled {
                    background-color: #e8ecf1;
                    color: #94a3b8;
                    border-color: #cbd5e1;
                }
                QProgressBar {
                    border: 1px solid #94a3b8;
                    border-radius: 7px;
                    text-align: center;
                    background-color: #cbd5e1;
                    color: #0f172a;
                    font-weight: bold;
                    font-size: 10px;
                }
                QProgressBar::chunk {
                    border-radius: 5px;
                    margin: 1px;
                }
                QPushButton#themeButton {
                    background-color: #e8ecf1;
                    border: 1px solid #cbd5e1;
                    border-radius: 8px;
                    color: #0f172a;
                    font-weight: 600;
                    font-size: 9.5pt;
                    padding: 4px 8px;
                }
                QPushButton#themeButton:hover {
                    background-color: #dfe4ea;
                    border-color: #94a3b8;
                    color: #000000;
                }
                QCalendarWidget QWidget {
                    background-color: #f8fafc;
                    color: #0f172a;
                }
                QCalendarWidget QAbstractItemView:enabled {
                    background-color: #f8fafc;
                    color: #0f172a;
                    selection-background-color: #dbe0e6;
                    selection-color: #0f172a;
                }
                QCalendarWidget QAbstractItemView:disabled {
                    color: #94a3b8;
                }
                QCalendarWidget QSpinBox {
                    background-color: #ffffff;
                    color: #0f172a;
                }
                QMessageBox {
                    background-color: #e8ecf1;
                    border: 1px solid #cbd5e1;
                    border-radius: 12px;
                }
                QMessageBox QLabel {
                    color: #0f172a;
                    font-family: 'IBM Plex Sans Thai', 'Kanit', 'Segoe UI Variable Text', 'Leelawadee UI', 'Segoe UI', -apple-system, sans-serif;
                    font-size: 11pt;
                }
                QMessageBox QPushButton {
                    background-color: #dbe0e6;
                    border: 1px solid #cbd5e1;
                    border-radius: 8px;
                    padding: 6px 16px;
                    color: #0f172a;
                    font-family: 'IBM Plex Sans Thai', 'Kanit', 'Segoe UI Variable Display', 'Leelawadee UI', 'Segoe UI', -apple-system, sans-serif;
                    font-size: 10pt;
                    font-weight: bold;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #cbd5e1;
                    border-color: #94a3b8;
                    color: #0f172a;
                }
                QMessageBox QPushButton:pressed {
                    background-color: #94a3b8;
                }
            """
        else:
            base_style = """
                QMainWindow, QWidget#centralWidget {
                    background-color: #09090b;
                }
                QWidget {
                    color: #e4e4e7;
                    font-family: 'IBM Plex Sans Thai', 'Kanit', 'Segoe UI Variable Display', 'Segoe UI Variable Text', 'Leelawadee UI', 'Prompt', 'Segoe UI', -apple-system, sans-serif;
                    font-size: 11pt;
                }
                QFrame#bentoCard, #bentoCard, #BentoCard {
                    background-color: #18181b;
                    border: 1px solid #27272a;
                    border-radius: 12px;
                }
                QLabel#bentoCardTitle, #bentoCardTitle, #BentoCardTitle {
                    color: #f4f4f5;
                    font-size: 13px;
                    font-weight: 600;
                    letter-spacing: 0.3px;
                    margin-bottom: 2px;
                    background: transparent;
                }
                QLabel {
                    color: #e4e4e7;
                    background-color: transparent;
                }
                QLabel#appTitle {
                    color: #f4f4f5;
                    font-size: 16px;
                    font-weight: bold;
                    background: transparent;
                }
                QLabel#statusLabel {
                    color: #a1a1aa;
                    font-size: 13px;
                    background: transparent;
                }
                QLabel#timeUnitLabel {
                    color: #a1a1aa;
                    font-size: 11px;
                    font-weight: 500;
                    background: transparent;
                }
                QLabel#clockLabel {
                    color: #e4e4e7;
                    font-size: 13px;
                    background: transparent;
                }
                QSpinBox, QComboBox, QDateTimeEdit, QDateEdit {
                    background-color: #27272a;
                    border: 1px solid #3f3f46;
                    color: #f4f4f5;
                    border-radius: 6px;
                    padding: 4px 8px;
                    font-size: 13px;
                    min-width: 60px;
                }
                QSpinBox:hover, QComboBox:hover, QDateTimeEdit:hover, QDateEdit:hover {
                    border-color: #52525b;
                    background-color: #2e2e33;
                }
                QSpinBox:focus, QComboBox:focus, QDateTimeEdit:focus, QDateEdit:focus {
                    border-color: #71717a;
                }
                QComboBox::drop-down, QDateTimeEdit::drop-down, QDateEdit::drop-down {
                    border: none;
                    width: 24px;
                }
                QComboBox::down-arrow, QDateTimeEdit::down-arrow, QDateEdit::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 5px solid #a1a1aa;
                    margin-right: 6px;
                }
                QSpinBox::up-button, QSpinBox::down-button {
                    border: none;
                    width: 18px;
                    background: transparent;
                }
                QSpinBox::up-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-bottom: 5px solid #a1a1aa;
                    width: 0;
                    height: 0;
                }
                QSpinBox::down-arrow {
                    image: none;
                    border-left: 4px solid transparent;
                    border-right: 4px solid transparent;
                    border-top: 5px solid #a1a1aa;
                    width: 0;
                    height: 0;
                }
                QSpinBox::up-arrow:hover {
                    border-bottom-color: #ffffff;
                }
                QSpinBox::down-arrow:hover {
                    border-top-color: #ffffff;
                }
                QComboBox QAbstractItemView {
                    background-color: #18181b;
                    border: 1px solid #3f3f46;
                    border-radius: 8px;
                    padding: 4px;
                    color: #f4f4f5;
                    selection-background-color: #27272a;
                    selection-color: #ffffff;
                    outline: none;
                }
                QComboBox QAbstractItemView QScrollBar:vertical {
                    background: transparent;
                    width: 6px;
                    margin: 2px 0 2px 0;
                }
                QComboBox QAbstractItemView QScrollBar::handle:vertical {
                    background: #3f3f46;
                    border-radius: 3px;
                    min-height: 20px;
                }
                QComboBox QAbstractItemView QScrollBar::add-line:vertical,
                QComboBox QAbstractItemView QScrollBar::sub-line:vertical {
                    height: 0px;
                }
                QPushButton#actionPill {
                    background-color: #27272a;
                    border: 1px solid #3f3f46;
                    border-radius: 8px;
                    padding: 8px 10px;
                    color: #a1a1aa;
                    font-weight: 600;
                    font-size: 11.5px;
                }
                QPushButton#actionPill:hover {
                    background-color: #3f3f46;
                    border-color: #52525b;
                    color: #f4f4f5;
                }
                QPushButton#actionPill:checked {
                    color: #ffffff;
                    font-weight: bold;
                }
                QRadioButton {
                    color: #a1a1aa;
                    spacing: 6px;
                    font-size: 12px;
                    background-color: #27272a;
                    border: 1px solid #3f3f46;
                    border-radius: 8px;
                    padding: 8px 14px;
                    font-weight: 500;
                }
                QRadioButton::indicator {
                    width: 0px;
                    height: 0px;
                }
                QRadioButton:hover {
                    border-color: #52525b;
                    color: #f4f4f5;
                }
                QRadioButton:checked {
                    color: #ffffff;
                    font-weight: bold;
                }
                AnimatedButton#presetCard, QPushButton#presetCard {
                    background-color: #27272a;
                    border: 1px solid #3f3f46;
                    border-radius: 16px;
                    color: #f4f4f5;
                }
                AnimatedButton#presetCard[hovered="true"], QPushButton#presetCard:hover {
                    background-color: #323238;
                    border-color: #52525b;
                }
                AnimatedButton#presetCard[pressed_state="true"], QPushButton#presetCard:pressed {
                    background-color: #1f1f23;
                }
                #presetCard QLabel {
                    background: transparent;
                }
                #presetIcon {
                    font-size: 16px;
                    background: transparent;
                }
                #presetValue {
                    color: #f4f4f5;
                    font-size: 15px;
                    font-weight: bold;
                    background: transparent;
                }
                #presetUnit {
                    color: #a1a1aa;
                    font-size: 9pt;
                    background: transparent;
                }
                AnimatedButton {
                    background-color: #27272a;
                    border: 1px solid #3f3f46;
                    border-radius: 8px;
                    padding: 8px 14px;
                    font-weight: bold;
                    font-size: 13px;
                    color: #e4e4e7;
                }
                AnimatedButton[hovered="true"] {
                    background-color: #3f3f46;
                    border-color: #52525b;
                    color: #ffffff;
                }
                AnimatedButton[pressed_state="true"] {
                    background-color: #1f1f23;
                    padding-top: 10px;
                    padding-bottom: 6px;
                }
                AnimatedButton:disabled {
                    background-color: #1f1f23;
                    color: #52525b;
                    border-color: #27272a;
                }
                QProgressBar {
                    border: 1px solid #3f3f46;
                    border-radius: 7px;
                    text-align: center;
                    background-color: #27272a;
                    color: #f4f4f5;
                    font-weight: bold;
                    font-size: 10px;
                }
                QProgressBar::chunk {
                    border-radius: 5px;
                    margin: 1px;
                }
                QPushButton#themeButton {
                    background-color: #27272a;
                    border: 1px solid #3f3f46;
                    border-radius: 8px;
                    color: #f4f4f5;
                    font-weight: 600;
                    font-size: 9.5pt;
                    padding: 4px 8px;
                }
                QPushButton#themeButton:hover {
                    background-color: #3f3f46;
                    border-color: #52525b;
                    color: #ffffff;
                }
                QCalendarWidget QWidget {
                    background-color: #18181b;
                    color: #f4f4f5;
                }
                QCalendarWidget QAbstractItemView:enabled {
                    background-color: #18181b;
                    color: #f4f4f5;
                    selection-background-color: #27272a;
                    selection-color: #ffffff;
                }
                QCalendarWidget QAbstractItemView:disabled {
                    color: #52525b;
                }
                QCalendarWidget QSpinBox {
                    background-color: #27272a;
                    color: #f4f4f5;
                }
                QMessageBox {
                    background-color: #18181b;
                    border: 1px solid #3f3f46;
                    border-radius: 12px;
                }
                QMessageBox QLabel {
                    color: #f4f4f5;
                    font-family: 'IBM Plex Sans Thai', 'Kanit', 'Segoe UI Variable Text', 'Leelawadee UI', 'Segoe UI', -apple-system, sans-serif;
                    font-size: 11pt;
                }
                QMessageBox QPushButton {
                    background-color: #27272a;
                    border: 1px solid #3f3f46;
                    border-radius: 8px;
                    padding: 6px 16px;
                    color: #f4f4f5;
                    font-family: 'IBM Plex Sans Thai', 'Kanit', 'Segoe UI Variable Display', 'Leelawadee UI', 'Segoe UI', -apple-system, sans-serif;
                    font-size: 10pt;
                    font-weight: bold;
                    min-width: 80px;
                }
                QMessageBox QPushButton:hover {
                    background-color: #3f3f46;
                    border-color: #52525b;
                }
                QMessageBox QPushButton:pressed {
                    background-color: #1f1f23;
                }
            """
        self.setStyleSheet(base_style)
        QApplication.instance().setStyleSheet(base_style)
        self.update_theme_button_ui()

    def hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple string"""
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r}, {g}, {b}"

    def update_theme_colors(self, action_index):
        """Update theme colors based on selected action with smooth visual transitions"""
        self.current_theme = ACTION_COLORS.get(action_index, ACTION_COLORS[0])
        primary = self.current_theme["primary"]
        secondary = self.current_theme["secondary"]
        accent = self.current_theme["accent"]

        if hasattr(self, "action_buttons"):
            for idx, btn in enumerate(self.action_buttons):
                if idx == action_index:
                    btn.setChecked(True)

        if self.current_theme_mode == "light":
            light_bg_ends = {
                0: "#dcd0d2",  # Shutdown - subtle soft red-grey
                1: "#dcd5cc",  # Restart - subtle soft orange-grey
                2: "#cad4df",  # Sleep - subtle soft blue-grey
                3: "#d6cbdc",  # Hibernate - subtle soft purple-grey
            }
            bg_end = light_bg_ends.get(action_index, "#dcd0d2")

            self.countdown_label.setStyleSheet(
                f"background: transparent; color: {primary}; letter-spacing: 2px;"
            )

            dynamic_style = f"""
                QMainWindow {{
                    background: qradialgradient(cx:0.5, cy:0.3, radius:1.0, fx:0.5, fy:0.3,
                        stop:0 #d8dce2,
                        stop:1 {bg_end});
                }}
                QFrame#bentoCard, #bentoCard, #BentoCard {{
                    border-color: rgba({self.hex_to_rgb(primary)}, 0.28);
                }}
                QComboBox::down-arrow, QDateTimeEdit::down-arrow {{
                    border-top-color: {primary};
                }}
                QPushButton#actionPill:checked, QPushButton#actionPillActive {{
                    background-color: {primary};
                    border: 1px solid {primary};
                    color: #ffffff;
                    font-weight: bold;
                }}
                QPushButton#actionPill:checked:hover, QPushButton#actionPillActive:hover {{
                    background-color: {secondary};
                    border-color: {secondary};
                    color: #ffffff;
                }}
                QRadioButton:checked {{
                    background-color: rgba({self.hex_to_rgb(primary)}, 0.15);
                    border: 1.5px solid {primary};
                    color: #0f172a;
                    font-weight: bold;
                }}
                QProgressBar#progressBar::chunk, QProgressBar::chunk {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {primary},
                        stop:1 {secondary});
                }}
            """

            preset_btn_style = f"""
                AnimatedButton#presetCard, QPushButton#presetCard {{
                    background-color: #f1f5f9;
                    border: 1px solid #cbd5e1;
                    border-radius: 16px;
                }}
                AnimatedButton#presetCard[hovered="true"], QPushButton#presetCard:hover {{
                    background-color: rgba({self.hex_to_rgb(primary)}, 0.08);
                    border-color: {primary};
                }}
                AnimatedButton#presetCard[pressed_state="true"], QPushButton#presetCard:pressed {{
                    background-color: rgba({self.hex_to_rgb(primary)}, 0.16);
                }}
                #presetCard QLabel {{
                    background: transparent;
                }}
                #presetIcon {{
                    font-size: 16px;
                    background: transparent;
                }}
                #presetValue {{
                    color: #0f172a;
                    font-size: 15px;
                    font-weight: bold;
                    background: transparent;
                }}
                #presetUnit {{
                    color: #475569;
                    font-size: 9pt;
                    background: transparent;
                }}
            """

            start_btn_style = f"""
                QPushButton#startButton, AnimatedButton#startButton, AnimatedButton {{
                    background-color: {primary};
                    border: 1px solid {primary};
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 14px;
                    color: #ffffff;
                    padding: 10px 16px;
                }}
                QPushButton#startButton:hover, AnimatedButton#startButton[hovered="true"], AnimatedButton[hovered="true"] {{
                    background-color: {secondary};
                    border-color: {secondary};
                    color: #ffffff;
                }}
                QPushButton#startButton:pressed, AnimatedButton#startButton[pressed_state="true"], AnimatedButton[pressed_state="true"] {{
                    background-color: {accent};
                    border-color: {accent};
                    padding-top: 12px;
                    padding-bottom: 8px;
                    color: #ffffff;
                }}
                QPushButton#startButton:disabled, AnimatedButton#startButton:disabled, AnimatedButton:disabled {{
                    background-color: #dbe0e6;
                    color: #94a3b8;
                    border: 1px solid #cbd5e1;
                }}
            """

            cancel_btn_style = f"""
                QPushButton#cancelButton, AnimatedButton#cancelButton, AnimatedButton {{
                    background-color: rgba(220, 38, 38, 0.08);
                    border: 1px solid rgba(220, 38, 38, 0.25);
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 13px;
                    color: #dc2626;
                    padding: 8px 14px;
                }}
                QPushButton#cancelButton:hover, AnimatedButton#cancelButton[hovered="true"], AnimatedButton[hovered="true"] {{
                    background-color: rgba(220, 38, 38, 0.16);
                    border-color: rgba(220, 38, 38, 0.45);
                    color: #b91c1c;
                }}
                QPushButton#cancelButton:pressed, AnimatedButton#cancelButton[pressed_state="true"], AnimatedButton[pressed_state="true"] {{
                    background-color: rgba(220, 38, 38, 0.04);
                    padding-top: 10px;
                    padding-bottom: 6px;
                }}
                QPushButton#cancelButton:disabled, AnimatedButton#cancelButton:disabled, AnimatedButton:disabled {{
                    background-color: #e8ecf1;
                    color: #94a3b8;
                    border: 1px solid #cbd5e1;
                }}
            """

            clear_btn_style = f"""
                QPushButton#clearButton, AnimatedButton#clearButton, AnimatedButton {{
                    background-color: #dbe0e6;
                    border: 1px solid #cbd5e1;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 13px;
                    color: #334155;
                    padding: 8px 14px;
                }}
                QPushButton#clearButton:hover, AnimatedButton#clearButton[hovered="true"], AnimatedButton[hovered="true"] {{
                    background-color: #cbd5e1;
                    border-color: #94a3b8;
                    color: #0f172a;
                }}
                QPushButton#clearButton:pressed, AnimatedButton#clearButton[pressed_state="true"], AnimatedButton[pressed_state="true"] {{
                    background-color: #94a3b8;
                    padding-top: 10px;
                    padding-bottom: 6px;
                }}
            """
        else:
            bg_end = self.current_theme["bg_gradient_end"]

            self.countdown_label.setStyleSheet(
                f"background: transparent; color: {primary}; letter-spacing: 2px;"
            )

            dynamic_style = f"""
                QMainWindow {{
                    background: qradialgradient(cx:0.5, cy:0.3, radius:1.0, fx:0.5, fy:0.3,
                        stop:0 #09090b,
                        stop:1 {bg_end});
                }}
                QFrame#bentoCard, #bentoCard, #BentoCard {{
                    border-color: rgba({self.hex_to_rgb(primary)}, 0.25);
                }}
                QComboBox::down-arrow, QDateTimeEdit::down-arrow {{
                    border-top-color: {primary};
                }}
                QPushButton#actionPill:checked, QPushButton#actionPillActive {{
                    background-color: {primary};
                    border: 1px solid {primary};
                    color: #ffffff;
                    font-weight: bold;
                }}
                QPushButton#actionPill:checked:hover, QPushButton#actionPillActive:hover {{
                    background-color: {secondary};
                    border-color: {secondary};
                    color: #ffffff;
                }}
                QRadioButton:checked {{
                    background-color: rgba({self.hex_to_rgb(primary)}, 0.2);
                    border: 1.5px solid {primary};
                    color: #ffffff;
                    font-weight: bold;
                }}
                QProgressBar#progressBar::chunk, QProgressBar::chunk {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {primary},
                        stop:1 {secondary});
                }}
            """

            preset_btn_style = f"""
                AnimatedButton#presetCard, QPushButton#presetCard {{
                    background-color: #27272a;
                    border: 1px solid #3f3f46;
                    border-radius: 16px;
                }}
                AnimatedButton#presetCard[hovered="true"], QPushButton#presetCard:hover {{
                    background-color: #323238;
                    border-color: {primary};
                }}
                AnimatedButton#presetCard[pressed_state="true"], QPushButton#presetCard:pressed {{
                    background-color: #1f1f23;
                }}
                #presetCard QLabel {{
                    background: transparent;
                }}
                #presetIcon {{
                    font-size: 16px;
                    background: transparent;
                }}
                #presetValue {{
                    color: #f4f4f5;
                    font-size: 15px;
                    font-weight: bold;
                    background: transparent;
                }}
                #presetUnit {{
                    color: #a1a1aa;
                    font-size: 9pt;
                    background: transparent;
                }}
            """

            start_btn_style = f"""
                QPushButton#startButton, AnimatedButton#startButton, AnimatedButton {{
                    background-color: {primary};
                    border: 1px solid {primary};
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 14px;
                    color: #ffffff;
                    padding: 10px 16px;
                }}
                QPushButton#startButton:hover, AnimatedButton#startButton[hovered="true"], AnimatedButton[hovered="true"] {{
                    background-color: {secondary};
                    border-color: {secondary};
                    color: #ffffff;
                }}
                QPushButton#startButton:pressed, AnimatedButton#startButton[pressed_state="true"], AnimatedButton[pressed_state="true"] {{
                    background-color: {accent};
                    border-color: {accent};
                    padding-top: 12px;
                    padding-bottom: 8px;
                    color: #ffffff;
                }}
                QPushButton#startButton:disabled, AnimatedButton#startButton:disabled, AnimatedButton:disabled {{
                    background-color: #27272a;
                    color: #52525b;
                    border: 1px solid #3f3f46;
                }}
            """

            cancel_btn_style = f"""
                QPushButton#cancelButton, AnimatedButton#cancelButton, AnimatedButton {{
                    background-color: rgba(239, 68, 68, 0.12);
                    border: 1px solid rgba(239, 68, 68, 0.35);
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 13px;
                    color: #f87171;
                    padding: 8px 14px;
                }}
                QPushButton#cancelButton:hover, AnimatedButton#cancelButton[hovered="true"], AnimatedButton[hovered="true"] {{
                    background-color: rgba(239, 68, 68, 0.22);
                    border-color: rgba(239, 68, 68, 0.55);
                    color: #fca5a5;
                }}
                QPushButton#cancelButton:pressed, AnimatedButton#cancelButton[pressed_state="true"], AnimatedButton[pressed_state="true"] {{
                    background-color: rgba(239, 68, 68, 0.08);
                    padding-top: 10px;
                    padding-bottom: 6px;
                }}
                QPushButton#cancelButton:disabled, AnimatedButton#cancelButton:disabled, AnimatedButton:disabled {{
                    background-color: #1f1f23;
                    color: #52525b;
                    border: 1px solid #27272a;
                }}
            """

            clear_btn_style = f"""
                QPushButton#clearButton, AnimatedButton#clearButton, AnimatedButton {{
                    background-color: #27272a;
                    border: 1px solid #3f3f46;
                    border-radius: 8px;
                    font-weight: bold;
                    font-size: 13px;
                    color: #e4e4e7;
                    padding: 8px 14px;
                }}
                QPushButton#clearButton:hover, AnimatedButton#clearButton[hovered="true"], AnimatedButton[hovered="true"] {{
                    background-color: #3f3f46;
                    border-color: #52525b;
                    color: #ffffff;
                }}
                QPushButton#clearButton:pressed, AnimatedButton#clearButton[pressed_state="true"], AnimatedButton[pressed_state="true"] {{
                    background-color: #222226;
                    padding-top: 10px;
                    padding-bottom: 6px;
                }}
            """

        current_style = self.styleSheet()
        if "/* DYNAMIC */" in current_style:
            base = current_style.split("/* DYNAMIC */")[0]
        else:
            base = current_style

        self.setStyleSheet(base + "/* DYNAMIC */" + dynamic_style)

        for btn in self.preset_buttons:
            btn.setStyleSheet(preset_btn_style)

        self.start_button.setStyleSheet(start_btn_style)
        self.cancel_button.setStyleSheet(cancel_btn_style)
        self.clear_button.setStyleSheet(clear_btn_style)

    def on_action_changed(self, index):
        """Handle action change, synchronize action button pills and update theme colors"""
        if hasattr(self, "action_buttons") and 0 <= index < len(self.action_buttons):
            self.action_buttons[index].setChecked(True)
        self.update_theme_colors(index)

    @property
    def target_clock_datetime(self) -> QDateTime:
        """Return QDateTime representing current selection in Clock mode"""
        if hasattr(self, "date_picker") and hasattr(self, "time_hours_combo") and hasattr(self, "time_minutes_combo"):
            d = self.date_picker.date()
            h = self.time_hours_combo.currentIndex()
            m = self.time_minutes_combo.currentIndex()
            return QDateTime(d, QTime(h, m, 0))
        return QDateTime.currentDateTime().addSecs(3600)

    def reset_clock_to_default(self):
        """Reset clock date and time dropdowns to current time + 1 hour"""
        if hasattr(self, "date_picker") and hasattr(self, "time_hours_combo") and hasattr(self, "time_minutes_combo"):
            init_dt = QDateTime.currentDateTime().addSecs(3600)
            self.date_picker.setDate(init_dt.date())
            self.time_hours_combo.setCurrentIndex(init_dt.time().hour())
            self.time_minutes_combo.setCurrentIndex(init_dt.time().minute())

    def on_mode_toggled(self, id, checked):
        """Switch time input widget based on selected mode with smooth slide transition"""
        if not checked or not hasattr(self, "time_stack"):
            return
        if id == 1:  # Clock mode
            if self.target_clock_datetime.toPython() <= datetime.now():
                self.reset_clock_to_default()
        self.time_stack.slide_to_index(id)

    def toggle_theme(self):
        """Switch between light and dark themes"""
        if self.current_theme_mode == "dark":
            self.current_theme_mode = "light"
        else:
            self.current_theme_mode = "dark"
            
        logger.info(f"🌓 Theme toggled to {self.current_theme_mode}")
        self.apply_styles()
        self.update_theme_colors(self.action_combo.currentIndex())
        self.save_window_settings()

    def update_theme_button_ui(self):
        """Update theme button label based on current theme"""
        if self.current_theme_mode == "light":
            self.theme_button.setText("🌙 Dark (โหมดมืด)")
        else:
            self.theme_button.setText("☀️ Light (โหมดสว่าง)")

    def start_preset_timer(self, value, unit):
        """Start timer from preset card"""
        if self.is_timer_active:
            self.show_toast("A timer is already active. Please cancel first. (มีการตั้งเวลาอยู่แล้ว กรุณายกเลิกก่อน)", "warning")
            return

        # Get selected action
        action_index = self.action_combo.currentIndex()
        if action_index >= 2:  # Sleep or Hibernate
            self.show_toast("Quick Presets only support Shutdown & Restart (Quick Presets รองรับเฉพาะ Shutdown และ Restart)", "warning")
            self.action_combo.setCurrentIndex(0)
            return

        is_restart = action_index == 1
        action_en = "Restart" if is_restart else "Shutdown"
        action_th = "รีสตาร์ท" if is_restart else "ปิดเครื่อง"
        action_combined = f"{action_en} ({action_th})"

        # Calculate time
        if unit == "minutes":
            self.target_shutdown_time = datetime.now() + timedelta(minutes=value)
            time_str_en = f"{value} mins"
            time_str_th = f"{value} นาที"
            self.radio_timer.setChecked(True)
            self.hours_combo.setCurrentIndex(0)
            self.minutes_combo.setCurrentIndex(min(value, 59))
            self.seconds_combo.setCurrentIndex(0)
        else:  # hours
            self.target_shutdown_time = datetime.now() + timedelta(hours=value)
            unit_en_str = "hour" if value == 1 else "hours"
            time_str_en = f"{value} {unit_en_str}"
            time_str_th = f"{value} ชั่วโมง"
            self.radio_timer.setChecked(True)
            self.hours_combo.setCurrentIndex(min(value, 24))
            self.minutes_combo.setCurrentIndex(0)
            self.seconds_combo.setCurrentIndex(0)

        time_combined = f"{time_str_en} ({time_str_th})"

        reply = QMessageBox.question(
            self,
            "Confirm Schedule (ยืนยันการตั้งเวลา)",
            f"Do you want to schedule {action_en} in {time_str_en}?\n"
            f"(ต้องการตั้งเวลา{action_th}ในอีก {time_str_th} หรือไม่?)\n\n"
            f"Please save your work before proceeding!\n"
            f"(โปรดบันทึกงานของคุณก่อนดำเนินการครับ!)",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.No:
            return

        try:
            total_seconds = int(
                (self.target_shutdown_time - datetime.now()).total_seconds()
            )
            self.total_seconds = total_seconds
            self.remaining_seconds = total_seconds

            # Cancel any existing shutdown schedule first (prevent conflicts)
            try:
                subprocess.run(
                    ["shutdown", "/a"], capture_output=True
                )
            except Exception:
                pass  # No existing shutdown to cancel, which is fine

            command = "/r" if is_restart else "/s"
            logger.info(f"⚡ [Preset] {action_en} in {time_combined} ({total_seconds}s) → ⏰ {self.target_shutdown_time.strftime('%H:%M:%S')}")
            subprocess.run(["shutdown", command, "/t", str(total_seconds)], check=True)

            self.is_timer_active = True
            self.status_label.setText(
                f"Status: {action_en} at {self.target_shutdown_time.strftime('%H:%M:%S')} (สถานะ: จะ{action_th}เวลา {self.target_shutdown_time.strftime('%H:%M:%S')})"
            )
            self.cancel_button.setEnabled(True)
            self.start_button.setEnabled(False)
            self.countdown_timer.start(1000)

            self.show_toast(f"Scheduled {action_combined}: {time_combined}", "success")
            self.save_settings()

        except Exception as e:
            self.show_toast(f"Cannot schedule (ไม่สามารถตั้งเวลาได้): {e}", "error")

    def start_timer(self):
        """Start shutdown/restart timer"""
        if self.is_timer_active:
            self.show_toast("A timer is already active. Please cancel first. (มีการตั้งเวลาอยู่แล้ว กรุณายกเลิกก่อน)", "warning")
            return

        action_index = self.action_combo.currentIndex()
        action_map = {
            0: ("Shutdown", "ปิดเครื่อง", "/s"),
            1: ("Restart", "รีสตาร์ท", "/r"),
            2: ("Sleep", "พักเครื่อง", "sleep"),
            3: ("Hibernate", "จำศีล", "hibernate"),
        }
        action_en, action_th, command_type = action_map.get(action_index, ("Shutdown", "ปิดเครื่อง", "/s"))
        action_combined = f"{action_en} ({action_th})"

        # Sleep/Hibernate execute immediately
        if action_index >= 2:
            self._execute_sleep_hibernate(action_en, action_th, command_type)
            return

        reply = QMessageBox.question(
            self,
            "Confirm Schedule (ยืนยันการตั้งเวลา)",
            f"Do you want to schedule {action_en}?\n"
            f"(คุณต้องการตั้งเวลา{action_th}หรือไม่?)\n\n"
            f"Please save your work before proceeding!\n"
            f"(โปรดบันทึกงานของคุณก่อนดำเนินการครับ!)",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.No:
            return

        try:
            mode_index = self.mode_button_group.checkedId()
            if mode_index == 0:  # Timer mode (Dropdowns)
                hours = self.hours_combo.currentIndex()
                minutes = self.minutes_combo.currentIndex()
                seconds = self.seconds_combo.currentIndex()
                if hours == 0 and minutes == 0 and seconds == 0:
                    self.show_toast("Please specify a duration greater than 0 (กรุณาระบุระยะเวลานับถอยหลังมากกว่า 0)", "warning")
                    return
                self.target_shutdown_time = datetime.now() + timedelta(
                    hours=hours, minutes=minutes, seconds=seconds
                )
            else:  # Clock mode (Date picker + Hour/Minute dropdowns)
                target_dt = self.target_clock_datetime
                self.target_shutdown_time = target_dt.toPython()

            if self.target_shutdown_time <= datetime.now():
                self.show_toast("Please select a future time (กรุณาตั้งเวลาในอนาคต)", "warning")
                return

            # Validate max duration (72 hours for safety)
            max_duration = timedelta(hours=72)
            if self.target_shutdown_time - datetime.now() > max_duration:
                self.show_toast("Please set time within 72 hours (กรุณาตั้งเวลาไม่เกิน 72 ชั่วโมง)", "warning")
                return

            total_seconds = int(
                (self.target_shutdown_time - datetime.now()).total_seconds()
            )
            self.total_seconds = total_seconds
            self.remaining_seconds = total_seconds

            # First, cancel any existing shutdown
            try:
                subprocess.run(
                    ["shutdown", "/a"], capture_output=True
                )
            except Exception:
                pass  # No existing shutdown to cancel, which is fine

            # Now schedule the new shutdown
            logger.info(f"⏱️  [Timer] {action_en} in {total_seconds}s → ⏰ {self.target_shutdown_time.strftime('%H:%M:%S')}")
            subprocess.run(
                ["shutdown", command_type, "/t", str(total_seconds)], check=True
            )

            self.is_timer_active = True
            self.status_label.setText(
                f"Status: {action_en} at {self.target_shutdown_time.strftime('%H:%M:%S')} (สถานะ: จะ{action_th}เวลา {self.target_shutdown_time.strftime('%H:%M:%S')})"
            )
            self.cancel_button.setEnabled(True)
            self.start_button.setEnabled(False)
            self.countdown_timer.start(1000)

            self.show_toast(f"Scheduled {action_combined} successfully (ตั้งเวลา{action_th}สำเร็จ)", "success")
            self.save_settings()

        except subprocess.CalledProcessError as e:
            error_msg = f"Cannot schedule (ไม่สามารถตั้งเวลาได้): Code {e.returncode}"
            if e.returncode == 1190:
                error_msg = "A shutdown is already scheduled. Please cancel it first. (มีการตั้งเวลาปิดเครื่องอยู่แล้ว กรุณากดยกเลิก)"
            elif e.returncode == 5:
                error_msg = "Administrator privileges required (ต้องมีสิทธิ์ Administrator เพื่อใช้งานฟีเจอร์นี้)"
            logger.error(f"❌ Shutdown command failed (code {e.returncode}): {e}")
            self.show_toast(error_msg, "error")
        except Exception as e:
            logger.error(f"💥 Unexpected error during timer: {e}")
            self.show_toast(f"Cannot schedule (ไม่สามารถตั้งเวลาได้): {e}", "error")

    def _execute_sleep_hibernate(self, action_en, action_th, command_type):
        """Execute Sleep or Hibernate immediately"""
        reply = QMessageBox.question(
            self,
            f"Confirm {action_en} (ยืนยันการ{action_th})",
            f"Do you want to execute {action_en} immediately?\n"
            f"(ต้องการ{action_th}ทันทีหรือไม่?)\n\n"
            f"Please save your work before proceeding!\n"
            f"(โปรดบันทึกงานของคุณก่อนดำเนินการครับ!)",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.No:
            return

        try:
            logger.info(f"😴 Executing {action_en} immediately...")
            if command_type == "sleep":
                subprocess.run(
                    ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
                    check=True,
                )
            else:  # hibernate
                subprocess.run(
                    ["rundll32.exe", "powrprof.dll,SetSuspendState", "1,1,0"],
                    check=True,
                )

            self.status_label.setText(f"Status: Executing {action_en}... (สถานะ: กำลัง{action_th}...)")
            self.show_toast(f"Executing {action_en}... (กำลัง{action_th}...)", "info")
        except Exception as e:
            self.show_toast(f"Cannot execute {action_en} (ไม่สามารถ{action_th}ได้): {e}", "error")

    def cancel_timer(self, confirm=True):
        """Cancel active timer"""
        if not self.is_timer_active:
            if confirm:
                self.show_toast("No active timer (ไม่มีการตั้งเวลาอยู่ในขณะนี้)", "info")
            return

        if confirm:
            reply = QMessageBox.question(
                self,
                "Confirm Cancel (ยืนยันการยกเลิก)",
                "Are you sure you want to cancel the timer?\n(ต้องการยกเลิกการตั้งเวลาหรือไม่?)",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return

        try:
            logger.info("🛑 Cancelling scheduled shutdown...")
            subprocess.run(["shutdown", "/a"], check=True)
            self.countdown_timer.stop()  # Stop the GUI countdown timer too
            self.reset_ui_state()
            self.is_timer_active = False
            self.status_label.setText("Status: Cancelled (สถานะ: ยกเลิกการตั้งเวลาแล้ว)")
            logger.info("✅ Timer cancelled successfully")
            if confirm:
                self.show_toast("Timer cancelled successfully (ยกเลิกการตั้งเวลาสำเร็จ)", "success")
            self.save_settings()
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to cancel shutdown: {e}")
            if confirm:
                if e.returncode == 1116:  # ERROR_NO_SHUTDOWN_IN_PROGRESS
                    self.show_toast("No scheduled shutdown to cancel (ไม่มีการตั้งเวลาให้ยกเลิก)", "info")
                else:
                    self.show_toast(f"Cannot cancel (ไม่สามารถยกเลิกได้): Code {e.returncode}", "error")
            self.reset_ui_state()
        except Exception as e:
            logger.error(f"💥 Unexpected error during cancel: {e}")
            if confirm:
                self.show_toast(f"Cannot cancel (ไม่สามารถยกเลิกได้): {e}", "error")
            self.reset_ui_state()

    def update_countdown(self):
        """Update countdown display every second"""
        if not self.is_timer_active or not self.target_shutdown_time:
            return

        now = datetime.now()
        remaining = self.target_shutdown_time - now

        if remaining.total_seconds() <= 0:
            self.countdown_label.setText("00:00:00")
            self.progress_bar.setValue(100)
            is_restart = self.action_combo.currentIndex() == 1
            action_en = "Restart" if is_restart else "Shutdown"
            action_th = "รีสตาร์ท" if is_restart else "ปิดเครื่อง"
            self.status_label.setText(f"Status: Executing {action_en}... (สถานะ: กำลัง{action_th}...)")
            self._delete_config_file()
            self.reset_ui_state()
        else:
            total_seconds = int(remaining.total_seconds())
            self.remaining_seconds = max(0, total_seconds)
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.countdown_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

            # Update progress bar with remaining time
            if self.total_seconds > 0:
                progress = int(
                    (self.total_seconds - self.remaining_seconds)
                    / self.total_seconds
                    * 100
                )
                mins, secs = divmod(self.remaining_seconds, 60)
                self.progress_bar.setFormat(f"{progress}% - Remaining (เหลือ) {mins:02d}:{secs:02d}")
                self.progress_bar.setValue(min(100, progress))

    def show_toast(self, message, type_="info"):
        """Show toast notification"""
        if self.current_toast is not None:
            try:
                self.current_toast.deleteLater()
            except Exception:
                pass
        toast = Toast(self, message, duration=3000, type_=type_)
        toast.show()
        self.current_toast = toast

    def clear_fields(self):
        """Clear all fields and delete config"""
        self.reset_clock_to_default()
        self.hours_combo.setCurrentIndex(0)
        self.minutes_combo.setCurrentIndex(30)
        self.seconds_combo.setCurrentIndex(0)
        self.radio_timer.setChecked(True)
        self.action_combo.setCurrentIndex(0)
        self.status_label.setText("Status: Ready / Idle (สถานะ: ยังไม่ได้เริ่มนับถอยหลัง)")
        self.countdown_label.setText("00:00:00")
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self._delete_config_file()
        logger.info("🧹 All fields cleared, config deleted")
        self.show_toast("All fields reset (ล้างค่าเรียบร้อย)", "info")

    def reset_ui_state(self):
        """Reset UI state after timer completes"""
        self.is_timer_active = False
        self.countdown_timer.stop()
        self.target_shutdown_time = None
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.cancel_button.setEnabled(False)
        self.start_button.setEnabled(True)
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")
        self.status_label.setText("Status: Ready / Idle (สถานะ: ยังไม่ได้เริ่มนับถอยหลัง)")
        self.countdown_label.setText("00:00:00")

    def closeEvent(self, event):
        """Called when closing the application"""
        logger.info("👋 Application closing... Bye!")
        self.countdown_timer.stop()
        self.save_window_settings()
        self._delete_config_file()
        super().closeEvent(event)

    def _delete_config_file(self):
        """Safely delete config file"""
        try:
            if os.path.exists(CONFIG_FILE):
                os.remove(CONFIG_FILE)
        except Exception as e:
            logger.warning(f"⚠️  Could not delete config file: {e}")

    def save_settings(self):
        """Save settings to JSON file with atomic write"""
        settings = {
            "action": self.action_combo.currentIndex(),
            "mode": self.mode_button_group.checkedId(),
            "datetime": self.target_clock_datetime.toString(Qt.ISODate),
            "timer_hours": self.hours_combo.currentIndex(),
            "timer_minutes": self.minutes_combo.currentIndex(),
            "timer_seconds": self.seconds_combo.currentIndex(),
            # Legacy compatibility
            "spin_hours": self.hours_combo.currentIndex(),
            "spin_minutes": self.minutes_combo.currentIndex(),
            "spin_seconds": self.seconds_combo.currentIndex(),
            "date": self.date_picker.date().toString(Qt.ISODate),
            "time": f"{self.time_hours_combo.currentText()}:{self.time_minutes_combo.currentText()}",
            "hours": self.hours_combo.currentIndex(),
            "minutes": self.minutes_combo.currentIndex(),
            "seconds": self.seconds_combo.currentIndex(),
        }
        try:
            temp_path = CONFIG_FILE + ".tmp"
            try:
                with open(temp_path, 'w', encoding='utf-8') as f:
                    json.dump(settings, f, indent=4)
                os.replace(temp_path, CONFIG_FILE)
            except Exception:
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass
                raise
        except Exception as e:
            logger.error(f"💾❌ Could not save settings: {e}")

    def load_settings(self):
        """Load settings from JSON file"""
        if not os.path.exists(CONFIG_FILE):
            self.radio_timer.setChecked(True)
            return

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)

            self.action_combo.setCurrentIndex(settings.get("action", 0))

            mode_id = settings.get("mode", 0)
            radio_to_check = self.mode_button_group.button(mode_id)
            if radio_to_check:
                radio_to_check.setChecked(True)
            else:
                self.radio_timer.setChecked(True)

            if "datetime" in settings:
                dt = QDateTime.fromString(settings["datetime"], Qt.ISODate)
                if dt.isValid():
                    self.date_picker.setDate(dt.date())
                    self.time_hours_combo.setCurrentIndex(max(0, min(dt.time().hour(), 23)))
                    self.time_minutes_combo.setCurrentIndex(max(0, min(dt.time().minute(), 59)))
            elif "date" in settings:
                d = QDate.fromString(settings.get("date", ""), Qt.ISODate)
                t_str = settings.get("time", "00:00")
                t_parts = t_str.split(":")
                if d.isValid():
                    self.date_picker.setDate(d)
                if len(t_parts) == 2:
                    h = max(0, min(int(t_parts[0]), 23))
                    m = max(0, min(int(t_parts[1]), 59))
                    self.time_hours_combo.setCurrentIndex(h)
                    self.time_minutes_combo.setCurrentIndex(m)

            h = settings.get("timer_hours", settings.get("spin_hours", settings.get("hours", 0)))
            m = settings.get("timer_minutes", settings.get("spin_minutes", settings.get("minutes", 30)))
            s = settings.get("timer_seconds", settings.get("spin_seconds", settings.get("seconds", 0)))
            self.hours_combo.setCurrentIndex(max(0, min(int(h), 24)))
            self.minutes_combo.setCurrentIndex(max(0, min(int(m), 59)))
            self.seconds_combo.setCurrentIndex(max(0, min(int(s), 59)))

        except Exception as e:
            logger.error(f"📂❌ Could not load settings: {e}")

    def save_window_settings(self):
        """Save window size and position to JSON file"""
        settings = {
            "width": self.width(),
            "height": self.height(),
            "x": self.x(),
            "y": self.y(),
            "theme": self.current_theme_mode,
        }
        try:
            temp_path = WINDOW_CONFIG_FILE + ".tmp"
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
            os.replace(temp_path, WINDOW_CONFIG_FILE)
            logger.info("💾 Window size and position saved")
        except Exception as e:
            logger.error(f"💾❌ Could not save window settings: {e}")

    def load_window_settings(self):
        """Load window size and position from JSON file"""
        if not os.path.exists(WINDOW_CONFIG_FILE):
            return
        try:
            with open(WINDOW_CONFIG_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)
            
            width = settings.get("width", 580)
            height = settings.get("height", 720)
            self.resize(width, height)
            
            x = settings.get("x")
            y = settings.get("y")
            if x is not None and y is not None:
                self.move(x, y)
                logger.info(f"📂 Window size ({width}x{height}) and position ({x}, {y}) restored")
            
            self.current_theme_mode = settings.get("theme", "dark")
            logger.info(f"📂 Theme mode '{self.current_theme_mode}' loaded")
        except Exception as e:
            logger.error(f"📂❌ Could not load window settings: {e}")


if __name__ == "__main__":
    import signal
    
    app = QApplication(sys.argv)

    # Set locale for consistent number display
    QLocale.setDefault(QLocale.C)

    # Handle keyboard interrupt (Ctrl+C) gracefully
    def handle_signal(sig, frame):
        if 'window' in globals() and window.is_timer_active:
            window.cancel_timer(confirm=False)
        app.quit()
    
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGBREAK, handle_signal)  # Windows Ctrl+Break

    if sys.platform == "win32":
        import ctypes

        myappid = "mycompany.myproduct.subproduct.version"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    window = ShutdownTimerApp()
    window.show()
    sys.exit(app.exec())
