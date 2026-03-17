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
    QSpinBox,
    QMessageBox,
    QRadioButton,
    QButtonGroup,
    QGroupBox,
    QGridLayout,
    QStackedWidget,
    QGraphicsDropShadowEffect,
    QProgressBar,
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
    QSize,
    QPoint,
    QRect,
)
from PySide6.QtGui import (
    QFont,
    QIcon,
    QColor,
    QPainter,
    QPen,
    QBrush,
    QLinearGradient,
    QRadialGradient,
    QFontDatabase,
)

# --- คำสั่งสำหรับการแพ็กเป็น .exe ด้วย PyInstaller ---
# 1. ติดตั้ง PyInstaller: pip install pyinstaller
# 2. รันคำสั่งนี้ใน Terminal ที่โฟลเดอร์เดียวกับไฟล์ .py:
# pyinstaller --onefile --windowed --name="Windows Shutdown Timer" --icon=icon.ico shutdown_timer.py

CONFIG_FILE = "timer_config.json"

# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# --- Color Themes for Each Action ---
ACTION_COLORS = {
    0: {  # Shutdown - Red
        "name": "shutdown",
        "primary": "#f38ba8",
        "secondary": "#f5c2e7",
        "accent": "#eba0ac",
        "bg_gradient_end": "#2d1f2f",
        "progress": "#f38ba8",
        "icon": "⏻",
    },
    1: {  # Restart - Orange
        "name": "restart",
        "primary": "#fab387",
        "secondary": "#f9e2af",
        "accent": "#f5c2e7",
        "bg_gradient_end": "#2d2520",
        "progress": "#fab387",
        "icon": "↻",
    },
    2: {  # Sleep - Blue
        "name": "sleep",
        "primary": "#89b4fa",
        "secondary": "#b4befe",
        "accent": "#74c7ec",
        "bg_gradient_end": "#1f2535",
        "progress": "#89b4fa",
        "icon": "⏾",
    },
    3: {  # Hibernate - Purple
        "name": "hibernate",
        "primary": "#cba6f7",
        "secondary": "#f5c2e7",
        "accent": "#b4befe",
        "bg_gradient_end": "#2a1f35",
        "progress": "#cba6f7",
        "icon": "⏿",
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


class PresetCard(QPushButton):
    """Glassmorphism preset card button"""

    def __init__(self, icon, label, sublabel, parent=None):
        super().__init__(parent)
        self.setFixedSize(115, 100)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(8, 8, 8, 8)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 20px; background: transparent;")

        value_label = QLabel(label)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setFont(QFont("Segoe UI", 18, QFont.Bold))
        value_label.setStyleSheet("background: transparent; color: #cdd6f4;")

        unit_label = QLabel(sublabel)
        unit_label.setAlignment(Qt.AlignCenter)
        unit_label.setFont(QFont("Segoe UI", 10))
        unit_label.setStyleSheet("background: transparent; color: #a6adc8;")

        layout.addWidget(icon_label)
        layout.addWidget(value_label)
        layout.addWidget(unit_label)

        # Add shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)

        self.shadow_effect = shadow

    def enterEvent(self, event):
        self.shadow_effect.setBlurRadius(25)
        self.shadow_effect.setColor(QColor(0, 0, 0, 80))
        self.shadow_effect.setOffset(0, 6)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.shadow_effect.setBlurRadius(15)
        self.shadow_effect.setColor(QColor(0, 0, 0, 60))
        self.shadow_effect.setOffset(0, 4)
        super().leaveEvent(event)


class Toast(QWidget):
    """Modern toast notification"""

    def __init__(self, parent, message, duration=3000, type_="info"):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        configs = {
            "info":    {"bg": "#1e66f5", "fg": "#ffffff", "icon": "ℹ️"},
            "success": {"bg": "#40a02b", "fg": "#ffffff", "icon": "✅"},
            "warning": {"bg": "#df8e1d", "fg": "#ffffff", "icon": "⚠️"},
            "error":   {"bg": "#d20f39", "fg": "#ffffff", "icon": "❌"},
        }
        cfg = configs.get(type_, configs["info"])

        self.setStyleSheet(f"""
            QWidget#toastBody {{
                background-color: {cfg['bg']};
                border-radius: 14px;
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

        # Drop shadow
        shadow = QGraphicsDropShadowEffect(body)
        shadow.setBlurRadius(24)
        shadow.setColor(QColor(0, 0, 0, 140))
        shadow.setOffset(0, 4)
        body.setGraphicsEffect(shadow)

        layout = QHBoxLayout(body)
        layout.setContentsMargins(18, 12, 18, 12)
        layout.setSpacing(10)

        icon_label = QLabel(cfg["icon"])
        icon_label.setStyleSheet("font-size: 16px; background: transparent;")
        layout.addWidget(icon_label)

        self.label = QLabel(message)
        self.label.setStyleSheet(f"color: {cfg['fg']}; font-size: 13px; font-weight: bold;")
        layout.addWidget(self.label)

        outer.addWidget(body)

        self.duration = duration
        self.animation = None

    def showEvent(self, event):
        super().showEvent(event)
        self.adjustSize()
        parent = self.parent()
        if parent:
            # Position at top center with 20px margin from top
            x = parent.width() // 2 - self.width() // 2
            y = 20
            self.move(x, y)

        # Slide down animation
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(280)
        self.animation.setEasingCurve(QEasingCurve.OutCubic)
        self.animation.setStartValue(QPoint(self.x(), self.y() - 20))
        self.animation.setEndValue(QPoint(self.x(), self.y()))
        self.animation.start()

        QTimer.singleShot(self.duration, self.hide_animation)

    def hide_animation(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(200)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.close)
        self.animation.start()


class ShutdownTimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows Shutdown Timer")
        self.setFixedSize(600, 680)

        # State variables
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.target_shutdown_time = None
        self.is_timer_active = False
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.current_theme = ACTION_COLORS[0]
        self.is_compact = False
        self.current_toast = None

        self.init_ui()
        self.load_settings()
        self.apply_styles()
        self.update_theme_colors(0)

    def init_ui(self):
        """Create and arrange widgets"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(18)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # --- Header with Action Selection ---
        header_layout = QHBoxLayout()

        self.action_combo = QComboBox()
        self.action_combo.addItem(f"{ACTION_COLORS[0]['icon']} ปิดเครื่อง (Shutdown)")
        self.action_combo.addItem(f"{ACTION_COLORS[1]['icon']} รีสตาร์ท (Restart)")
        self.action_combo.addItem(f"{ACTION_COLORS[2]['icon']} พักเครื่อง (Sleep)")
        self.action_combo.addItem(f"{ACTION_COLORS[3]['icon']} จำศีล (Hibernate)")
        self.action_combo.setMinimumHeight(40)
        self.action_combo.setMinimumWidth(280)
        self.action_combo.currentIndexChanged.connect(self.update_theme_colors)

        header_layout.addWidget(QLabel("การกระทำ:"))
        header_layout.addWidget(self.action_combo, 1)
        main_layout.addLayout(header_layout)

        # --- Quick Presets Section (Visual Cards) ---
        presets_group = QGroupBox(f"{ICONS['clock']} Quick Presets")
        presets_layout = QGridLayout(presets_group)
        presets_layout.setSpacing(12)

        self.preset_buttons = []
        for i, preset in enumerate(PRESETS):
            btn = PresetCard(preset["icon"], preset["label"], preset["sublabel"])
            btn.clicked.connect(
                lambda checked,
                v=preset["value"],
                u=preset["unit"]: self.start_preset_timer(v, u)
            )
            self.preset_buttons.append(btn)
            presets_layout.addWidget(btn, 0, i)

        presets_layout.setColumnStretch(4, 1)
        main_layout.addWidget(presets_group)

        # --- Mode Selection (Radio Buttons in horizontal layout) ---
        mode_group = QGroupBox(f"{ICONS['timer']} โหมดการตั้งเวลา")
        mode_layout = QVBoxLayout(mode_group)

        self.mode_button_group = QButtonGroup(self)
        mode_buttons_layout = QGridLayout()
        mode_buttons_layout.setHorizontalSpacing(12)
        mode_buttons_layout.setVerticalSpacing(6)

        self.radio_datetime = QRadioButton(f"{ICONS['calendar']} ระบุวัน/เวลา")
        self.radio_hours = QRadioButton("⏱ นับถอยหลัง (ชั่วโมง)")
        self.radio_minutes = QRadioButton("⏱ นับถอยหลัง (นาที)")
        self.radio_seconds = QRadioButton("⏱ นับถอยหลัง (วินาที)")

        self.mode_button_group.addButton(self.radio_datetime, 0)
        self.mode_button_group.addButton(self.radio_hours, 1)
        self.mode_button_group.addButton(self.radio_minutes, 2)
        self.mode_button_group.addButton(self.radio_seconds, 3)

        self.mode_button_group.idToggled.connect(self.on_mode_toggled)

        mode_buttons_layout.addWidget(self.radio_datetime, 0, 0)
        mode_buttons_layout.addWidget(self.radio_hours, 0, 1)
        mode_buttons_layout.addWidget(self.radio_minutes, 1, 0)
        mode_buttons_layout.addWidget(self.radio_seconds, 1, 1)
        mode_buttons_layout.setColumnStretch(0, 1)
        mode_buttons_layout.setColumnStretch(1, 1)
        mode_layout.addLayout(mode_buttons_layout)

        # --- Time Input Container with Stacked Widget ---
        self.time_stack = QStackedWidget()

        # Datetime page
        self.datetime_page = QWidget()
        datetime_layout = QHBoxLayout(self.datetime_page)
        datetime_layout.setContentsMargins(0, 0, 0, 0)

        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self.date_edit.setDisplayFormat("ddd d MMM yyyy")
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setMinimumWidth(140)

        self.time_hours_combo = QComboBox()
        self.time_hours_combo.addItems([f"{i:02d}" for i in range(0, 24)])
        self.time_hours_combo.setCurrentText(
            f"{QDateTime.currentDateTime().addSecs(3600).toString('HH')}"
        )
        self.time_hours_combo.setMinimumWidth(60)

        self.time_minutes_combo = QComboBox()
        self.time_minutes_combo.addItems([f"{i:02d}" for i in range(0, 60)])
        self.time_minutes_combo.setCurrentText(
            f"{QDateTime.currentDateTime().addSecs(3600).toString('mm')}"
        )
        self.time_minutes_combo.setMinimumWidth(60)

        datetime_layout.addWidget(QLabel("วันที่:"))
        datetime_layout.addWidget(self.date_edit)
        datetime_layout.addWidget(QLabel("เวลา:"))
        datetime_layout.addWidget(self.time_hours_combo)
        datetime_layout.addWidget(QLabel(":"))
        datetime_layout.addWidget(self.time_minutes_combo)
        datetime_layout.addStretch()

        # Hours page
        self.hours_page = QWidget()
        hours_layout = QHBoxLayout(self.hours_page)
        hours_layout.setContentsMargins(0, 0, 0, 0)
        self.hours_combo = QComboBox()
        self.hours_combo.addItems([f"{i} ชั่วโมง" for i in range(1, 25)])
        self.hours_combo.setMinimumWidth(150)
        hours_layout.addWidget(QLabel("ระยะเวลา:"))
        hours_layout.addWidget(self.hours_combo)
        hours_layout.addStretch()

        # Minutes page
        self.minutes_page = QWidget()
        minutes_layout = QHBoxLayout(self.minutes_page)
        minutes_layout.setContentsMargins(0, 0, 0, 0)
        self.minutes_combo = QComboBox()
        self.minutes_combo.addItems([f"{i} นาที" for i in range(1, 61)])
        self.minutes_combo.setMinimumWidth(150)
        minutes_layout.addWidget(QLabel("ระยะเวลา:"))
        minutes_layout.addWidget(self.minutes_combo)
        minutes_layout.addStretch()

        # Seconds page
        self.seconds_page = QWidget()
        seconds_layout = QHBoxLayout(self.seconds_page)
        seconds_layout.setContentsMargins(0, 0, 0, 0)
        self.seconds_combo = QComboBox()
        self.seconds_combo.addItems([f"{i} วินาที" for i in range(10, 301, 10)])
        self.seconds_combo.setMinimumWidth(150)
        seconds_layout.addWidget(QLabel("ระยะเวลา:"))
        seconds_layout.addWidget(self.seconds_combo)
        seconds_layout.addStretch()

        self.time_stack.addWidget(self.datetime_page)
        self.time_stack.addWidget(self.hours_page)
        self.time_stack.addWidget(self.minutes_page)
        self.time_stack.addWidget(self.seconds_page)
        self.time_stack.setFixedHeight(60)

        mode_layout.addWidget(self.time_stack)
        main_layout.addWidget(mode_group)

        # --- Status Section with Beautiful Progress Bar ---
        status_group = QGroupBox("สถานะ")
        status_layout = QVBoxLayout(status_group)
        status_layout.setSpacing(18)
        status_layout.setContentsMargins(20, 16, 20, 16)

        # Countdown display
        self.countdown_label = QLabel("--:--:--")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        countdown_font = QFont("JetBrains Mono, Consolas, monospace", 42, QFont.Bold)
        self.countdown_label.setFont(countdown_font)
        self.countdown_label.setStyleSheet(
            "background: transparent; color: #cdd6f4; letter-spacing: 2px;"
        )

        # Beautiful Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")
        self.progress_bar.setMinimumHeight(28)
        self.progress_bar.setMaximumHeight(28)

        self.status_label = QLabel("สถานะ: ยังไม่มีการตั้งเวลา")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 11))
        self.status_label.setStyleSheet("color: #a6adc8; background: transparent;")

        status_layout.addWidget(self.countdown_label)
        status_layout.addWidget(self.progress_bar)
        status_layout.addWidget(self.status_label)
        main_layout.addWidget(status_group)

        # --- Control Buttons ---
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        self.start_button = QPushButton(f"{ICONS['start']} เริ่มตั้งเวลา")
        self.cancel_button = QPushButton(f"{ICONS['cancel']} ยกเลิก")
        self.clear_button = QPushButton(f"{ICONS['clear']} ล้างค่า")

        self.cancel_button.setEnabled(False)

        self.start_button.setMinimumHeight(45)
        self.cancel_button.setMinimumHeight(45)
        self.clear_button.setMinimumHeight(45)

        self.start_button.clicked.connect(self.start_timer)
        self.cancel_button.clicked.connect(self.cancel_timer)
        self.clear_button.clicked.connect(self.clear_fields)

        self.start_button.setToolTip("เริ่มตั้งเวลาปิดเครื่อง/รีสตาร์ท")
        self.cancel_button.setToolTip("ยกเลิกการตั้งเวลาและหยุดการนับถอยหลัง")
        self.clear_button.setToolTip("ล้างค่าและลบไฟล์การตั้งค่าที่บันทึกไว้")

        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.clear_button)
        main_layout.addLayout(button_layout)

        # Store references for dynamic styling
        self.preset_group = presets_group
        self.mode_group = mode_group
        self.status_group = status_group

    def apply_styles(self):
        """Apply base stylesheet - theme colors will be applied dynamically"""
        base_style = """
            QMainWindow {
                background-color: #1e1e2e;
            }
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', 'Microsoft Sans Serif', sans-serif;
                font-size: 11pt;
            }
            QGroupBox {
                background-color: rgba(49, 50, 68, 0.6);
                border: 1px solid rgba(137, 180, 250, 0.3);
                border-radius: 16px;
                margin-top: 12px;
                padding-top: 12px;
                padding-bottom: 12px;
                padding-left: 16px;
                padding-right: 16px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 0 8px;
                color: #89b4fa;
                font-size: 12pt;
            }
            QLabel {
                color: #cdd6f4;
                background-color: transparent;
            }
            QComboBox, QDateTimeEdit {
                background-color: rgba(49, 50, 68, 0.8);
                border: 1px solid rgba(137, 180, 250, 0.2);
                border-radius: 10px;
                padding: 8px 12px;
                color: #cdd6f4;
                min-width: 80px;
            }
            QComboBox::drop-down, QDateTimeEdit::drop-down {
                border: none;
                width: 24px;
            }
            QComboBox::down-arrow, QDateTimeEdit::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #89b4fa;
            }
            QComboBox:hover, QDateTimeEdit:hover {
                border-color: rgba(137, 180, 250, 0.5);
            }
            QComboBox QAbstractItemView {
                background-color: #313244;
                border: 1px solid #45475a;
                border-radius: 8px;
                selection-background-color: #585b70;
                padding: 4px;
            }
            QRadioButton {
                color: #cdd6f4;
                spacing: 8px;
                font-size: 10pt;
                background: transparent;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #89b4fa;
                background-color: transparent;
            }
            QRadioButton::indicator:checked {
                background-color: #89b4fa;
                border: 2px solid #89b4fa;
            }
            QRadioButton::indicator:hover {
                border-color: #b4befe;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(69, 71, 90, 0.9),
                    stop:1 rgba(49, 50, 68, 0.9));
                border: 1px solid rgba(137, 180, 250, 0.2);
                border-radius: 12px;
                padding: 12px 20px;
                font-weight: bold;
                font-size: 12px;
                color: #cdd6f4;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(88, 91, 112, 0.9),
                    stop:1 rgba(69, 71, 90, 0.9));
                border-color: rgba(137, 180, 250, 0.4);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(49, 50, 68, 0.9),
                    stop:1 rgba(69, 71, 90, 0.9));
            }
            QPushButton:disabled {
                background-color: #45475a;
                color: #6c7086;
                border-color: transparent;
            }
            QProgressBar {
                border: 2px solid rgba(137, 180, 250, 0.2);
                border-radius: 14px;
                text-align: center;
                background-color: rgba(49, 50, 68, 0.8);
                color: #808080;
                font-weight: bold;
                font-size: 12px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #89b4fa,
                    stop:0.5 #b4befe,
                    stop:1 #89b4fa);
                border-radius: 10px;
                margin: 2px;
            }
            QDateTimeEdit::calendar {
                background-color: #313244;
                border: 1px solid #45475a;
            }
            QCalendarWidget QWidget {
                background-color: #313244;
                color: #cdd6f4;
            }
            QCalendarWidget QAbstractItemView:enabled {
                background-color: #313244;
                color: #cdd6f4;
                selection-background-color: #89b4fa;
                selection-color: #1e1e2e;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #6c7086;
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
        """Update theme colors based on selected action"""
        self.current_theme = ACTION_COLORS.get(action_index, ACTION_COLORS[0])
        primary = self.current_theme["primary"]
        secondary = self.current_theme["secondary"]
        accent = self.current_theme["accent"]
        bg_end = self.current_theme["bg_gradient_end"]

        # Update countdown color to match theme
        self.countdown_label.setStyleSheet(
            f"background: transparent; color: {primary}; letter-spacing: 2px;"
        )

        # Dynamic stylesheet for action-specific elements
        dynamic_style = f"""
            QMainWindow {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1e1e2e,
                    stop:1 {bg_end});
            }}
            QGroupBox::title {{
                color: {primary};
            }}
            QComboBox::down-arrow, QDateTimeEdit::down-arrow {{
                border-top-color: {primary};
            }}
            QRadioButton::indicator {{
                border-color: {primary};
            }}
            QRadioButton::indicator:checked {{
                background-color: {primary};
                border-color: {primary};
            }}
            QProgressBar {{
                border-color: rgba({self.hex_to_rgb(primary)}, 0.3);
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 {primary},
                    stop:0.5 {secondary},
                    stop:1 {primary});
            }}
        """

        # Apply dynamic style by combining with base
        current_style = self.styleSheet()
        if "/* DYNAMIC */" in current_style:
            base = current_style.split("/* DYNAMIC */")[0]
        else:
            base = current_style

        self.setStyleSheet(base + "/* DYNAMIC */" + dynamic_style)

        # Update preset button styles
        for btn in self.preset_buttons:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(69, 71, 90, 0.8),
                        stop:1 rgba(49, 50, 68, 0.8));
                    border: 2px solid transparent;
                    border-radius: 16px;
                    padding: 16px;
                }}
                QPushButton:hover {{
                    border-color: {primary};
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(88, 91, 112, 0.9),
                        stop:1 rgba(69, 71, 90, 0.9));
                }}
                QPushButton:pressed {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                        stop:0 rgba(49, 50, 68, 0.9),
                        stop:1 rgba(69, 71, 90, 0.9));
                }}
            """)

        # Update control buttons with action colors
        self.start_button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {primary},
                    stop:1 {accent});
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 13px;
                color: #1e1e2e;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {secondary},
                    stop:1 {primary});
            }}
            QPushButton:pressed {{
                background: {accent};
            }}
        """)

        self.cancel_button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ff6b6b,
                    stop:0.5 #e53e3e,
                    stop:1 #9b2335);
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 13px;
                color: #ffffff;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #ff8e8e,
                    stop:0.5 #fc5c5c,
                    stop:1 #e53e3e);
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e53e3e,
                    stop:1 #7b1d2a);
            }}
            QPushButton:disabled {{
                background-color: #45475a;
                color: #6c7086;
            }}
        """)

        self.clear_button.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #a6adc8,
                    stop:1 #9399b2);
                border: none;
                border-radius: 12px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 13px;
                color: #1e1e2e;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #cdd6f4,
                    stop:1 #a6adc8);
            }}
            QPushButton:pressed {{
                background: #b4befe;
            }}
        """)

    def on_mode_toggled(self, id, checked):
        """Switch time input widget based on selected mode"""
        if not checked:
            return

        # Animate the stack widget change
        self.time_stack.setCurrentIndex(id)

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

            command = "/r" if is_restart else "/s"
            subprocess.run(["shutdown", command, "/t", str(total_seconds)], check=True, timeout=5)

            self.is_timer_active = True
            self.status_label.setText(f"สถานะ: จะ{action_text}ในอีก {time_str}")
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
                self.show_toast("กรุณาตั้งเวลาในอนาคต", "warning")
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

            subprocess.run(
                ["shutdown", command_type, "/t", str(total_seconds)], check=True, timeout=5
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

        except Exception as e:
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
            if command_type == "sleep":
                subprocess.run(
                    ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
                    check=True,
                    timeout=5,
                )
            else:  # hibernate
                subprocess.run(
                    ["rundll32.exe", "powrprof.dll,SetSuspendState", "1,1,0"],
                    check=True,
                    timeout=5,
                )

            self.status_label.setText(f"สถานะ: กำลัง{action_text}...")
            self.show_toast(f"กำลัง{action_text}...", "info")
        except Exception as e:
            self.show_toast(f"ไม่สามารถ{action_text}ได้: {e}", "error")

    def cancel_timer(self):
        """Cancel active timer"""
        if not self.is_timer_active:
            self.show_toast("ไม่มีการตั้งเวลาอยู่ในขณะนี้", "info")
            return

        reply = QMessageBox.question(
            self,
            "ยืนยันการยกเลิก",
            "ต้องการยกเลิกการตั้งเวลาหรือไม่?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:
            try:
                subprocess.run(["shutdown", "/a"], check=True, timeout=5)
                self.reset_ui_state()
                self.status_label.setText("สถานะ: ยกเลิกการตั้งเวลาแล้ว")
                self.show_toast("ยกเลิกการตั้งเวลาสำเร็จ", "error")
            except Exception as e:
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

            # Update progress bar
            if self.total_seconds > 0:
                progress = int(
                    (self.total_seconds - self.remaining_seconds)
                    / self.total_seconds
                    * 100
                )
                self.progress_bar.setValue(min(100, progress))

    def show_toast(self, message, type_="info"):
        """Show toast notification"""
        if self.current_toast is not None:
            try:
                self.current_toast.close()
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
        self.countdown_timer.stop()
        self._delete_config_file()
        super().closeEvent(event)

    def _delete_config_file(self):
        """Safely delete config file"""
        try:
            if os.path.exists(CONFIG_FILE):
                os.remove(CONFIG_FILE)
        except Exception as e:
            logger.warning(f"Could not delete config file: {e}")

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
            # Write to temp file first, then atomically move
            import tempfile
            fd, temp_path = tempfile.mkstemp(suffix='.json', text=True)
            try:
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    json.dump(settings, f, indent=4)
                # Atomic rename to avoid corruption from concurrent access
                if sys.platform == "win32":
                    os.replace(temp_path, CONFIG_FILE)
                else:
                    os.rename(temp_path, CONFIG_FILE)
            except Exception:
                try:
                    os.unlink(temp_path)
                except Exception:
                    pass
                raise
        except Exception as e:
            logger.error(f"Could not save settings: {e}")

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
            logger.error(f"Could not load settings: {e}")


if __name__ == "__main__":
    import signal
    import tempfile
    
    app = QApplication(sys.argv)

    # Set locale for consistent number display
    QLocale.setDefault(QLocale.C)

    # Handle keyboard interrupt (Ctrl+C) gracefully
    def handle_signal(sig, frame):
        if 'window' in globals() and window.is_timer_active:
            window.cancel_timer()
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
