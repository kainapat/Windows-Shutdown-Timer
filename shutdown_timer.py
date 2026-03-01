# -*- coding: utf-8 -*-

import sys
import os
import json
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
    QTimeEdit,
    QSpinBox,
    QMessageBox,
    QRadioButton,
    QButtonGroup,
    QProgressBar,
    QGroupBox,
    QGridLayout,
)
from PySide6.QtCore import (
    QTimer,
    QDateTime,
    Qt,
    QLocale,
    QDate,
    QPropertyAnimation,
    QEasingCurve,
    QSize,
)
from PySide6.QtGui import QFont, QIcon

# --- คำสั่งสำหรับการแพ็กเป็น .exe ด้วย PyInstaller ---
# 1. ติดตั้ง PyInstaller: pip install pyinstaller
# 2. รันคำสั่งนี้ใน Terminal ที่โฟลเดอร์เดียวกับไฟล์ .py:
# pyinstaller --onefile --windowed --name="Windows Shutdown Timer" --icon=icon.ico shutdown_timer.py

CONFIG_FILE = "timer_config.json"


class ShutdownTimerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Windows Shutdown/Restart Timer")
        self.setMinimumSize(500, 550)
        self.resize(500, 600)

        # ตัวแปรสำหรับจัดการสถานะ
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.target_shutdown_time = None
        self.is_timer_active = False
        self.total_seconds = 0
        self.remaining_seconds = 0

        # Animation for countdown
        self.countdown_animation = None

        self.init_ui()
        self.load_settings()
        self.apply_styles()

    def init_ui(self):
        """สร้างและจัดวาง Widgets ต่างๆ บนหน้าต่าง"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # --- Quick Presets Section ---
        presets_group = QGroupBox("⚡ Quick Presets (กดเร็ว)")
        presets_layout = QGridLayout(presets_group)

        self.preset_15min = QPushButton("15 นาที")
        self.preset_30min = QPushButton("30 นาที")
        self.preset_1hour = QPushButton("1 ชั่วโมง")
        self.preset_2hour = QPushButton("2 ชั่วโมง")

        self.preset_15min.clicked.connect(
            lambda: self.start_preset_timer(15, "minutes")
        )
        self.preset_30min.clicked.connect(
            lambda: self.start_preset_timer(30, "minutes")
        )
        self.preset_1hour.clicked.connect(lambda: self.start_preset_timer(1, "hours"))
        self.preset_2hour.clicked.connect(lambda: self.start_preset_timer(2, "hours"))

        presets_layout.addWidget(self.preset_15min, 0, 0)
        presets_layout.addWidget(self.preset_30min, 0, 1)
        presets_layout.addWidget(self.preset_1hour, 0, 2)
        presets_layout.addWidget(self.preset_2hour, 0, 3)

        main_layout.addWidget(presets_group)

        # --- ส่วนเลือกการกระทำ ---
        action_layout = QHBoxLayout()
        self.action_label = QLabel("เลือกการกระทำ:")
        self.action_combo = QComboBox()
        self.action_combo.addItems(
            [
                "ปิดเครื่อง (Shutdown)",
                "รีสตาร์ท (Restart)",
                "พักเครื่อง (Sleep)",
                "จำศีล (Hibernate)",
            ]
        )
        action_layout.addWidget(self.action_label)
        action_layout.addWidget(self.action_combo)
        main_layout.addLayout(action_layout)

        # --- ส่วนเลือกโหมดการตั้งเวลา (ใช้ Radio Buttons) ---
        mode_group_layout = QVBoxLayout()
        self.mode_label = QLabel("เลือกโหมด:")
        mode_group_layout.addWidget(self.mode_label)

        self.mode_button_group = QButtonGroup(self)

        self.radio_datetime = QRadioButton("ตั้งเวลาแบบระบุวันที่/เวลา")
        self.radio_hours = QRadioButton("ตั้งเวลาแบบนับถอยหลัง (ชั่วโมง)")
        self.radio_minutes = QRadioButton("ตั้งเวลาแบบนับถอยหลัง (นาที)")
        self.radio_seconds = QRadioButton("ตั้งเวลาแบบนับถอยหลัง (วินาที)")

        self.mode_button_group.addButton(self.radio_datetime, 0)
        self.mode_button_group.addButton(self.radio_hours, 1)
        self.mode_button_group.addButton(self.radio_minutes, 2)
        self.mode_button_group.addButton(self.radio_seconds, 3)

        self.mode_button_group.idToggled.connect(self.on_mode_toggled)

        mode_group_layout.addWidget(self.radio_datetime)
        mode_group_layout.addWidget(self.radio_hours)
        mode_group_layout.addWidget(self.radio_minutes)
        mode_group_layout.addWidget(self.radio_seconds)

        main_layout.addLayout(mode_group_layout)

        # --- ส่วนกรอกข้อมูลเวลา ---
        # ส่วนเลือกวัน/เวลาแบบเจาะจง (Datetime mode)
        self.datetime_container = QWidget()
        self.datetime_layout = QHBoxLayout(self.datetime_container)
        self.datetime_layout.setContentsMargins(0, 0, 0, 0)

        self.date_edit = QDateTimeEdit()
        self.date_edit.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self.date_edit.setDisplayFormat("ddd d MMM yyyy")
        self.date_edit.setCalendarPopup(True)

        # Dropdown เลือกชั่วโมง (00-23)
        self.time_hours_combo = QComboBox()
        self.time_hours_combo.addItems([f"{i:02d}" for i in range(0, 24)])
        self.time_hours_combo.setCurrentText(
            f"{QDateTime.currentDateTime().addSecs(3600).toString('HH')}"
        )
        self.time_hours_combo.setMaximumWidth(60)

        # Dropdown เลือกนาที (00-59)
        self.time_minutes_combo = QComboBox()
        self.time_minutes_combo.addItems([f"{i:02d}" for i in range(0, 60)])
        self.time_minutes_combo.setCurrentText(
            f"{QDateTime.currentDateTime().addSecs(3600).toString('mm')}"
        )
        self.time_minutes_combo.setMaximumWidth(60)

        self.datetime_layout.addWidget(QLabel("วันที่:"))
        self.datetime_layout.addWidget(self.date_edit)
        self.datetime_layout.addWidget(QLabel("เวลา:"))
        self.datetime_layout.addWidget(self.time_hours_combo)
        self.datetime_layout.addWidget(QLabel(":"))
        self.datetime_layout.addWidget(self.time_minutes_combo)

        # สร้าง Dropdown สำหรับเลือกเวลาแทน Spinbox
        self.hours_combo = QComboBox()
        self.hours_combo.addItems([f"{i} ชั่วโมง" for i in range(1, 25)])  # 1-24 ชั่วโมง
        self.hours_combo.hide()

        self.minutes_combo = QComboBox()
        self.minutes_combo.addItems([f"{i} นาที" for i in range(1, 61)])  # 1-60 นาที
        self.minutes_combo.hide()

        self.seconds_combo = QComboBox()
        self.seconds_combo.addItems(
            [f"{i} วินาที" for i in range(10, 301, 10)]
        )  # 10-300 วินาที (ทีละ 10 วินาที)
        self.seconds_combo.hide()

        main_layout.addWidget(self.datetime_container)
        main_layout.addWidget(self.hours_combo)
        main_layout.addWidget(self.minutes_combo)
        main_layout.addWidget(self.seconds_combo)

        # --- ส่วนแสดงสถานะและเวลาที่เหลือ ---
        status_group = QGroupBox("สถานะ")
        status_layout = QVBoxLayout(status_group)

        self.status_label = QLabel("สถานะ: ยังไม่มีการตั้งเวลา")
        self.status_label.setAlignment(Qt.AlignCenter)

        self.countdown_label = QLabel("--:--:--")
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setFont(QFont("Arial", 32, QFont.Bold))

        # Progress Bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%p%")

        status_layout.addWidget(self.status_label)
        status_layout.addWidget(self.countdown_label)
        status_layout.addWidget(self.progress_bar)

        main_layout.addWidget(status_group)

        # --- ส่วนปุ่มควบคุม ---
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("เริ่มตั้งเวลา")
        self.cancel_button = QPushButton("ยกเลิก")
        self.clear_button = QPushButton("ล้างค่า")

        self.cancel_button.setEnabled(False)

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

    def apply_styles(self):
        """กำหนด Theme สี Dark Blue/Navy ให้กับแอปพลิเคชัน"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
            }
            QWidget {
                background-color: #1e1e2e;
                color: #cdd6f4;
                font-family: 'Segoe UI', 'Microsoft Sans Serif', sans-serif;
                font-size: 12pt;
            }
            QGroupBox {
                border: 2px solid #45475a;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
                color: #89b4fa;
            }
            QLabel {
                color: #cdd6f4;
                background-color: transparent;
            }
            QComboBox, QDateTimeEdit, QTimeEdit {
                background-color: #313244;
                border: 1px solid #45475a;
                border-radius: 8px;
                padding: 5px 10px;
                color: #cdd6f4;
                min-width: 80px;
            }
            QComboBox::drop-down, QDateTimeEdit::drop-down, QTimeEdit::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow, QDateTimeEdit::down-arrow, QTimeEdit::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #89b4fa;
            }
            QRadioButton {
                color: #cdd6f4;
                spacing: 10px;
                font-size: 11pt;
            }
            QRadioButton::indicator {
                width: 18px;
                height: 18px;
                border-radius: 9px;
                border: 2px solid #89b4fa;
                background-color: #1e1e2e;
            }
            QRadioButton::indicator:checked {
                background-color: #89b4fa;
                border: 2px solid #89b4fa;
            }
            QRadioButton::indicator:hover {
                border-color: #b4befe;
            }
            QPushButton {
                background-color: #45475a;
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #585b70;
            }
            QPushButton:pressed {
                background-color: #6c7086;
            }
            QPushButton#startButton {
                background-color: #89b4fa;
                color: #1e1e2e;
            }
            QPushButton#startButton:hover {
                background-color: #b4befe;
            }
            QPushButton#cancelButton {
                background-color: #f38ba8;
                color: #1e1e2e;
            }
            QPushButton#cancelButton:hover {
                background-color: #eba0ac;
            }
            QPushButton#cancelButton:disabled {
                background-color: #45475a;
                color: #6c7086;
            }
            QPushButton#clearButton {
                background-color: #a6adc8;
                color: #1e1e2e;
            }
            QPushButton#clearButton:hover {
                background-color: #cdd6f4;
            }
            QProgressBar {
                border: 2px solid #45475a;
                border-radius: 8px;
                text-align: center;
                background-color: #313244;
                height: 25px;
            }
            QProgressBar::chunk {
                background-color: #89b4fa;
                border-radius: 6px;
            }
        """)
        self.start_button.setObjectName("startButton")
        self.cancel_button.setObjectName("cancelButton")
        self.clear_button.setObjectName("clearButton")

    def on_mode_toggled(self, id, checked):
        """สลับการแสดงผล Widget ตาม Radio Button ที่เลือก"""
        if not checked:
            return

        self.datetime_container.hide()
        self.hours_combo.hide()
        self.minutes_combo.hide()
        self.seconds_combo.hide()

        if id == 0:
            self.datetime_container.show()
        elif id == 1:
            self.hours_combo.show()
        elif id == 2:
            self.minutes_combo.show()
        else:  # id == 3
            self.seconds_combo.show()

    def start_preset_timer(self, value, unit):
        """เริ่มตั้งเวลาแบบ Preset ทันที"""
        if self.is_timer_active:
            QMessageBox.warning(self, "คำเตือน", "มีการตั้งเวลาอยู่แล้ว กรุณายกเลิกก่อนตั้งค่าใหม่")
            return

        # ดึงการกระทำที่เลือก (shutdown หรือ restart เท่านั้นสำหรับ preset)
        action_index = self.action_combo.currentIndex()
        if action_index >= 2:  # Sleep หรือ Hibernate
            QMessageBox.warning(
                self, "คำเตือน", "Quick Presets รองรับเฉพาะ Shutdown และ Restart"
            )
            self.action_combo.setCurrentIndex(0)
            return

        is_restart = action_index == 1
        action_text = "รีสตาร์ท" if is_restart else "ปิดเครื่อง"

        # คำนวณเวลา
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
            subprocess.run(["shutdown", command, "/t", str(total_seconds)], check=True)

            self.is_timer_active = True
            self.status_label.setText(f"สถานะ: จะ{action_text}ในอีก {time_str}")
            self.cancel_button.setEnabled(True)
            self.start_button.setEnabled(False)
            self.countdown_timer.start(1000)

            self.save_settings()

        except Exception as e:
            QMessageBox.critical(self, "ข้อผิดพลาด", f"ไม่สามารถตั้งเวลาได้: {e}")

    def start_timer(self):
        """ฟังก์ชันเริ่มตั้งเวลาปิดเครื่องหรือรีสตาร์ท"""
        if self.is_timer_active:
            QMessageBox.warning(self, "คำเตือน", "มีการตั้งเวลาอยู่แล้ว กรุณายกเลิกก่อนตั้งค่าใหม่")
            return

        action_index = self.action_combo.currentIndex()
        action_map = {
            0: ("ปิดเครื่อง", "/s"),
            1: ("รีสตาร์ท", "/r"),
            2: ("พักเครื่อง", "sleep"),
            3: ("จำศีล", "hibernate"),
        }
        action_text, command_type = action_map.get(action_index, ("ปิดเครื่อง", "/s"))

        # สำหรับ Sleep/Hibernate ไม่ต้องยืนยันมาก
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
                # ดึงค่าจาก Dropdown แล้วแปลงเป็นตัวเลข
                hours = int(self.hours_combo.currentText().split()[0])
                self.target_shutdown_time = datetime.now() + timedelta(hours=hours)
            elif mode_index == 2:
                minutes = int(self.minutes_combo.currentText().split()[0])
                self.target_shutdown_time = datetime.now() + timedelta(minutes=minutes)
            else:  # mode_index == 3
                seconds = int(self.seconds_combo.currentText().split()[0])
                self.target_shutdown_time = datetime.now() + timedelta(seconds=seconds)

            if self.target_shutdown_time <= datetime.now():
                QMessageBox.warning(self, "ข้อผิดพลาด", "กรุณาตั้งเวลาในอนาคต")
                return

            total_seconds = int(
                (self.target_shutdown_time - datetime.now()).total_seconds()
            )
            self.total_seconds = total_seconds
            self.remaining_seconds = total_seconds

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

            self.save_settings()

        except Exception as e:
            QMessageBox.critical(self, "ข้อผิดพลาด", f"ไม่สามารถตั้งเวลาได้: {e}")

    def _execute_sleep_hibernate(self, action_text, command_type):
        """ทำการ Sleep หรือ Hibernate ทันที"""
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
                # Sleep command
                subprocess.run(
                    ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
                    check=True,
                )
            else:  # hibernate
                # Hibernate command
                subprocess.run(
                    ["rundll32.exe", "powrprof.dll,SetSuspendState", "1,1,0"],
                    check=True,
                )

            self.status_label.setText(f"สถานะ: กำลัง{action_text}...")
        except Exception as e:
            QMessageBox.critical(self, "ข้อผิดพลาด", f"ไม่สามารถ{action_text}ได้: {e}")

    def cancel_timer(self):
        """ฟังก์ชันยกเลิกการตั้งเวลา"""
        if not self.is_timer_active:
            QMessageBox.information(self, "ข้อมูล", "ไม่มีการตั้งเวลาปิดเครื่อง/รีสตาร์ทอยู่ในขณะนี้")
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
                subprocess.run(["shutdown", "/a"], check=True)
                self.reset_ui_state()
                self.status_label.setText("สถานะ: ยกเลิกการตั้งเวลาแล้ว")
            except Exception as e:
                QMessageBox.critical(
                    self, "ข้อผิดพลาด", f"ไม่สามารถยกเลิกได้: {e}\n(อาจจะไม่มีการตั้งเวลาอยู่จริง)"
                )
                self.reset_ui_state()

    def update_countdown(self):
        """อัปเดตเวลานับถอยหลังทุกวินาที"""
        if not self.is_timer_active or not self.target_shutdown_time:
            return

        remaining = self.target_shutdown_time - datetime.now()

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
            self.remaining_seconds = total_seconds
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
                self.progress_bar.setValue(progress)

    def clear_fields(self):
        """ล้างค่าในช่องกรอกข้อมูลและลบไฟล์ config"""
        self.date_edit.setDateTime(QDateTime.currentDateTime().addSecs(3600))
        self.time_hours_combo.setCurrentText(
            QDateTime.currentDateTime().addSecs(3600).toString("HH")
        )
        self.time_minutes_combo.setCurrentText(
            QDateTime.currentDateTime().addSecs(3600).toString("mm")
        )
        self.hours_combo.setCurrentIndex(0)  # รีเซ็ตเป็นค่าแรก
        self.minutes_combo.setCurrentIndex(0)
        self.seconds_combo.setCurrentIndex(0)
        self.action_combo.setCurrentIndex(0)
        self.status_label.setText("สถานะ: ยังไม่มีการตั้งเวลา")
        self.countdown_label.setText("--:--:--")
        self.progress_bar.setValue(0)
        self._delete_config_file()

    def reset_ui_state(self):
        """รีเซ็ตสถานะ UI หลังจากนับถอยหลังเสร็จสิ้น"""
        self.is_timer_active = False
        self.countdown_timer.stop()
        self.target_shutdown_time = None
        self.total_seconds = 0
        self.remaining_seconds = 0
        self.progress_bar.setValue(0)
        self.cancel_button.setEnabled(False)
        self.start_button.setEnabled(True)

    def closeEvent(self, event):
        """Event ที่เรียกเมื่อปิดโปรแกรม"""
        self._delete_config_file()
        super().closeEvent(event)

    def _delete_config_file(self):
        """ฟังก์ชันสำหรับลบไฟล์การตั้งค่าอย่างปลอดภัย"""
        try:
            if os.path.exists(CONFIG_FILE):
                os.remove(CONFIG_FILE)
        except Exception as e:
            print(f"Could not delete config file: {e}")

    def save_settings(self):
        """บันทึกการตั้งค่าล่าสุดลงไฟล์ JSON"""
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
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(settings, f, indent=4)
        except Exception as e:
            print(f"Could not save settings: {e}")

    def load_settings(self):
        """โหลดการตั้งค่าจากไฟล์ JSON"""
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

            # โหลดค่าวันที่
            date_str = settings.get("date")
            if date_str:
                self.date_edit.setDate(QDate.fromString(date_str, Qt.ISODate))

            # โหลดค่าเวลา
            time_str = settings.get("time")
            if time_str:
                time_parts = time_str.split(":")
                self.time_hours_combo.setCurrentText(time_parts[0])
                self.time_minutes_combo.setCurrentText(time_parts[1])

            self.hours_combo.setCurrentIndex(settings.get("hours", 0))
            self.minutes_combo.setCurrentIndex(settings.get("minutes", 0))
            self.seconds_combo.setCurrentIndex(settings.get("seconds", 0))

        except Exception as e:
            print(f"Could not load settings: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # ตั้งค่าให้แสดงตัวเลขเป็นอาราบิกเสมอ
    QLocale.setDefault(QLocale.C)

    if sys.platform == "win32":
        import ctypes

        myappid = "mycompany.myproduct.subproduct.version"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    window = ShutdownTimerApp()
    window.show()
    sys.exit(app.exec())
