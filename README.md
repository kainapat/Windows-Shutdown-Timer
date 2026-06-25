# Windows Shutdown Timer

โปรแกรมตั้งเวลาปิดเครื่อง รีสตาร์ท พักเครื่อง และจำศีลคอมพิวเตอร์ Windows พัฒนาด้วย Python และ PySide6 มาพร้อมอินเทอร์เฟซสไตล์มินิมอล/โมเดิร์นที่รองรับการปรับขนาดและจดจำตำแหน่งหน้าต่างอัตโนมัติ

A lightweight, reliable Windows shutdown/restart/sleep/hibernate timer application built with Python and PySide6.

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/PySide6-6.4+-green.svg)](https://doc.qt.io/qtforpython-6/)
[![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## ฟีเจอร์หลัก (Key Features)

### 1. โหมดการทำงานครอบคลุม (Operation Modes)
- **Shutdown**: ปิดเครื่องคอมพิวเตอร์
- **Restart**: เริ่มระบบใหม่
- **Sleep**: พักเครื่อง (ใช้พลังงานต่ำ)
- **Hibernate**: จำศีล (เซฟสถานะงานลงดิสก์แล้วดับเครื่อง)

### 2. การตั้งเวลาที่ยืดหยุ่น (Scheduling Options)
- **Quick Presets**: ปุ่มลัดตั้งเวลาด่วน (15 นาที, 30 นาที, 1 ชั่วโมง, 2 ชั่วโมง)
- **Specific Time**: ระบุวันและเวลาที่เจาะจงผ่านปฏิทิน
- **Countdown**: นับถอยหลังระบุละเอียดเป็น ชั่วโมง, นาที หรือวินาที (สูงสุด 24 ชั่วโมง)

### 3. อินเทอร์เฟซและการแสดงผล (UI/UX Design)
- **Resizable & Sticky Window**: หน้าต่างปรับขนาดได้อย่างอิสระ (ขั้นต่ำ 600x680px) และจดจำขนาด/ตำแหน่งการวางบนหน้าจอล่าสุดเมื่อเปิดใช้งานครั้งถัดไป
- **Monospace Countdown**: ตัวนับเวลาถอยหลังแบบเรียลไทม์ที่แสดงผลด้วยฟอนต์ Monospace เพื่อป้องกันตัวเลขขยับตัวไปมาระหว่างเปลี่ยนวิ
- **Dynamic Themes**: เปลี่ยนโทนสีของโปรแกรม (แดง, ส้ม, น้ำเงิน, ม่วง) ตามประเภทของการกระทำที่เลือกโดยอัตโนมัติ
- **Toast Notifications**: ระบบแจ้งเตือนข้อความบนตัวโปรแกรม ทำงานรวดเร็ว ไม่ทับซ้อนกัน และไม่มีปัญหา Memory Leak

### 4. ความปลอดภัยและความเสถียร (Safety & Performance)
- **Atomic Writes**: บันทึกการตั้งค่าลงไฟล์ `timer_config.json` และ `window_config.json` แบบปลอดภัย ป้องกันไฟล์เสียหายเมื่อแอปถูกปิดกะทันหัน
- **Auto-Cancel**: ยกเลิกการตั้งเวลาคำสั่งเดิมใน Windows อัตโนมัติก่อนตั้งค่าใหม่ เพื่อป้องกันคำสั่งชนกัน
- **Graceful Exit**: ดักจับการปิดโปรแกรมหรือการกด `Ctrl+C` / `Ctrl+Break` ใน Terminal เพื่อเคลียร์สถานะอย่างถูกต้องก่อนปิดระบบ

---

## ความต้องการของระบบ (System Requirements)

- **OS**: Windows 7 / 8 / 10 / 11
- **Python**: 3.12 ขึ้นไป (กรณีรันจาก Source Code)
- **Dependencies**:
  - `PySide6 >= 6.4.0`

---

## การติดตั้งและการใช้งาน (Installation & Usage)

### สำหรับผู้ใช้ทั่วไป (ดาวน์โหลดไฟล์ .exe)
1. ดาวน์โหลดไฟล์เวอร์ชันล่าสุดจากหน้า [Releases](../../releases) (ไฟล์ `.exe` แบบ Standalone)
2. ดับเบิ้ลคลิกเพื่อเปิดใช้งานได้ทันทีโดยไม่ต้องติดตั้ง Python หรือไลบรารี่เพิ่มเติม

### สำหรับนักพัฒนา (รันจาก Source Code)
1. **Clone repository และเปิดโฟลเดอร์โครงการ**:
   ```bash
   git clone https://github.com/kainapat/Windows-Shutdown-Timer.git
   cd Windows-Shutdown-Timer
   ```

2. **ติดตั้งไลบรารี่ที่จำเป็น**:
   ```bash
   pip install -r requirements.txt
   ```

3. **สั่งรันแอปพลิเคชัน**:
   ```bash
   python shutdown_timer.py
   ```

---

## การสร้างไฟล์ .exe (Building Executable)

หากต้องการแพ็กโปรแกรมเป็นไฟล์ `.exe` เดี่ยวสำหรับใช้งานทั่วไป สามารถทำได้โดยใช้ PyInstaller:

1. **ติดตั้ง PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **รันคำสั่ง Build**:
   ```bash
   pyinstaller --onefile --windowed --name="Windows Shutdown Timer" --icon=icon.ico shutdown_timer.py
   ```

3. ไฟล์ติดตั้งสำเร็จรูปจะอยู่ในโฟลเดอร์ `dist/Windows Shutdown Timer.exe`

---

## โครงสร้างโครงการ (Project Structure)

```
Windows Shutdown Timer/
├── shutdown_timer.py          # ซอร์สโค้ดหลักของแอปพลิเคชัน
├── requirements.txt           # รายการไลบรารี่ที่โปรแกรมต้องการ
├── icon.ico                   # ไอคอนหลักของแอปพลิเคชัน
├── off.png                    # รูปภาพประกอบอินเทอร์เฟซ
├── Windows Shutdown Timer.spec # ไฟล์การตั้งค่าการแพ็ก .exe ของ PyInstaller
├── timer_config.json          # ไฟล์เซฟการตั้งค่าเวลาปัจจุบัน (สร้างขึ้นชั่วคราว)
└── window_config.json         # ไฟล์จดจำขนาดและตำแหน่งหน้าต่าง
```

---

## การทำงานเบื้องหลัง (How It Works)

โปรแกรมเรียกใช้คำสั่งระบบของ Windows (Windows Command Line) ในการทำงานดังนี้:
- **Shutdown**: `shutdown /s /t [seconds]`
- **Restart**: `shutdown /r /t [seconds]`
- **Sleep**: `rundll32.exe powrprof.dll,SetSuspendState 0,1,0`
- **Hibernate**: `rundll32.exe powrprof.dll,SetSuspendState 1,1,0`
- **Cancel**: `shutdown /a`

---

## ประวัติการอัปเดต (Changelog)

### v1.5.0 (June 2026) - Resizable Window & Settings Separation
- **Resizable UI**: เปลี่ยนขนาดหน้าต่างให้ยืดขยายได้อย่างอิสระโดยตั้งขนาดขั้นต่ำไว้ที่ 600x680px เพื่อลดการแออัดของหน้าจอ
- **Position & Size Persistence**: บันทึกข้อมูลขนาด (Size) และพิกัดตำแหน่ง (Position) ลงในไฟล์ `window_config.json` ตอนปิดแอป และกู้คืนสภาพแวดล้อมเดิมเมื่อเปิดแอปใหม่
- **Clean Configuration Architecture**: แยกการจดจำขนาดหน้าต่างออกจากประวัติตั้งเวลา เพื่อไม่ให้ข้อมูลตำแหน่งและขนาดหน้าต่างหายไปเมื่อสิ้นสุดการตั้งเวลาหรือเคลียร์ช่องป้อนข้อมูล

### v1.4.0 (March 2026) - Terminal Logging & Code Cleanup
- **Terminal Logging**: เพิ่มระบบ Log รายละเอียดการทำงานของแอปใน Terminal พร้อม Emoji และ Timestamp รูปแบบ `HH:MM:SS │ message`
- **Code Optimization**: เคลียร์ Unused Imports (QSpinBox, QPainter, QPen ฯลฯ) และลบ dead code ออกทั้งหมดเพื่อลดขนาดแอปพลิเคชัน

### v1.3.0 (March 2026) - UI/UX Improvements
- **Action Icons**: ปรับปรุงเมนู Dropdown ให้เป็นสัญลักษณ์ Emoji ที่อ่านง่าย (🔌, 🔄, 😴, 🌙)
- **Monospace Countdown**: ตั้งค่า Font-pitch ของหน้าจอถอยหลังแบบเรียลไทม์เพื่อป้องกันไม่ให้ตัวเลขขยับตัวขณะนับถอยหลัง

### v1.2.0 (March 2026) - Bug Fixes & Stability
- **Memory Leak Fix**: หยุดการทำงานของ QTimer ทันทีเมื่อปิดหน้าต่าง ป้องกันโปรแกรมค้างใน Task Manager
- **Atomic File Config**: เปลี่ยนกระบวนการบันทึกไฟล์ config แบบเขียนลงไฟล์ชั่วคราวก่อนย้ายทับไฟล์จริง ป้องกันปัญหาเขียนไฟล์ทับขณะไดรฟ์ต่างกัน (Cross-drive move error)

---

## สัญญาอนุญาต (License)

โครงการนี้อยู่ภายใต้สัญญาอนุญาตแบบ **MIT License** สามารถนำไปดัดแปลง ศึกษา และใช้งานได้ฟรีตามข้อตกลงที่ระบุไว้
