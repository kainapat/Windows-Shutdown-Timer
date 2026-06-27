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
)
from PySide6.QtGui import (
    QFont,
    QColor,
    QFontDatabase,
)

CONFIG_FILE = "timer_config.json"
WINDOW_CONFIG_FILE = "window_config.json"

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
        "primary": "#ff5277",
        "secondary": "#ff94ab",
        "accent": "#ff2a54",
        "bg_gradient_end": "#18060a",
        "progress": "#ff5277",
        "icon": "🔌",
    },
    1: {  # Restart - Orange Accent
        "name": "restart",
        "primary": "#ff9130",
        "secondary": "#ffc28d",
        "accent": "#e07310",
        "bg_gradient_end": "#180c05",
        "progress": "#ff9130",
        "icon": "🔄",
    },
    2: {  # Sleep - Blue Accent
        "name": "sleep",
        "primary": "#3a86ff",
        "secondary": "#8eb7ff",
        "accent": "#1d63d8",
        "bg_gradient_end": "#050c18",
        "progress": "#3a86ff",
        "icon": "😴",
    },
    3: {  # Hibernate - Purple Accent
        "name": "hibernate",
        "primary": "#a855f7",
        "secondary": "#d8b4fe",
        "accent": "#7e22ce",
        "bg_gradient_end": "#0e0518",
        "progress": "#a855f7",
        "icon": "🌙",
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
    {"value": 15, "unit": "minutes", "icon": "⚡", "label": "15", "sublabel": "นาที"},
    {"value": 30, "unit": "minutes", "icon": "⚡", "label": "30", "sublabel": "นาที"},
    {"value": 1, "unit": "hours", "icon": "⏰", "label": "1", "sublabel": "ชม."},
    {"value": 2, "unit": "hours", "icon": "⏰", "label": "2", "sublabel": "ชม."},
]


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
        self.setFixedSize(100, 95)

        layout = QVBoxLayout(self)
        layout.setSpacing(2)
        layout.setContentsMargins(6, 6, 6, 6)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 18px; background: transparent;")

        value_label = QLabel(label)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setFont(QFont("Segoe UI", 16, QFont.Bold))
        value_label.setObjectName("presetValue")
        value_label.setStyleSheet("background: transparent;")

        unit_label = QLabel(sublabel)
        unit_label.setAlignment(Qt.AlignCenter)
        unit_label.setFont(QFont("Segoe UI", 9))
        unit_label.setObjectName("presetUnit")
        unit_label.setStyleSheet("background: transparent;")

        layout.addWidget(icon_label)
        layout.addWidget(value_label)
        layout.addWidget(unit_label)


class BentoCard(QFrame):
    """Machined glass-like enclosure representing Bento grid sections"""

    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("BentoCard")
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(16, 16, 16, 16)
        self.layout.setSpacing(10)

        if title:
            self.title_label = QLabel(title)
            self.title_label.setFont(QFont("Segoe UI", 9, QFont.Bold))
            self.title_label.setObjectName("BentoCardTitle")
            self.layout.addWidget(self.title_label)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(18)
        shadow.setColor(QColor(0, 0, 0, 45))
        shadow.setOffset(0, 6)
        self.setGraphicsEffect(shadow)


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


class Toast(QWidget):
    """Modern toast notification with cinematic entry & exit animation"""

    def __init__(self, parent, message, duration=3000, type_="info"):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        configs = {
            "info":    {"bg": "rgba(30, 102, 245, 0.88)", "fg": "#ffffff", "icon": "ℹ️"},
            "success": {"bg": "rgba(64, 160, 43, 0.88)", "fg": "#ffffff", "icon": "✅"},
            "warning": {"bg": "rgba(223, 142, 29, 0.88)", "fg": "#ffffff", "icon": "⚠️"},
            "error":   {"bg": "rgba(210, 15, 57, 0.88)", "fg": "#ffffff", "icon": "❌"},
        }
        cfg = configs.get(type_, configs["info"])

        self.setStyleSheet(f"""
            QWidget#toastBody {{
                background-color: {cfg['bg']};
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 12px;
            }}
            QLabel {{
                background: transparent;
                color: {cfg['fg']};
                font-size: 13px;
                font-weight: bold;
                font-family: 'Segoe UI', sans-serif;
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
        self.setMinimumSize(650, 580)
        self.resize(650, 580)

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
        self.apply_styles()
        self.update_theme_colors(0)
        logger.info("🚀 Application started with Bento Grid design")

    def init_ui(self):
        """Create and arrange widgets inside Bento Grid architecture"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(18, 18, 18, 18)

        # --- Header Layout ---
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(4, 0, 4, 4)

        self.title_label = QLabel("Windows Shutdown Timer")
        title_font = QFont("Segoe UI", 16, QFont.Bold)
        self.title_label.setFont(title_font)
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        self.theme_button = QPushButton()
        self.theme_button.setObjectName("themeButton")
        self.theme_button.setCursor(Qt.PointingHandCursor)
        self.theme_button.setFixedWidth(100)
        self.theme_button.setMinimumHeight(32)
        self.theme_button.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_button)

        main_layout.addLayout(header_layout)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(14)
        grid_layout.setColumnStretch(0, 1)
        grid_layout.setColumnStretch(1, 1)

        # --- Card A: Action & Mode Selector ---
        self.card_action_mode = BentoCard("การตั้งค่าและการกระทำ", self)
        card_a_layout = self.card_action_mode.layout

        action_layout = QHBoxLayout()
        self.action_combo = QComboBox()
        self.action_combo.addItem(f"{ACTION_COLORS[0]['icon']} ปิดเครื่อง")
        self.action_combo.addItem(f"{ACTION_COLORS[1]['icon']} รีสตาร์ท")
        self.action_combo.addItem(f"{ACTION_COLORS[2]['icon']} พักเครื่อง")
        self.action_combo.addItem(f"{ACTION_COLORS[3]['icon']} จำศีล")
        self.action_combo.setMinimumHeight(38)
        self.action_combo.currentIndexChanged.connect(self.update_theme_colors)

        action_layout.addWidget(QLabel("การกระทำ:"))
        action_layout.addWidget(self.action_combo, 1)
        card_a_layout.addLayout(action_layout)

        # Mode selector pills in 2x2 grid
        mode_pills_layout = QGridLayout()
        mode_pills_layout.setSpacing(6)

        self.mode_button_group = QButtonGroup(self)
        self.radio_datetime = QRadioButton(f"{ICONS['calendar']} วัน/เวลา")
        self.radio_hours = QRadioButton("⏱ ชั่วโมง")
        self.radio_minutes = QRadioButton("⏱ นาที")
        self.radio_seconds = QRadioButton("⏱ วินาที")

        self.mode_button_group.addButton(self.radio_datetime, 0)
        self.mode_button_group.addButton(self.radio_hours, 1)
        self.mode_button_group.addButton(self.radio_minutes, 2)
        self.mode_button_group.addButton(self.radio_seconds, 3)

        self.mode_button_group.idToggled.connect(self.on_mode_toggled)

        mode_pills_layout.addWidget(self.radio_datetime, 0, 0)
        mode_pills_layout.addWidget(self.radio_hours, 0, 1)
        mode_pills_layout.addWidget(self.radio_minutes, 1, 0)
        mode_pills_layout.addWidget(self.radio_seconds, 1, 1)

        card_a_layout.addLayout(mode_pills_layout)
        grid_layout.addWidget(self.card_action_mode, 0, 0)

        # --- Card B: Time Input ---
        self.card_time_input = BentoCard("ระบุเวลาทำงาน", self)
        card_b_layout = self.card_time_input.layout
        card_b_layout.setAlignment(Qt.AlignCenter)

        self.time_stack = SlidingStackedWidget()

        # Datetime page
        self.datetime_page = QWidget()
        datetime_layout = QHBoxLayout(self.datetime_page)
        datetime_layout.setContentsMargins(0, 0, 0, 0)
        datetime_layout.setSpacing(8)

        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self.date_edit.setDisplayFormat("ddd d MMM yyyy")
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumWidth(125)

        self.time_hours_combo = QComboBox()
        self.time_hours_combo.addItems([f"{i:02d}" for i in range(0, 24)])
        self.time_hours_combo.setCurrentText(
            f"{QDateTime.currentDateTime().addSecs(3600).toString('HH')}"
        )
        self.time_hours_combo.setMinimumWidth(50)

        self.time_minutes_combo = QComboBox()
        self.time_minutes_combo.addItems([f"{i:02d}" for i in range(0, 60)])
        self.time_minutes_combo.setCurrentText(
            f"{QDateTime.currentDateTime().addSecs(3600).toString('mm')}"
        )
        self.time_minutes_combo.setMinimumWidth(50)

        datetime_layout.addWidget(self.date_edit)
        datetime_layout.addWidget(QLabel("เวลา:"))
        datetime_layout.addWidget(self.time_hours_combo)
        datetime_layout.addWidget(QLabel(":"))
        datetime_layout.addWidget(self.time_minutes_combo)

        # Hours page
        self.hours_page = QWidget()
        hours_layout = QHBoxLayout(self.hours_page)
        hours_layout.setContentsMargins(0, 0, 0, 0)
        self.hours_combo = QComboBox()
        self.hours_combo.addItems([f"{i} ชั่วโมง" for i in range(1, 25)])
        self.hours_combo.setMinimumWidth(140)
        hours_layout.addWidget(QLabel("ระยะเวลา:"))
        hours_layout.addWidget(self.hours_combo)

        # Minutes page
        self.minutes_page = QWidget()
        minutes_layout = QHBoxLayout(self.minutes_page)
        minutes_layout.setContentsMargins(0, 0, 0, 0)
        self.minutes_combo = QComboBox()
        self.minutes_combo.addItems([f"{i} นาที" for i in range(1, 61)])
        self.minutes_combo.setMinimumWidth(140)
        minutes_layout.addWidget(QLabel("ระยะเวลา:"))
        minutes_layout.addWidget(self.minutes_combo)

        # Seconds page
        self.seconds_page = QWidget()
        seconds_layout = QHBoxLayout(self.seconds_page)
        seconds_layout.setContentsMargins(0, 0, 0, 0)
        self.seconds_combo = QComboBox()
        self.seconds_combo.addItems([f"{i} วินาที" for i in range(10, 301, 10)])
        self.seconds_combo.setMinimumWidth(140)
        seconds_layout.addWidget(QLabel("ระยะเวลา:"))
        seconds_layout.addWidget(self.seconds_combo)

        self.time_stack.addWidget(self.datetime_page)
        self.time_stack.addWidget(self.hours_page)
        self.time_stack.addWidget(self.minutes_page)
        self.time_stack.addWidget(self.seconds_page)
        self.time_stack.setFixedHeight(50)

        card_b_layout.addWidget(self.time_stack)
        grid_layout.addWidget(self.card_time_input, 0, 1)

        # --- Card C: Hero Countdown (Spans 2 columns) ---
        self.card_countdown = BentoCard("หน้าจอตรวจสอบสถานะการนับถอยหลัง", self)
        card_c_layout = self.card_countdown.layout
        card_c_layout.setSpacing(14)

        self.countdown_label = QLabel("--:--:--")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        available_fonts = QFontDatabase.families()
        countdown_font_name = "JetBrains Mono" if "JetBrains Mono" in available_fonts else \
                              "Consolas" if "Consolas" in available_fonts else \
                              "Courier New"
        countdown_font = QFont(countdown_font_name, 48, QFont.Bold)
        countdown_font.setFixedPitch(True)
        self.countdown_label.setFont(countdown_font)
        self.countdown_label.setStyleSheet(
            "background: transparent; color: #e4e4e7; letter-spacing: 2px;"
        )

        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setMinimumHeight(16)
        self.progress_bar.setMaximumHeight(16)

        self.status_label = QLabel("สถานะ: ยังไม่มีการตั้งเวลา")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 10))
        self.status_label.setStyleSheet("color: #a1a1aa; background: transparent;")

        card_c_layout.addWidget(self.countdown_label)
        card_c_layout.addWidget(self.progress_bar)
        card_c_layout.addWidget(self.status_label)
        grid_layout.addWidget(self.card_countdown, 1, 0, 1, 2)

        # --- Card D: Quick Presets ---
        self.card_presets = BentoCard("Quick Presets (ด่วน)", self)
        card_d_layout = self.card_presets.layout

        presets_grid = QGridLayout()
        presets_grid.setSpacing(8)

        self.preset_buttons = []
        for i, preset in enumerate(PRESETS):
            btn = PresetCard(preset["icon"], preset["label"], preset["sublabel"])
            btn.clicked.connect(
                lambda checked,
                v=preset["value"],
                u=preset["unit"]: self.start_preset_timer(v, u)
            )
            self.preset_buttons.append(btn)
            presets_grid.addWidget(btn, i // 2, i % 2)

        card_d_layout.addLayout(presets_grid)
        grid_layout.addWidget(self.card_presets, 2, 0)

        # --- Card E: Controls Panel ---
        self.card_controls = BentoCard("การควบคุมระบบ", self)
        card_e_layout = self.card_controls.layout
        card_e_layout.setSpacing(10)
        card_e_layout.setAlignment(Qt.AlignCenter)

        self.start_button = AnimatedButton(f"{ICONS['start']} เริ่มตั้งเวลา")
        self.cancel_button = AnimatedButton(f"{ICONS['cancel']} ยกเลิก")
        self.clear_button = AnimatedButton(f"{ICONS['clear']} ล้างค่า")

        self.cancel_button.setEnabled(False)
        self.start_button.setMinimumHeight(42)
        self.cancel_button.setMinimumHeight(42)
        self.clear_button.setMinimumHeight(42)

        self.start_button.clicked.connect(self.start_timer)
        self.cancel_button.clicked.connect(self.cancel_timer)
        self.clear_button.clicked.connect(self.clear_fields)

        self.start_button.setToolTip("เริ่มตั้งเวลาปิดเครื่อง/รีสตาร์ท")
        self.cancel_button.setToolTip("ยกเลิกการตั้งเวลาและหยุดการนับถอยหลัง")
        self.clear_button.setToolTip("ล้างค่าและลบไฟล์การตั้งค่าที่บันทึกไว้")

        card_e_layout.addWidget(self.start_button)
        card_e_layout.addWidget(self.cancel_button)
        card_e_layout.addWidget(self.clear_button)
        grid_layout.addWidget(self.card_controls, 2, 1)

        main_layout.addLayout(grid_layout)

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
                #presetValue {
                    color: #1c1917;
                }
                #presetUnit {
                    color: #78716c;
                }
                QPushButton#themeButton {
                    background-color: rgba(0, 0, 0, 0.03);
                    border: 1px solid rgba(0, 0, 0, 0.08);
                    border-radius: 12px;
                    color: #1c1917;
                    font-weight: 600;
                    font-size: 10pt;
                }
                QPushButton#themeButton:hover {
                    background-color: rgba(0, 0, 0, 0.08);
                    border-color: rgba(0, 0, 0, 0.15);
                }
            """
        else:
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
                #presetValue {
                    color: #f4f4f5;
                }
                #presetUnit {
                    color: #a1a1aa;
                }
                QPushButton#themeButton {
                    background-color: rgba(255, 255, 255, 0.03);
                    border: 1px solid rgba(255, 255, 255, 0.08);
                    border-radius: 12px;
                    color: #e4e4e7;
                    font-weight: 600;
                    font-size: 10pt;
                }
                QPushButton#themeButton:hover {
                    background-color: rgba(255, 255, 255, 0.08);
                    border-color: rgba(255, 255, 255, 0.15);
                }
            """
        self.setStyleSheet(base_style)

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

        if self.current_theme_mode == "light":
            light_bg_ends = {
                0: "#fef2f3",  # Shutdown - light pink
                1: "#fff7ed",  # Restart - light orange
                2: "#eff6ff",  # Sleep - light blue
                3: "#faf5ff",  # Hibernate - light purple
            }
            bg_end = light_bg_ends.get(action_index, "#fef2f3")

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

        for btn in self.preset_buttons:
            btn.setStyleSheet(preset_btn_style)

        self.start_button.setStyleSheet(start_btn_style)
        self.cancel_button.setStyleSheet(cancel_btn_style)
        self.clear_button.setStyleSheet(clear_btn_style)

    def on_mode_toggled(self, id, checked):
        """Switch time input widget based on selected mode with smooth slide transition"""
        if not checked:
            return
        self.time_stack.slide_to_index(id)

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

    def start_preset_timer(self, value, unit):
        """Start timer from preset card"""
        if self.is_timer_active:
            self.show_toast("มีการตั้งเวลาอยู่แล้ว กรุณายกเลิกก่อน", "warning")
            return

        # Get selected action
        action_index = self.action_combo.currentIndex()
        if action_index >= 2:  # Sleep or Hibernate
            self.show_toast("Quick Presets รองรับเฉพาะ Shutdown และ Restart", "warning")
            self.action_combo.setCurrentIndex(0)
            return

        is_restart = action_index == 1
        action_text = "รีสตาร์ท" if is_restart else "ปิดเครื่อง"

        # Calculate time
        if unit == "minutes":
            self.target_shutdown_time = datetime.now() + timedelta(minutes=value)
            time_str = f"{value} นาที"
        else:  # hours
            self.target_shutdown_time = datetime.now() + timedelta(hours=value)
            time_str = f"{value} ชั่วโมง"

        reply = QMessageBox.question(
            self,
            f"ยืนยันการตั้งเวลา",
            f"ต้องการตั้งเวลา{action_text}ในอีก {time_str} หรือไม่?\n\n**โปรดบันทึกงานของคุณก่อนดำเนินการครับ!**",
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
            logger.info(f"⚡ [Preset] {action_text} in {time_str} ({total_seconds}s) → ⏰ {self.target_shutdown_time.strftime('%H:%M:%S')}")
            subprocess.run(["shutdown", command, "/t", str(total_seconds)], check=True)

            self.is_timer_active = True
            self.status_label.setText(f"สถานะ: จะ{action_text}เวลา {self.target_shutdown_time.strftime('%H:%M:%S')}")
            self.cancel_button.setEnabled(True)
            self.start_button.setEnabled(False)
            self.countdown_timer.start(1000)

            self.show_toast(f"ตั้งเวลา{action_text}แล้ว: {time_str}", "success")
            self.save_settings()

        except Exception as e:
            self.show_toast(f"ไม่สามารถตั้งเวลาได้: {e}", "error")

    def start_timer(self):
        """Start shutdown/restart timer"""
        if self.is_timer_active:
            self.show_toast("มีการตั้งเวลาอยู่แล้ว กรุณายกเลิกก่อน", "warning")
            return

        action_index = self.action_combo.currentIndex()
        action_map = {
            0: ("ปิดเครื่อง", "/s"),
            1: ("รีสตาร์ท", "/r"),
            2: ("พักเครื่อง", "sleep"),
            3: ("จำศีล", "hibernate"),
        }
        action_text, command_type = action_map.get(action_index, ("ปิดเครื่อง", "/s"))

        # Sleep/Hibernate execute immediately
        if action_index >= 2:
            self._execute_sleep_hibernate(action_text, command_type)
            return

        reply = QMessageBox.question(
            self,
            f"ยืนยันการตั้งเวลา",
            f"คุณต้องการตั้งเวลา{action_text}หรือไม่?\n\n**โปรดบันทึกงานของคุณก่อนดำเนินการครับ!**",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.No:
            return

        try:
            mode_index = self.mode_button_group.checkedId()
            if mode_index == 0:
                date_part = self.date_edit.date()
                hours = int(self.time_hours_combo.currentText())
                minutes = int(self.time_minutes_combo.currentText())
                time_part = QTime(hours, minutes)
                target_qdatetime = QDateTime(date_part, time_part)
                self.target_shutdown_time = target_qdatetime.toPython()
            elif mode_index == 1:
                hours = int(self.hours_combo.currentText().split()[0])
                self.target_shutdown_time = datetime.now() + timedelta(hours=hours)
            elif mode_index == 2:
                minutes = int(self.minutes_combo.currentText().split()[0])
                self.target_shutdown_time = datetime.now() + timedelta(minutes=minutes)
            else:  # mode_index == 3
                seconds = int(self.seconds_combo.currentText().split()[0])
                self.target_shutdown_time = datetime.now() + timedelta(seconds=seconds)

            if self.target_shutdown_time <= datetime.now():
                self.show_toast("กรุณาตั้งเวลา in อนาคต", "warning")
                return

            # Validate max duration (24 hours for safety)
            max_duration = timedelta(hours=24)
            if self.target_shutdown_time - datetime.now() > max_duration:
                self.show_toast("กรุณาตั้งเวลาไม่เกิน 24 ชั่วโมง", "warning")
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
            logger.info(f"⏱️  [Timer] {action_text} in {total_seconds}s → ⏰ {self.target_shutdown_time.strftime('%H:%M:%S')}")
            subprocess.run(
                ["shutdown", command_type, "/t", str(total_seconds)], check=True
            )

            self.is_timer_active = True
            self.status_label.setText(
                f"สถานะ: จะ{action_text}เวลา {self.target_shutdown_time.strftime('%H:%M:%S')}"
            )
            self.cancel_button.setEnabled(True)
            self.start_button.setEnabled(False)
            self.countdown_timer.start(1000)

            self.show_toast(f"ตั้งเวลา{action_text}สำเร็จ", "success")
            self.save_settings()

        except subprocess.CalledProcessError as e:
            error_msg = f"ไม่สามารถตั้งเวลาได้ (Code {e.returncode})"
            if e.returncode == 1190:
                error_msg = "มีการตั้งเวลาปิดเครื่องอยู่แล้ว กรุณากดยกเลิก"
            elif e.returncode == 5:
                error_msg = "ต้องมีสิทธิ์ Administrator เพื่อใช้งานฟีเจอร์นี้"
            logger.error(f"❌ Shutdown command failed (code {e.returncode}): {e}")
            self.show_toast(error_msg, "error")
        except Exception as e:
            logger.error(f"💥 Unexpected error during timer: {e}")
            self.show_toast(f"ไม่สามารถตั้งเวลาได้: {e}", "error")

    def _execute_sleep_hibernate(self, action_text, command_type):
        """Execute Sleep or Hibernate immediately"""
        reply = QMessageBox.question(
            self,
            f"ยืนยันการ{action_text}",
            f"ต้องการ{action_text}ทันทีหรือไม่?\n\n**โปรดบันทึกงานของคุณก่อนดำเนินการครับ!**",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.No:
            return

        try:
            logger.info(f"😴 Executing {action_text} immediately...")
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

            self.status_label.setText(f"สถานะ: กำลัง{action_text}...")
            self.show_toast(f"กำลัง{action_text}...", "info")
        except Exception as e:
            self.show_toast(f"ไม่สามารถ{action_text}ได้: {e}", "error")

    def cancel_timer(self, confirm=True):
        """Cancel active timer"""
        if not self.is_timer_active:
            if confirm:
                self.show_toast("ไม่มีการตั้งเวลาอยู่ในขณะนี้", "info")
            return

        if confirm:
            reply = QMessageBox.question(
                self,
                "ยืนยันการยกเลิก",
                "ต้องการยกเลิกการตั้งเวลาหรือไม่?",
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
            self.status_label.setText("สถานะ: ยกเลิกการตั้งเวลาแล้ว")
            logger.info("✅ Timer cancelled successfully")
            if confirm:
                self.show_toast("ยกเลิกการตั้งเวลาสำเร็จ", "success")
            self.save_settings()
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to cancel shutdown: {e}")
            if confirm:
                if e.returncode == 1116:  # ERROR_NO_SHUTDOWN_IN_PROGRESS
                    self.show_toast("ไม่มีการตั้งเวลาให้ยกเลิก", "info")
                else:
                    self.show_toast(f"ไม่สามารถยกเลิกได้: Code {e.returncode}", "error")
            self.reset_ui_state()
        except Exception as e:
            logger.error(f"💥 Unexpected error during cancel: {e}")
            if confirm:
                self.show_toast(f"ไม่สามารถยกเลิกได้: {e}", "error")
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
            action_text = "รีสตาร์ท" if is_restart else "ปิดเครื่อง"
            self.status_label.setText(f"สถานะ: กำลัง{action_text}...")
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
                self.progress_bar.setFormat(f"{progress}% - เหลือ {mins:02d}:{secs:02d}")
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
        self.date_edit.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self.time_hours_combo.setCurrentText(
            QDateTime.currentDateTime().addSecs(3600).toString("HH")
        )
        self.time_minutes_combo.setCurrentText(
            QDateTime.currentDateTime().addSecs(3600).toString("mm")
        )
        self.hours_combo.setCurrentIndex(0)
        self.minutes_combo.setCurrentIndex(0)
        self.seconds_combo.setCurrentIndex(0)
        self.action_combo.setCurrentIndex(0)
        self.status_label.setText("สถานะ: ยังไม่มีการตั้งเวลา")
        self.countdown_label.setText("--:--:--")
        self.progress_bar.setValue(0)
        self._delete_config_file()
        logger.info("🧹 All fields cleared, config deleted")
        self.show_toast("ล้างค่าเรียบร้อย", "info")

    def reset_ui_state(self):
        """Reset UI state after timer completes"""
        self.is_timer_active = False
        self.countdown_timer.stop()
        self.target_shutdown_time = None
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.progress_bar.setValue(0)
        self.countdown_label.setText("--:--:--")
        self.cancel_button.setEnabled(False)
        self.start_button.setEnabled(True)

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
            "date": self.date_edit.date().toString(Qt.ISODate),
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
            self.radio_datetime.setChecked(True)
            return

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)

            self.action_combo.setCurrentIndex(settings.get("action", 0))

            mode_id = settings.get("mode", 0)
            radio_to_check = self.mode_button_group.button(mode_id)
            if radio_to_check:
                radio_to_check.setChecked(True)

            date_str = settings.get("date")
            if date_str:
                self.date_edit.setDate(QDate.fromString(date_str, Qt.ISODate))

            time_str = settings.get("time")
            if time_str:
                time_parts = time_str.split(":")
                self.time_hours_combo.setCurrentText(time_parts[0])
                self.time_minutes_combo.setCurrentText(time_parts[1])

            self.hours_combo.setCurrentIndex(settings.get("hours", 0))
            self.minutes_combo.setCurrentIndex(settings.get("minutes", 0))
            self.seconds_combo.setCurrentIndex(settings.get("seconds", 0))

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
            
            width = settings.get("width", 650)
            height = settings.get("height", 580)
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
