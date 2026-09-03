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
    QByteArray,
)
from PySide6.QtGui import (
    QFont,
    QColor,
    QFontDatabase,
    QIcon,
    QPixmap,
    QPainter,
)
from PySide6.QtSvg import QSvgRenderer

CONFIG_FILE = "timer_config.json"
WINDOW_CONFIG_FILE = "window_config.json"


def resource_path(relative_name: str) -> str:
    """Return absolute path to a bundled resource."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative_name)


# Initialize logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
_handler = logging.StreamHandler()
_handler.setFormatter(logging.Formatter("%(asctime)s │ %(message)s", datefmt="%H:%M:%S"))
logger.addHandler(_handler)

# --- SVG Vector Icon Library (Zero Emoji Slop) ---
SVG_ICONS = {
    "power": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M18.36 6.64a9 9 0 1 1-12.73 0"/><line x1="12" y1="2" x2="12" y2="12"/></svg>',
    "restart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21.5 2v6h-6M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-5.67"/></svg>',
    "moon": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',
    "hibernate": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M2 12h20M4.93 4.93l14.14 14.14M4.93 19.07L19.07 4.93"/><path d="M10 4l2-2 2 2M10 20l2 2 2-2M4 10l-2 2 2 2M20 10l2 2-2 2"/></svg>',
    "sun": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>',
    "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>',
    "play": '<svg viewBox="0 0 24 24" fill="currentColor" stroke="none"><polygon points="6 4 20 12 6 20 6 4"/></svg>',
    "x": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    "reset": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>',
    "alert": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>',
    "chevron_down": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>',
}


def render_svg_icon(name: str, color: str = "#ffffff", size: int = 18) -> QIcon:
    """Render an SVG string into a crisp QIcon with the requested color and size."""
    svg = SVG_ICONS.get(name, "")
    if not svg:
        return QIcon()
    svg_colored = svg.replace("currentColor", color)
    renderer = QSvgRenderer(QByteArray(svg_colored.encode("utf-8")))
    pixmap = QPixmap(size * 2, size * 2)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    pixmap.setDevicePixelRatio(2.0)
    return QIcon(pixmap)


def ensure_chevron_assets():
    """Ensure crisp chevron SVGs exist in local directory for QSS styling"""
    chevron_svg_dark = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#8b949e" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>'
    chevron_svg_light = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="#52525b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>'
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dark_path = os.path.join(base_dir, "chevron_dark.svg")
    light_path = os.path.join(base_dir, "chevron_light.svg")
    try:
        with open(dark_path, "w", encoding="utf-8") as f:
            f.write(chevron_svg_dark)
        with open(light_path, "w", encoding="utf-8") as f:
            f.write(chevron_svg_light)
    except Exception as e:
        logger.warning(f"Could not write chevron assets: {e}")
    return dark_path.replace("\\", "/"), light_path.replace("\\", "/")


CHEVRON_DARK_PATH, CHEVRON_LIGHT_PATH = ensure_chevron_assets()


# --- Refined Semantic Accents for Each Action ---
ACTION_COLORS = {
    0: {  # Shutdown - Crimson / Rose
        "name": "shutdown",
        "primary": "#f43f5e",
        "secondary": "#fb7185",
        "accent": "#e11d48",
        "bg_subtle_dark": "rgba(244, 63, 94, 0.12)",
        "bg_subtle_light": "rgba(244, 63, 94, 0.08)",
        "icon": "power",
        "label_en": "Shutdown",
        "label_th": "ปิดเครื่อง",
    },
    1: {  # Restart - Warm Amber
        "name": "restart",
        "primary": "#f59e0b",
        "secondary": "#fbbf24",
        "accent": "#d97706",
        "bg_subtle_dark": "rgba(245, 158, 11, 0.12)",
        "bg_subtle_light": "rgba(245, 158, 11, 0.08)",
        "icon": "restart",
        "label_en": "Restart",
        "label_th": "รีสตาร์ท",
    },
    2: {  # Sleep - Sky / Slate Blue
        "name": "sleep",
        "primary": "#0ea5e9",
        "secondary": "#38bdf8",
        "accent": "#0284c7",
        "bg_subtle_dark": "rgba(14, 165, 233, 0.12)",
        "bg_subtle_light": "rgba(14, 165, 233, 0.08)",
        "icon": "moon",
        "label_en": "Sleep",
        "label_th": "พักเครื่อง",
    },
    3: {  # Hibernate - Soft Violet
        "name": "hibernate",
        "primary": "#a855f7",
        "secondary": "#c084fc",
        "accent": "#7e22ce",
        "bg_subtle_dark": "rgba(168, 85, 247, 0.12)",
        "bg_subtle_light": "rgba(168, 85, 247, 0.08)",
        "icon": "hibernate",
        "label_en": "Hibernate",
        "label_th": "จำศีล",
    },
}

# --- Preset Configurations ---
PRESETS = [
    {"value": 15, "unit": "minutes", "label": "15m", "sub_en": "15 min", "sub_th": "15 นาที"},
    {"value": 30, "unit": "minutes", "label": "30m", "sub_en": "30 min", "sub_th": "30 นาที"},
    {"value": 1, "unit": "hours", "label": "1h", "sub_en": "1 hour", "sub_th": "1 ชม."},
    {"value": 2, "unit": "hours", "label": "2h", "sub_en": "2 hours", "sub_th": "2 ชม."},
]

# --- Localization Dictionary ---
STRINGS = {
    "en": {
        "app_title": "Windows Shutdown Timer",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "lang_name": "ไทย",
        "section_action": "ACTION",
        "section_duration": "DURATION",
        "status_ready": "Ready",
        "status_active": "{action} at {time}",
        "status_executing": "Executing {action}...",
        "status_cancelled": "Cancelled",
        "mode_timer": "Timer",
        "mode_clock": "Clock",
        "unit_hours": "Hours",
        "unit_minutes": "Minutes",
        "unit_seconds": "Seconds",
        "unit_date": "Date",
        "btn_start": "Start Countdown",
        "btn_cancel": "Cancel",
        "btn_clear": "Reset",
        "confirm_title": "Confirm Schedule",
        "confirm_timer_desc": "Do you want to schedule {action} in {time}?\n\nPlease save your work before proceeding!",
        "confirm_clock_desc": "Do you want to schedule {action} at {time}?\n\nPlease save your work before proceeding!",
        "confirm_exec_desc": "Do you want to execute {action} immediately?\n\nPlease save your work before proceeding!",
        "confirm_cancel_title": "Confirm Cancel",
        "confirm_cancel_desc": "Are you sure you want to cancel the scheduled timer?",
        "toast_scheduled": "Scheduled {action} for {time}",
        "toast_cancelled": "Timer cancelled successfully",
        "toast_already_active": "A timer is already active. Please cancel first.",
        "toast_preset_limit": "Quick Presets only support Shutdown & Restart",
        "toast_future_time": "Please select a future time",
        "toast_zero_duration": "Please specify a duration greater than 0",
        "toast_max_duration": "Please set time within 72 hours",
        "toast_all_reset": "All fields reset",
        "toast_no_active": "No active timer",
        "toast_no_shutdown_to_cancel": "No scheduled shutdown to cancel",
        "toast_cannot_schedule": "Cannot schedule: {error}",
        "toast_cannot_execute": "Cannot execute {action}: {error}",
        "toast_cannot_cancel": "Cannot cancel: {error}",
    },
    "th": {
        "app_title": "Windows Shutdown Timer",
        "theme_light": "โหมดสว่าง",
        "theme_dark": "โหมดมืด",
        "lang_name": "English",
        "section_action": "เลือกคำสั่ง",
        "section_duration": "กำหนดเวลา",
        "status_ready": "พร้อมทำงาน",
        "status_active": "{action}เวลา {time}",
        "status_executing": "กำลัง{action}...",
        "status_cancelled": "ยกเลิกแล้ว",
        "mode_timer": "นับถอยหลัง",
        "mode_clock": "ระบุเวลา",
        "unit_hours": "ชั่วโมง",
        "unit_minutes": "นาที",
        "unit_seconds": "วินาที",
        "unit_date": "วันที่",
        "btn_start": "เริ่มนับถอยหลัง",
        "btn_cancel": "ยกเลิก",
        "btn_clear": "ล้างค่า",
        "confirm_title": "ยืนยันการตั้งเวลา",
        "confirm_timer_desc": "ต้องการตั้งเวลา{action}ในอีก {time} หรือไม่?\n\nโปรดบันทึกงานของคุณก่อนดำเนินการครับ!",
        "confirm_clock_desc": "ต้องการตั้งเวลา{action}เวลา {time} หรือไม่?\n\nโปรดบันทึกงานของคุณก่อนดำเนินการครับ!",
        "confirm_exec_desc": "ต้องการ{action}ทันทีหรือไม่?\n\nโปรดบันทึกงานของคุณก่อนดำเนินการครับ!",
        "confirm_cancel_title": "ยืนยันการยกเลิก",
        "confirm_cancel_desc": "ต้องการยกเลิกการตั้งเวลาหรือไม่?",
        "toast_scheduled": "ตั้งเวลา{action}สำเร็จ: {time}",
        "toast_cancelled": "ยกเลิกการตั้งเวลาสำเร็จ",
        "toast_already_active": "มีการตั้งเวลาอยู่แล้ว กรุณายกเลิกก่อน",
        "toast_preset_limit": "Quick Presets รองรับเฉพาะ Shutdown และ Restart",
        "toast_future_time": "กรุณาตั้งเวลาในอนาคต",
        "toast_zero_duration": "กรุณาระบุระยะเวลานับถอยหลังมากกว่า 0",
        "toast_max_duration": "กรุณาตั้งเวลาไม่เกิน 72 ชั่วโมง",
        "toast_all_reset": "ล้างค่าเรียบร้อย",
        "toast_no_active": "ไม่มีการตั้งเวลาอยู่ในขณะนี้",
        "toast_no_shutdown_to_cancel": "ไม่มีการตั้งเวลาให้ยกเลิก",
        "toast_cannot_schedule": "ไม่สามารถตั้งเวลาได้: {error}",
        "toast_cannot_execute": "ไม่สามารถ{action}ได้: {error}",
        "toast_cannot_cancel": "ไม่สามารถยกเลิกได้: {error}",
    },
}


def get_modern_font_name():
    """Return the most modern, loopless Thai sans-serif font available on the system."""
    try:
        families = QFontDatabase.families()
    except Exception:
        families = []
    for candidate in [
        "IBM Plex Sans Thai",
        "Kanit",
        "Segoe UI Variable Display",
        "Segoe UI",
        "Leelawadee UI",
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
    """Refined push button with micro-scale feedback and border highlights"""

    def __init__(self, text="", parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.PointingHandCursor)

    def enterEvent(self, event):
        self.setProperty("hovered", True)
        self.style().unpolish(self)
        self.style().polish(self)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.setProperty("hovered", False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self.setProperty("pressed_state", True)
        self.style().unpolish(self)
        self.style().polish(self)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setProperty("pressed_state", False)
        self.style().unpolish(self)
        self.style().polish(self)
        super().mouseReleaseEvent(event)


class PresetChip(AnimatedButton):
    """Compact minimalist preset button chip"""

    def __init__(self, label: str, parent=None):
        super().__init__(label, parent)
        self.setObjectName("presetChip")
        self.setMinimumHeight(38)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFont(get_modern_font(11, weight=QFont.DemiBold))


# Backward compatibility alias
PresetCard = PresetChip


class BentoCard(QFrame):
    """Clean precision card enclosure with subtle 1px border"""

    def __init__(self, title="", parent=None):
        super().__init__(parent)
        self.setObjectName("bentoCard")

        self.card_layout = QVBoxLayout(self)
        self.card_layout.setContentsMargins(16, 12, 16, 12)
        self.card_layout.setSpacing(8)
        self.card_layout.setSizeConstraint(QLayout.SetMinimumSize)

        self.title_label = None
        if title:
            self.title_label = QLabel(title)
            self.title_label.setObjectName("bentoCardTitle")
            self.title_label.setFont(get_modern_font(9.5, weight=QFont.Bold))
            self.card_layout.addWidget(self.title_label)

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
        self.m_speed = 220
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
    """Modern translucent glass toast notification with vector icon"""

    def __init__(self, parent, message, duration=3000, type_="info"):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        configs = {
            "info":    {"accent": "#0ea5e9", "icon": "info"},
            "success": {"accent": "#10b981", "icon": "check"},
            "warning": {"accent": "#f59e0b", "icon": "alert"},
            "error":   {"accent": "#f43f5e", "icon": "alert"},
        }
        cfg = configs.get(type_, configs["info"])

        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        body = QWidget()
        body.setObjectName("toastBody")

        layout = QHBoxLayout(body)
        layout.setContentsMargins(14, 8, 16, 8)
        layout.setSpacing(10)

        icon_label = QLabel()
        icon_label.setPixmap(render_svg_icon(cfg["icon"], color=cfg["accent"], size=16).pixmap(16, 16))
        layout.addWidget(icon_label)

        self.label = QLabel(message)
        self.label.setFont(get_modern_font(10, weight=QFont.DemiBold))
        self.label.setStyleSheet("color: #f1f5f9; background: transparent;")
        layout.addWidget(self.label)

        body.setStyleSheet(f"""
            QWidget#toastBody {{
                background-color: rgba(22, 27, 34, 0.94);
                border: 1px solid rgba(255, 255, 255, 0.12);
                border-left: 3px solid {cfg['accent']};
                border-radius: 8px;
            }}
        """)

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

        self.anim_pos = QPropertyAnimation(self, b"pos")
        self.anim_pos.setDuration(220)
        self.anim_pos.setEasingCurve(QEasingCurve.OutCubic)
        self.anim_pos.setStartValue(QPoint(self.x(), self.y() - 20))
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
        self.anim_fade.setDuration(220)
        self.anim_fade.setStartValue(1.0)
        self.anim_fade.setEndValue(0.0)
        self.anim_fade.finished.connect(self.close)
        self.anim_fade.start()


class ShutdownTimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows Shutdown Timer")

        icon_path = resource_path("off.ico")
        if not os.path.isfile(icon_path):
            icon_path = resource_path("off.png")
        if os.path.isfile(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Dedicated Fixed Utility Dimensions (compact, no empty void)
        self.setFixedSize(520, 560)

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
        self.current_lang = "en"

        self.init_ui()
        self.load_window_settings()
        self.load_settings()
        self.action_combo.currentIndexChanged.connect(self.on_action_changed)
        self.apply_styles()
        self.update_theme_colors(self.action_combo.currentIndex())
        self.update_localized_text()
        logger.info("🚀 Application started with Raycast / Linear Precision architecture")

    def t(self, key: str, **kwargs) -> str:
        """Get localized string for current language."""
        lang_dict = STRINGS.get(self.current_lang, STRINGS["en"])
        val = lang_dict.get(key, STRINGS["en"].get(key, key))
        if kwargs:
            try:
                return val.format(**kwargs)
            except Exception:
                return val
        return val

    def init_ui(self):
        """Create and arrange widgets in a Centered Modern Precision layout"""
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)

        # Snug, non-stretched cohesive container
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(18, 14, 18, 16)
        self.content_container = central_widget

        # --- 1. Header Bar ---
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(2, 0, 2, 2)
        header_layout.setSpacing(8)

        self.title_label = QLabel(self.t("app_title"))
        self.title_label.setObjectName("appTitle")
        self.title_label.setFont(get_modern_font(13.5, bold=True))
        header_layout.addWidget(self.title_label)

        header_layout.addStretch()

        # Language Switcher Pill
        self.lang_button = QPushButton("ไทย")
        self.lang_button.setObjectName("headerButton")
        self.lang_button.setCursor(Qt.PointingHandCursor)
        self.lang_button.setMinimumHeight(30)
        self.lang_button.setFont(get_modern_font(9.5, weight=QFont.DemiBold))
        self.lang_button.setIcon(render_svg_icon("globe", color="#94a3b8", size=14))
        self.lang_button.clicked.connect(self.toggle_language)
        header_layout.addWidget(self.lang_button)

        # Theme Switcher Pill
        self.theme_button = QPushButton()
        self.theme_button.setObjectName("headerButton")
        self.theme_button.setCursor(Qt.PointingHandCursor)
        self.theme_button.setMinimumHeight(30)
        self.theme_button.setFont(get_modern_font(9.5, weight=QFont.DemiBold))
        self.theme_button.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_button)

        main_layout.addLayout(header_layout)

        # --- 2. Hero Section: Precision Chronometer ---
        self.card_countdown = BentoCard("", self)
        card_c_layout = self.card_countdown.layout
        card_c_layout.setContentsMargins(16, 12, 16, 12)
        card_c_layout.setSpacing(6)

        # Live Status Indicator Row
        status_row = QHBoxLayout()
        status_row.setSpacing(6)
        status_row.addStretch()

        self.status_dot = QLabel()
        self.status_dot.setObjectName("statusDot")
        self.status_dot.setFixedSize(8, 8)
        status_row.addWidget(self.status_dot)

        self.status_label = QLabel(self.t("status_ready"))
        self.status_label.setObjectName("statusLabel")
        self.status_label.setFont(get_modern_font(10, weight=QFont.DemiBold))
        status_row.addWidget(self.status_label)
        status_row.addStretch()
        card_c_layout.addLayout(status_row)

        # Large Tabular Countdown Digits
        self.countdown_label = QLabel("00:00:00")
        self.countdown_label.setObjectName("countdownLabel")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        available_fonts = QFontDatabase().families()
        countdown_font_name = "JetBrains Mono" if "JetBrains Mono" in available_fonts else \
                              "Consolas" if "Consolas" in available_fonts else \
                              "Courier New"
        countdown_font = QFont(countdown_font_name, 40, QFont.Bold)
        countdown_font.setFixedPitch(True)
        self.countdown_label.setFont(countdown_font)
        card_c_layout.addWidget(self.countdown_label)

        # Slim Micro-Progress Line (3px height)
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(3)
        card_c_layout.addWidget(self.progress_bar)

        main_layout.addWidget(self.card_countdown)

        # --- 3. Action Selector Section ---
        self.card_action = BentoCard("", self)
        card_action_layout = self.card_action.layout
        card_action_layout.setContentsMargins(16, 10, 16, 12)
        card_action_layout.setSpacing(8)

        self.label_action_sec = QLabel(self.t("section_action"))
        self.label_action_sec.setObjectName("quietSectionHeader")
        self.label_action_sec.setFont(get_modern_font(9, weight=QFont.Bold))
        card_action_layout.addWidget(self.label_action_sec)

        # Hidden combo box preserved for legacy API compatibility
        self.action_combo = QComboBox()
        for i in range(4):
            self.action_combo.addItem(ACTION_COLORS[i]["label_en"])
        self.action_combo.setVisible(False)

        action_row = QHBoxLayout()
        action_row.setSpacing(8)

        self.action_buttons = []
        self.action_button_group = QButtonGroup(self)
        self.action_button_group.setExclusive(True)

        for i in range(4):
            info = ACTION_COLORS[i]
            btn = QPushButton()
            btn.setCheckable(True)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setMinimumHeight(38)
            btn.setObjectName("actionPill")
            btn.setFont(get_modern_font(10, weight=QFont.DemiBold))
            btn.clicked.connect(lambda checked, idx=i: self.action_combo.setCurrentIndex(idx))
            self.action_button_group.addButton(btn, i)
            self.action_buttons.append(btn)
            action_row.addWidget(btn)

        self.action_buttons[0].setChecked(True)
        card_action_layout.addLayout(action_row)
        main_layout.addWidget(self.card_action)

        self.card_action_mode = self.card_action  # Legacy alias

        # --- 4. Duration & Time Setting Section ---
        self.card_time = BentoCard("", self)
        card_time_layout = self.card_time.layout
        card_time_layout.setContentsMargins(16, 10, 16, 12)
        card_time_layout.setSpacing(8)

        self.label_duration_sec = QLabel(self.t("section_duration"))
        self.label_duration_sec.setObjectName("quietSectionHeader")
        self.label_duration_sec.setFont(get_modern_font(9, weight=QFont.Bold))
        card_time_layout.addWidget(self.label_duration_sec)

        # Presets Row: Minimalist Chips
        presets_row = QHBoxLayout()
        presets_row.setSpacing(8)

        self.preset_buttons = []
        for i, preset in enumerate(PRESETS):
            btn = PresetChip(preset["label"])
            btn.clicked.connect(
                lambda checked,
                v=preset["value"],
                u=preset["unit"]: self.start_preset_timer(v, u)
            )
            self.preset_buttons.append(btn)
            presets_row.addWidget(btn)

        card_time_layout.addLayout(presets_row)

        # Mode Switcher: Segmented Pill Tab using ButtonGroup of PushButtons (no radio circles!)
        mode_switcher_frame = QFrame()
        mode_switcher_frame.setObjectName("segmentedControl")
        mode_switcher_layout = QHBoxLayout(mode_switcher_frame)
        mode_switcher_layout.setContentsMargins(3, 3, 3, 3)
        mode_switcher_layout.setSpacing(4)

        self.tab_timer = QPushButton(self.t("mode_timer"))
        self.tab_timer.setObjectName("segmentedTab")
        self.tab_timer.setCheckable(True)
        self.tab_timer.setChecked(True)
        self.tab_timer.setCursor(Qt.PointingHandCursor)
        self.tab_timer.setFont(get_modern_font(10, weight=QFont.DemiBold))

        self.tab_clock = QPushButton(self.t("mode_clock"))
        self.tab_clock.setObjectName("segmentedTab")
        self.tab_clock.setCheckable(True)
        self.tab_clock.setCursor(Qt.PointingHandCursor)
        self.tab_clock.setFont(get_modern_font(10, weight=QFont.DemiBold))

        self.mode_button_group = QButtonGroup(self)
        self.mode_button_group.setExclusive(True)
        self.mode_button_group.addButton(self.tab_timer, 0)
        self.mode_button_group.addButton(self.tab_clock, 1)
        self.mode_button_group.idToggled.connect(self.on_mode_toggled)

        mode_switcher_layout.addWidget(self.tab_timer)
        mode_switcher_layout.addWidget(self.tab_clock)
        card_time_layout.addWidget(mode_switcher_frame)

        # Backward compatibility aliases
        self.radio_timer = self.tab_timer
        self.radio_clock = self.tab_clock
        self.radio_datetime = self.tab_clock
        self.radio_hours = self.tab_timer
        self.radio_minutes = self.tab_timer
        self.radio_seconds = self.tab_timer

        # Sliding Stacked Time Inputs
        self.time_stack = SlidingStackedWidget()

        # Page 0: Timer mode (Hours, Minutes, Seconds dropdowns)
        self.timer_page = QWidget()
        timer_input_layout = QHBoxLayout(self.timer_page)
        timer_input_layout.setContentsMargins(0, 2, 0, 2)
        timer_input_layout.setSpacing(8)

        # Hours Dropdown
        h_layout = QVBoxLayout()
        h_layout.setSpacing(3)
        self.lbl_h = QLabel(self.t("unit_hours"))
        self.lbl_h.setObjectName("timeUnitLabel")
        self.lbl_h.setFont(get_modern_font(9, weight=QFont.DemiBold))
        self.hours_combo = QComboBox()
        self.hours_combo.setObjectName("timeComboBox")
        self.hours_combo.addItems([f"{i} hr" for i in range(25)])
        self.hours_combo.setCurrentIndex(0)
        self.hours_combo.setMinimumHeight(38)
        h_layout.addWidget(self.lbl_h)
        h_layout.addWidget(self.hours_combo)

        # Minutes Dropdown
        m_layout = QVBoxLayout()
        m_layout.setSpacing(3)
        self.lbl_m = QLabel(self.t("unit_minutes"))
        self.lbl_m.setObjectName("timeUnitLabel")
        self.lbl_m.setFont(get_modern_font(9, weight=QFont.DemiBold))
        self.minutes_combo = QComboBox()
        self.minutes_combo.setObjectName("timeComboBox")
        self.minutes_combo.addItems([f"{i} min" for i in range(60)])
        self.minutes_combo.setCurrentIndex(30)
        self.minutes_combo.setMinimumHeight(38)
        m_layout.addWidget(self.lbl_m)
        m_layout.addWidget(self.minutes_combo)

        # Seconds Dropdown
        s_layout = QVBoxLayout()
        s_layout.setSpacing(3)
        self.lbl_s = QLabel(self.t("unit_seconds"))
        self.lbl_s.setObjectName("timeUnitLabel")
        self.lbl_s.setFont(get_modern_font(9, weight=QFont.DemiBold))
        self.seconds_combo = QComboBox()
        self.seconds_combo.setObjectName("timeComboBox")
        self.seconds_combo.addItems([f"{i} sec" for i in range(60)])
        self.seconds_combo.setCurrentIndex(0)
        self.seconds_combo.setMinimumHeight(38)
        s_layout.addWidget(self.lbl_s)
        s_layout.addWidget(self.seconds_combo)

        timer_input_layout.addLayout(h_layout)
        timer_input_layout.addLayout(m_layout)
        timer_input_layout.addLayout(s_layout)

        # Compatibility proxies
        self.spin_hours = SpinBoxProxy(self.hours_combo, 24)
        self.spin_minutes = SpinBoxProxy(self.minutes_combo, 59)
        self.spin_seconds = SpinBoxProxy(self.seconds_combo, 59)

        # Page 1: Clock mode (Date picker + Hour/Minute dropdowns)
        self.clock_page = QWidget()
        clock_layout = QHBoxLayout(self.clock_page)
        clock_layout.setContentsMargins(0, 2, 0, 2)
        clock_layout.setSpacing(8)

        # Column 1: Date Picker with Calendar
        date_col_layout = QVBoxLayout()
        date_col_layout.setSpacing(3)
        self.lbl_date = QLabel(self.t("unit_date"))
        self.lbl_date.setObjectName("timeUnitLabel")
        self.lbl_date.setFont(get_modern_font(9, weight=QFont.DemiBold))
        self.date_picker = QDateEdit()
        self.date_picker.setObjectName("datePicker")
        self.date_picker.setCalendarPopup(True)
        self.date_picker.setDisplayFormat("ddd d MMM yyyy")
        self.date_picker.setMinimumHeight(38)
        self.date_picker.setAlignment(Qt.AlignCenter)
        date_col_layout.addWidget(self.lbl_date)
        date_col_layout.addWidget(self.date_picker)

        # Column 2: Hours Dropdown
        clock_h_layout = QVBoxLayout()
        clock_h_layout.setSpacing(3)
        self.lbl_clock_h = QLabel(self.t("unit_hours"))
        self.lbl_clock_h.setObjectName("timeUnitLabel")
        self.lbl_clock_h.setFont(get_modern_font(9, weight=QFont.DemiBold))
        self.time_hours_combo = QComboBox()
        self.time_hours_combo.setObjectName("timeComboBox")
        self.time_hours_combo.addItems([f"{i:02d}" for i in range(24)])
        self.time_hours_combo.setMinimumHeight(38)
        clock_h_layout.addWidget(self.lbl_clock_h)
        clock_h_layout.addWidget(self.time_hours_combo)

        # Column 3: Minutes Dropdown
        clock_m_layout = QVBoxLayout()
        clock_m_layout.setSpacing(3)
        self.lbl_clock_m = QLabel(self.t("unit_minutes"))
        self.lbl_clock_m.setObjectName("timeUnitLabel")
        self.lbl_clock_m.setFont(get_modern_font(9, weight=QFont.DemiBold))
        self.time_minutes_combo = QComboBox()
        self.time_minutes_combo.setObjectName("timeComboBox")
        self.time_minutes_combo.addItems([f"{i:02d}" for i in range(60)])
        self.time_minutes_combo.setMinimumHeight(38)
        clock_m_layout.addWidget(self.lbl_clock_m)
        clock_m_layout.addWidget(self.time_minutes_combo)

        clock_layout.addLayout(date_col_layout)
        clock_layout.addLayout(clock_h_layout)
        clock_layout.addLayout(clock_m_layout)

        init_dt = QDateTime.currentDateTime().addSecs(3600)
        self.date_picker.setDate(init_dt.date())
        self.time_hours_combo.setCurrentIndex(init_dt.time().hour())
        self.time_minutes_combo.setCurrentIndex(init_dt.time().minute())

        self.date_edit = DateTimeProxy(self.date_picker, self.time_hours_combo, self.time_minutes_combo)

        self.datetime_page = self.clock_page
        self.hours_page = self.timer_page
        self.minutes_page = self.timer_page
        self.seconds_page = self.timer_page

        self.time_stack.addWidget(self.timer_page)
        self.time_stack.addWidget(self.clock_page)
        self.time_stack.setFixedHeight(72)
        card_time_layout.addWidget(self.time_stack)

        main_layout.addWidget(self.card_time)

        self.card_time_input = self.card_time
        self.card_presets = self.card_time

        # --- 5. Ergonomic Bottom Action Bar (Directly beneath DURATION card) ---
        self.card_controls = QWidget(self)
        self.card_controls.setObjectName("bottomActionBar")
        controls_layout = QHBoxLayout(self.card_controls)
        controls_layout.setContentsMargins(0, 2, 0, 2)
        controls_layout.setSpacing(8)

        self.cancel_button = AnimatedButton(self.t("btn_cancel"))
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.setIcon(render_svg_icon("x", color="#f43f5e", size=14))
        self.cancel_button.setEnabled(False)
        self.cancel_button.setMinimumHeight(42)
        self.cancel_button.setFont(get_modern_font(10, weight=QFont.DemiBold))

        self.clear_button = AnimatedButton(self.t("btn_clear"))
        self.clear_button.setObjectName("clearButton")
        self.clear_button.setIcon(render_svg_icon("reset", color="#71717a", size=14))
        self.clear_button.setMinimumHeight(42)
        self.clear_button.setFont(get_modern_font(10, weight=QFont.DemiBold))

        self.start_button = AnimatedButton(self.t("btn_start"))
        self.start_button.setObjectName("startButton")
        self.start_button.setIcon(render_svg_icon("play", color="#ffffff", size=14))
        self.start_button.setMinimumHeight(42)
        self.start_button.setFont(get_modern_font(11, bold=True))
        self.start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.start_button.clicked.connect(self.start_timer)
        self.cancel_button.clicked.connect(self.cancel_timer)
        self.clear_button.clicked.connect(self.clear_fields)

        controls_layout.addWidget(self.cancel_button)
        controls_layout.addWidget(self.clear_button)
        controls_layout.addWidget(self.start_button)

        main_layout.addWidget(self.card_controls)

    def toggle_language(self):
        """Switch between English and Thai dynamically"""
        self.current_lang = "th" if self.current_lang == "en" else "en"
        logger.info(f"🌐 Language switched to {self.current_lang.upper()}")
        self.update_localized_text()
        self.update_theme_colors(self.action_combo.currentIndex())
        self.save_window_settings()

    def update_localized_text(self):
        """Update all text in the UI to match the selected language"""
        self.title_label.setText(self.t("app_title"))
        self.lang_button.setText(self.t("lang_name"))
        self.update_theme_button_ui()

        self.label_action_sec.setText(self.t("section_action"))
        self.label_duration_sec.setText(self.t("section_duration"))

        self.tab_timer.setText(self.t("mode_timer"))
        self.tab_clock.setText(self.t("mode_clock"))

        self.lbl_h.setText(self.t("unit_hours"))
        self.lbl_m.setText(self.t("unit_minutes"))
        self.lbl_s.setText(self.t("unit_seconds"))
        self.lbl_date.setText(self.t("unit_date"))
        self.lbl_clock_h.setText(self.t("unit_hours"))
        self.lbl_clock_m.setText(self.t("unit_minutes"))

        self.start_button.setText(self.t("btn_start"))
        self.cancel_button.setText(self.t("btn_cancel"))
        self.clear_button.setText(self.t("btn_clear"))

        # Update action buttons text
        for i, btn in enumerate(self.action_buttons):
            info = ACTION_COLORS[i]
            label = info[f"label_{self.current_lang}"]
            btn.setText(label)

        # Update status if idle
        if not self.is_timer_active:
            self.status_label.setText(self.t("status_ready"))

    def apply_styles(self):
        """Apply sleek Modern Precision Zinc/Slate base stylesheet"""
        if self.current_theme_mode == "light":
            # Eye-Comfort Soft Concrete Light Palette (#D8D8D8 background)
            base_style = f"""
                QMainWindow, QWidget#centralWidget {{
                    background-color: #D8D8D8;
                }}
                QWidget {{
                    color: #18181b;
                    font-family: 'IBM Plex Sans Thai', 'Kanit', 'Segoe UI Variable Display', 'Segoe UI Variable Text', 'Leelawadee UI', 'Segoe UI', -apple-system, sans-serif;
                    font-size: 10pt;
                }}
                QFrame#bentoCard {{
                    background-color: #ffffff;
                    border: 1px solid #c0c0c0;
                    border-radius: 12px;
                }}
                QLabel#quietSectionHeader {{
                    color: #52525b;
                    font-size: 10px;
                    font-weight: 700;
                    letter-spacing: 1px;
                    background: transparent;
                }}
                QLabel#appTitle {{
                    color: #18181b;
                    font-size: 14px;
                    font-weight: 700;
                    background: transparent;
                }}
                QLabel#statusLabel {{
                    color: #52525b;
                    font-size: 11px;
                    background: transparent;
                }}
                QLabel#statusDot {{
                    background-color: #a1a1aa;
                    border-radius: 4px;
                }}
                QLabel#timeUnitLabel {{
                    color: #52525b;
                    font-size: 10px;
                    font-weight: 600;
                    background: transparent;
                }}
                QComboBox, QDateEdit, QDateTimeEdit {{
                    background-color: #ffffff;
                    border: 1px solid #b8b8b8;
                    border-radius: 8px;
                    padding: 5px 10px;
                    color: #18181b;
                    font-size: 12px;
                    font-weight: 500;
                }}
                QComboBox:hover, QDateEdit:hover {{
                    background-color: #ffffff;
                    border-color: #71717a;
                }}
                QComboBox:focus, QDateEdit:focus {{
                    border-color: #0284c7;
                    background-color: #ffffff;
                }}
                QComboBox::drop-down, QDateEdit::drop-down {{
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 24px;
                    border-left: none;
                }}
                QComboBox::down-arrow, QDateEdit::down-arrow {{
                    image: url('{CHEVRON_LIGHT_PATH}');
                    width: 12px;
                    height: 12px;
                    margin-right: 8px;
                }}
                QFrame#segmentedControl {{
                    background-color: #cecece;
                    border: 1px solid #b8b8b8;
                    border-radius: 8px;
                    padding: 2px;
                }}
                QPushButton#segmentedTab {{
                    background-color: transparent;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 14px;
                    color: #52525b;
                    font-size: 11px;
                    font-weight: 600;
                }}
                QPushButton#segmentedTab:checked {{
                    background-color: #ffffff;
                    color: #18181b;
                    border: 1px solid #b8b8b8;
                }}
                QPushButton#segmentedTab:hover:!checked {{
                    color: #18181b;
                }}
                QPushButton#headerButton {{
                    background-color: #ffffff;
                    border: 1px solid #c0c0c0;
                    border-radius: 7px;
                    padding: 4px 10px;
                    color: #3f3f46;
                    font-size: 11px;
                    font-weight: 600;
                }}
                QPushButton#headerButton:hover {{
                    background-color: #f4f4f5;
                    color: #18181b;
                    border-color: #a1a1aa;
                }}
                QPushButton#actionPill {{
                    background-color: #ffffff;
                    border: 1px solid #c0c0c0;
                    border-radius: 8px;
                    color: #3f3f46;
                    padding: 6px 12px;
                }}
                QPushButton#actionPill:hover {{
                    background-color: #f4f4f5;
                    border-color: #a1a1aa;
                    color: #18181b;
                }}
                AnimatedButton#presetChip {{
                    background-color: #ffffff;
                    border: 1px solid #c0c0c0;
                    border-radius: 8px;
                    color: #18181b;
                    padding: 6px 10px;
                }}
                AnimatedButton#presetChip:hover {{
                    background-color: #f4f4f5;
                    border-color: #a1a1aa;
                }}
                QProgressBar {{
                    background-color: #c0c0c0;
                    border: none;
                    border-radius: 1.5px;
                }}
                QProgressBar::chunk {{
                    border-radius: 1.5px;
                }}
            """
        else:  # Dark Mode (Deep Zinc / Slate)
            base_style = f"""
                QMainWindow, QWidget#centralWidget {{
                    background-color: #0d1117;
                }}
                QWidget {{
                    color: #e6edf3;
                    font-family: 'IBM Plex Sans Thai', 'Kanit', 'Segoe UI Variable Display', 'Segoe UI Variable Text', 'Leelawadee UI', 'Segoe UI', -apple-system, sans-serif;
                    font-size: 10pt;
                }}
                QFrame#bentoCard {{
                    background-color: #161b22;
                    border: 1px solid #30363d;
                    border-radius: 12px;
                }}
                QLabel#quietSectionHeader {{
                    color: #8b949e;
                    font-size: 10px;
                    font-weight: 700;
                    letter-spacing: 1px;
                    background: transparent;
                }}
                QLabel#appTitle {{
                    color: #f0f6fc;
                    font-size: 14px;
                    font-weight: 700;
                    background: transparent;
                }}
                QLabel#statusLabel {{
                    color: #8b949e;
                    font-size: 11px;
                    background: transparent;
                }}
                QLabel#statusDot {{
                    background-color: #484f58;
                    border-radius: 4px;
                }}
                QLabel#timeUnitLabel {{
                    color: #8b949e;
                    font-size: 10px;
                    font-weight: 600;
                    background: transparent;
                }}
                QComboBox, QDateEdit, QDateTimeEdit {{
                    background-color: #0d1117;
                    border: 1px solid #30363d;
                    border-radius: 8px;
                    padding: 5px 10px;
                    color: #f0f6fc;
                    font-size: 12px;
                    font-weight: 500;
                }}
                QComboBox:hover, QDateEdit:hover {{
                    background-color: #161b22;
                    border-color: #484f58;
                }}
                QComboBox:focus, QDateEdit:focus {{
                    border-color: #38bdf8;
                }}
                QComboBox::drop-down, QDateEdit::drop-down {{
                    subcontrol-origin: padding;
                    subcontrol-position: top right;
                    width: 24px;
                    border-left: none;
                }}
                QComboBox::down-arrow, QDateEdit::down-arrow {{
                    image: url('{CHEVRON_DARK_PATH}');
                    width: 12px;
                    height: 12px;
                    margin-right: 8px;
                }}
                QFrame#segmentedControl {{
                    background-color: #0d1117;
                    border: 1px solid #30363d;
                    border-radius: 8px;
                    padding: 2px;
                }}
                QPushButton#segmentedTab {{
                    background-color: transparent;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 14px;
                    color: #8b949e;
                    font-size: 11px;
                    font-weight: 600;
                }}
                QPushButton#segmentedTab:checked {{
                    background-color: #21262d;
                    color: #f0f6fc;
                    border: 1px solid #30363d;
                }}
                QPushButton#segmentedTab:hover:!checked {{
                    color: #f0f6fc;
                }}
                QPushButton#headerButton {{
                    background-color: #161b22;
                    border: 1px solid #30363d;
                    border-radius: 7px;
                    padding: 4px 10px;
                    color: #8b949e;
                    font-size: 11px;
                    font-weight: 600;
                }}
                QPushButton#headerButton:hover {{
                    background-color: #21262d;
                    color: #f0f6fc;
                    border-color: #484f58;
                }}
                QPushButton#actionPill {{
                    background-color: #161b22;
                    border: 1px solid #30363d;
                    border-radius: 8px;
                    color: #c9d1d9;
                    padding: 6px 12px;
                }}
                QPushButton#actionPill:hover {{
                    background-color: #21262d;
                    border-color: #484f58;
                    color: #f0f6fc;
                }}
                AnimatedButton#presetChip {{
                    background-color: #161b22;
                    border: 1px solid #30363d;
                    border-radius: 8px;
                    color: #f0f6fc;
                    padding: 6px 10px;
                }}
                AnimatedButton#presetChip:hover {{
                    background-color: #21262d;
                    border-color: #484f58;
                }}
                QProgressBar {{
                    background-color: #21262d;
                    border: none;
                    border-radius: 1.5px;
                }}
                QProgressBar::chunk {{
                    border-radius: 1.5px;
                }}
            """

        self.setStyleSheet(base_style)
        self.update_theme_button_ui()

    def update_theme_colors(self, action_index: int):
        """Update theme accents based on selected action"""
        self.current_theme = ACTION_COLORS.get(action_index, ACTION_COLORS[0])
        primary = self.current_theme["primary"]
        secondary = self.current_theme["secondary"]
        accent = self.current_theme["accent"]

        is_dark = self.current_theme_mode == "dark"
        icon_color_idle = "#c9d1d9" if is_dark else "#52525b"

        # Update Action Buttons UI (Icons and Checked States)
        if hasattr(self, "action_buttons"):
            for idx, btn in enumerate(self.action_buttons):
                info = ACTION_COLORS[idx]
                is_checked = (idx == action_index)
                btn.setChecked(is_checked)
                ic_col = primary if is_checked else icon_color_idle
                btn.setIcon(render_svg_icon(info["icon"], color=ic_col, size=16))

        # Dynamic Stylesheet Injections
        if is_dark:
            countdown_color = primary if self.is_timer_active else "#6e7681"
            status_dot_color = "#10b981" if self.is_timer_active else "#484f58"

            dynamic_style = f"""
                QLabel#countdownLabel {{
                    color: {countdown_color};
                    letter-spacing: 2px;
                    background: transparent;
                }}
                QLabel#statusDot {{
                    background-color: {status_dot_color};
                }}
                QProgressBar#progressBar::chunk {{
                    background-color: {primary};
                }}
                QPushButton#actionPill:checked {{
                    background-color: {self.current_theme['bg_subtle_dark']};
                    border: 1.5px solid {primary};
                    color: #ffffff;
                    font-weight: 700;
                }}
                AnimatedButton#presetChip:hover {{
                    border-color: {primary};
                }}
                QPushButton#startButton {{
                    background-color: {primary};
                    border: 1px solid {primary};
                    border-radius: 8px;
                    color: #ffffff;
                    font-weight: 700;
                    padding: 8px 16px;
                }}
                QPushButton#startButton:hover {{
                    background-color: {secondary};
                    border-color: {secondary};
                }}
                QPushButton#startButton:pressed {{
                    background-color: {accent};
                }}
                QPushButton#startButton:disabled {{
                    background-color: #21262d;
                    color: #484f58;
                    border: 1px solid #30363d;
                }}
                QPushButton#cancelButton {{
                    background-color: rgba(244, 63, 94, 0.1);
                    border: 1px solid rgba(244, 63, 94, 0.25);
                    border-radius: 8px;
                    color: #f43f5e;
                    font-weight: 600;
                    padding: 8px 14px;
                }}
                QPushButton#cancelButton:hover {{
                    background-color: rgba(244, 63, 94, 0.2);
                    border-color: rgba(244, 63, 94, 0.45);
                }}
                QPushButton#cancelButton:disabled {{
                    background-color: transparent;
                    color: #484f58;
                    border: 1px solid #21262d;
                }}
                QPushButton#clearButton {{
                    background-color: #161b22;
                    border: 1px solid #30363d;
                    border-radius: 8px;
                    color: #8b949e;
                    font-weight: 600;
                    padding: 8px 14px;
                }}
                QPushButton#clearButton:hover {{
                    background-color: #21262d;
                    color: #f0f6fc;
                    border-color: #484f58;
                }}
            """
        else:  # Light Mode (#D8D8D8 background)
            countdown_color = primary if self.is_timer_active else "#71717a"
            status_dot_color = "#10b981" if self.is_timer_active else "#a1a1aa"

            dynamic_style = f"""
                QLabel#countdownLabel {{
                    color: {countdown_color};
                    letter-spacing: 2px;
                    background: transparent;
                }}
                QLabel#statusDot {{
                    background-color: {status_dot_color};
                }}
                QProgressBar#progressBar::chunk {{
                    background-color: {primary};
                }}
                QPushButton#actionPill:checked {{
                    background-color: {self.current_theme['bg_subtle_light']};
                    border: 1.5px solid {primary};
                    color: #18181b;
                    font-weight: 700;
                }}
                AnimatedButton#presetChip:hover {{
                    border-color: {primary};
                }}
                QPushButton#startButton {{
                    background-color: {primary};
                    border: 1px solid {primary};
                    border-radius: 8px;
                    color: #ffffff;
                    font-weight: 700;
                    padding: 8px 16px;
                }}
                QPushButton#startButton:hover {{
                    background-color: {secondary};
                    border-color: {secondary};
                }}
                QPushButton#startButton:pressed {{
                    background-color: {accent};
                }}
                QPushButton#startButton:disabled {{
                    background-color: #e4e4e7;
                    color: #a1a1aa;
                    border: 1px solid #c0c0c0;
                }}
                QPushButton#cancelButton {{
                    background-color: rgba(244, 63, 94, 0.08);
                    border: 1px solid rgba(244, 63, 94, 0.25);
                    border-radius: 8px;
                    color: #e11d48;
                    font-weight: 600;
                    padding: 8px 14px;
                }}
                QPushButton#cancelButton:hover {{
                    background-color: rgba(244, 63, 94, 0.16);
                    border-color: rgba(244, 63, 94, 0.4);
                }}
                QPushButton#cancelButton:disabled {{
                    background-color: transparent;
                    color: #a1a1aa;
                    border: 1px solid #c0c0c0;
                }}
                QPushButton#clearButton {{
                    background-color: #ffffff;
                    border: 1px solid #c0c0c0;
                    border-radius: 8px;
                    color: #3f3f46;
                    font-weight: 600;
                    padding: 8px 14px;
                }}
                QPushButton#clearButton:hover {{
                    background-color: #f4f4f5;
                    color: #18181b;
                    border-color: #a1a1aa;
                }}
            """

        current_style = self.styleSheet()
        if "/* DYNAMIC */" in current_style:
            base = current_style.split("/* DYNAMIC */")[0]
        else:
            base = current_style

        self.setStyleSheet(base + "/* DYNAMIC */" + dynamic_style)

    def on_action_changed(self, index):
        """Handle action change and synchronize pills and theme colors"""
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
        self.current_theme_mode = "light" if self.current_theme_mode == "dark" else "dark"
        logger.info(f"🌓 Theme toggled to {self.current_theme_mode}")
        self.apply_styles()
        self.update_theme_colors(self.action_combo.currentIndex())
        self.save_window_settings()

    def update_theme_button_ui(self):
        """Update theme button label and icon based on current theme"""
        if self.current_theme_mode == "light":
            self.theme_button.setText(self.t("theme_dark"))
            self.theme_button.setIcon(render_svg_icon("moon", color="#52525b", size=14))
        else:
            self.theme_button.setText(self.t("theme_light"))
            self.theme_button.setIcon(render_svg_icon("sun", color="#fbbf24", size=14))

    def start_preset_timer(self, value, unit):
        """Start timer from preset chip"""
        if self.is_timer_active:
            self.show_toast(self.t("toast_already_active"), "warning")
            return

        action_index = self.action_combo.currentIndex()
        if action_index >= 2:
            self.show_toast(self.t("toast_preset_limit"), "warning")
            self.action_combo.setCurrentIndex(0)
            return

        info = ACTION_COLORS[action_index]
        action_name = info[f"label_{self.current_lang}"]

        if unit == "minutes":
            self.target_shutdown_time = datetime.now() + timedelta(minutes=value)
            time_str = f"{value}m" if self.current_lang == "en" else f"{value} นาที"
            self.tab_timer.setChecked(True)
            self.hours_combo.setCurrentIndex(0)
            self.minutes_combo.setCurrentIndex(min(value, 59))
            self.seconds_combo.setCurrentIndex(0)
        else:
            self.target_shutdown_time = datetime.now() + timedelta(hours=value)
            time_str = f"{value}h" if self.current_lang == "en" else f"{value} ชั่วโมง"
            self.tab_timer.setChecked(True)
            self.hours_combo.setCurrentIndex(min(value, 24))
            self.minutes_combo.setCurrentIndex(0)
            self.seconds_combo.setCurrentIndex(0)

        reply = QMessageBox.question(
            self,
            self.t("confirm_title"),
            self.t("confirm_timer_desc", action=action_name, time=time_str),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.No:
            return

        try:
            total_seconds = int((self.target_shutdown_time - datetime.now()).total_seconds())
            self.total_seconds = total_seconds
            self.remaining_seconds = total_seconds

            try:
                subprocess.run(["shutdown", "/a"], capture_output=True)
            except Exception:
                pass

            command = "/r" if action_index == 1 else "/s"
            logger.info(f"⚡ [Preset] {action_name} in {time_str} ({total_seconds}s) → {self.target_shutdown_time.strftime('%H:%M:%S')}")
            subprocess.run(["shutdown", command, "/t", str(total_seconds)], check=True)

            self.is_timer_active = True
            time_display = self.target_shutdown_time.strftime('%H:%M:%S')
            self.status_label.setText(self.t("status_active", action=action_name, time=time_display))
            self.cancel_button.setEnabled(True)
            self.start_button.setEnabled(False)
            self.countdown_timer.start(1000)

            self.update_theme_colors(action_index)
            self.show_toast(self.t("toast_scheduled", action=action_name, time=time_str), "success")
            self.save_settings()

        except Exception as e:
            self.show_toast(self.t("toast_cannot_schedule", error=str(e)), "error")

    def start_timer(self):
        """Start shutdown/restart timer"""
        if self.is_timer_active:
            self.show_toast(self.t("toast_already_active"), "warning")
            return

        action_index = self.action_combo.currentIndex()
        action_map = {
            0: ("/s"),
            1: ("/r"),
            2: ("sleep"),
            3: ("hibernate"),
        }
        command_type = action_map.get(action_index, "/s")
        info = ACTION_COLORS[action_index]
        action_name = info[f"label_{self.current_lang}"]

        if action_index >= 2:
            self._execute_sleep_hibernate(action_name, command_type)
            return

        reply = QMessageBox.question(
            self,
            self.t("confirm_title"),
            self.t("confirm_clock_desc", action=action_name, time=self.target_clock_datetime.toString("HH:mm")) if self.mode_button_group.checkedId() == 1 else self.t("confirm_timer_desc", action=action_name, time=f"{self.hours_combo.currentIndex()}h {self.minutes_combo.currentIndex()}m {self.seconds_combo.currentIndex()}s"),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.No:
            return

        try:
            mode_index = self.mode_button_group.checkedId()
            if mode_index == 0:  # Timer mode
                hours = self.hours_combo.currentIndex()
                minutes = self.minutes_combo.currentIndex()
                seconds = self.seconds_combo.currentIndex()
                if hours == 0 and minutes == 0 and seconds == 0:
                    self.show_toast(self.t("toast_zero_duration"), "warning")
                    return
                self.target_shutdown_time = datetime.now() + timedelta(
                    hours=hours, minutes=minutes, seconds=seconds
                )
            else:  # Clock mode
                target_dt = self.target_clock_datetime
                self.target_shutdown_time = target_dt.toPython()

            if self.target_shutdown_time <= datetime.now():
                self.show_toast(self.t("toast_future_time"), "warning")
                return

            max_duration = timedelta(hours=72)
            if self.target_shutdown_time - datetime.now() > max_duration:
                self.show_toast(self.t("toast_max_duration"), "warning")
                return

            total_seconds = int((self.target_shutdown_time - datetime.now()).total_seconds())
            self.total_seconds = total_seconds
            self.remaining_seconds = total_seconds

            try:
                subprocess.run(["shutdown", "/a"], capture_output=True)
            except Exception:
                pass

            logger.info(f"⏱️ [Timer] {action_name} in {total_seconds}s → {self.target_shutdown_time.strftime('%H:%M:%S')}")
            subprocess.run(["shutdown", command_type, "/t", str(total_seconds)], check=True)

            self.is_timer_active = True
            time_display = self.target_shutdown_time.strftime('%H:%M:%S')
            self.status_label.setText(self.t("status_active", action=action_name, time=time_display))
            self.cancel_button.setEnabled(True)
            self.start_button.setEnabled(False)
            self.countdown_timer.start(1000)

            self.update_theme_colors(action_index)
            self.show_toast(self.t("toast_scheduled", action=action_name, time=time_display), "success")
            self.save_settings()

        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Shutdown command failed: {e}")
            self.show_toast(self.t("toast_cannot_schedule", error=f"Code {e.returncode}"), "error")
        except Exception as e:
            logger.error(f"💥 Unexpected error: {e}")
            self.show_toast(self.t("toast_cannot_schedule", error=str(e)), "error")

    def _execute_sleep_hibernate(self, action_name, command_type):
        """Execute Sleep or Hibernate immediately"""
        reply = QMessageBox.question(
            self,
            self.t("confirm_title"),
            self.t("confirm_exec_desc", action=action_name),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.No:
            return

        try:
            logger.info(f"Executing {action_name} immediately...")
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

            self.status_label.setText(self.t("status_executing", action=action_name))
            self.show_toast(self.t("status_executing", action=action_name), "info")
        except Exception as e:
            self.show_toast(self.t("toast_cannot_execute", action=action_name, error=str(e)), "error")

    def cancel_timer(self, confirm=True):
        """Cancel active timer"""
        if not self.is_timer_active:
            if confirm:
                self.show_toast(self.t("toast_no_active"), "info")
            return

        if confirm:
            reply = QMessageBox.question(
                self,
                self.t("confirm_cancel_title"),
                self.t("confirm_cancel_desc"),
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply != QMessageBox.Yes:
                return

        try:
            logger.info("🛑 Cancelling scheduled shutdown...")
            subprocess.run(["shutdown", "/a"], check=True)
            self.countdown_timer.stop()
            self.reset_ui_state()
            self.is_timer_active = False
            self.status_label.setText(self.t("status_cancelled"))
            logger.info("✅ Timer cancelled successfully")
            if confirm:
                self.show_toast(self.t("toast_cancelled"), "success")
            self.save_settings()
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to cancel shutdown: {e}")
            if confirm:
                if e.returncode == 1116:
                    self.show_toast(self.t("toast_no_shutdown_to_cancel"), "info")
                else:
                    self.show_toast(self.t("toast_cannot_cancel", error=f"Code {e.returncode}"), "error")
            self.reset_ui_state()
        except Exception as e:
            logger.error(f"💥 Unexpected error during cancel: {e}")
            if confirm:
                self.show_toast(self.t("toast_cannot_cancel", error=str(e)), "error")
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
            action_index = self.action_combo.currentIndex()
            info = ACTION_COLORS[action_index]
            action_name = info[f"label_{self.current_lang}"]
            self.status_label.setText(self.t("status_executing", action=action_name))
            self._delete_config_file()
            self.reset_ui_state()
        else:
            total_seconds = int(remaining.total_seconds())
            self.remaining_seconds = max(0, total_seconds)
            hours, remainder = divmod(total_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.countdown_label.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

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
        self.tab_timer.setChecked(True)
        self.action_combo.setCurrentIndex(0)
        self.status_label.setText(self.t("status_ready"))
        self.countdown_label.setText("00:00:00")
        self.progress_bar.setValue(0)
        self._delete_config_file()
        logger.info("🧹 All fields cleared, config deleted")
        self.show_toast(self.t("toast_all_reset"), "info")
        self.update_theme_colors(0)

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
        self.status_label.setText(self.t("status_ready"))
        self.countdown_label.setText("00:00:00")
        self.update_theme_colors(self.action_combo.currentIndex())

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
            logger.warning(f"⚠️ Could not delete config file: {e}")

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
            self.tab_timer.setChecked(True)
            return

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)

            self.action_combo.setCurrentIndex(settings.get("action", 0))

            mode_id = settings.get("mode", 0)
            btn_to_check = self.mode_button_group.button(mode_id)
            if btn_to_check:
                btn_to_check.setChecked(True)
            else:
                self.tab_timer.setChecked(True)

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
        """Save window position, theme and language to JSON file"""
        settings = {
            "width": 520,
            "height": 560,
            "x": self.x(),
            "y": self.y(),
            "theme": self.current_theme_mode,
            "language": self.current_lang,
        }
        try:
            temp_path = WINDOW_CONFIG_FILE + ".tmp"
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
            os.replace(temp_path, WINDOW_CONFIG_FILE)
            logger.info("💾 Window settings saved")
        except Exception as e:
            logger.error(f"💾❌ Could not save window settings: {e}")

    def load_window_settings(self):
        """Load window position, theme and language from JSON file"""
        if not os.path.exists(WINDOW_CONFIG_FILE):
            return
        try:
            with open(WINDOW_CONFIG_FILE, "r", encoding="utf-8") as f:
                settings = json.load(f)

            x = settings.get("x")
            y = settings.get("y")
            if x is not None and y is not None:
                self.move(x, y)
                logger.info(f"📂 Window position ({x}, {y}) restored")

            self.current_theme_mode = settings.get("theme", "dark")
            self.current_lang = settings.get("language", "en")
            logger.info(f"📂 Theme '{self.current_theme_mode}', Language '{self.current_lang}' loaded")
        except Exception as e:
            logger.error(f"📂❌ Could not load window settings: {e}")


if __name__ == "__main__":
    import signal

    app = QApplication(sys.argv)
    QLocale.setDefault(QLocale.C)

    def handle_signal(sig, frame):
        if 'window' in globals() and window.is_timer_active:
            window.cancel_timer(confirm=False)
        app.quit()

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGBREAK, handle_signal)

    if sys.platform == "win32":
        import ctypes
        myappid = "mycompany.myproduct.subproduct.version"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    window = ShutdownTimerApp()
    window.show()
    sys.exit(app.exec())
