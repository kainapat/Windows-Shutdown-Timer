# 🕒 Windows Shutdown Timer

โปรแกรมตั้งเวลาปิดเครื่อง/รีสตาร์ท/พักเครื่อง/จำศีลคอมพิวเตอร์ Windows อัตโนมัติ ที่มาพร้อมกับ GUI สวยงามและใช้งานง่าย

A beautiful and user-friendly Windows shutdown/restart/sleep/hibernate timer application with dark mode UI.

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.0+-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![PyInstaller](https://img.shields.io/badge/PyInstaller-6.16+-orange.svg)
![Last Updated](https://img.shields.io/badge/Last%20Updated-March%202026-brightgreen.svg)

---

## ✨ Features (คุณสมบัติเด่น)

- 🎯 **สี่โหมดการทำงาน**: Shutdown, Restart, Sleep, Hibernate
- ⚡ **Quick Presets**: ปุ่มลัด 15 นาที, 30 นาที, 1 ชั่วโมง, 2 ชั่วโมง
- ⏰ **หลากหลายรูปแบบการตั้งเวลา**:
  - ระบุวัน/เวลาเจาะจง (Specific Date/Time)
  - นับถอยหลังแบบชั่วโมง (1-24 ชั่วโมง)
  - นับถอยหลังแบบนาที (1-60 นาที)
  - นับถอยหลังแบบวินาที (10-300 วินาที)
- 📊 **Progress Bar**: แสดงความคืบหน้าการนับถอยหลัง + เวลาที่เหลือในรูปแบบ MM:SS (เช่น "50% - เหลือ 15:45")
- 📊 **ตัวนับถอยหลังแบบเรียลไทม์**: แสดงเวลาที่เหลืออย่างชัดเจนด้วยฟอนต์ monospace ที่ทำให้ตัวเลขอ่านง่ายขึ้น
- � **แสดงเวลาที่จะทำการกระทำ**: สถานะแสดงเวลาจริง เช่น "จะปิดเครื่องเวลา 17:00" แทนการนับถอยหลัง
- �💾 **บันทึกการตั้งค่าอัตโนมัติ** (ชั่วคราวระหว่างการรัน): ลบไฟล์เมื่อปิดโปรแกรมหรือเมื่อเวลาทำงานเสร็จสิ้น
- 🔒 **Safety Features**: 
  - Atomic file writes สำหรับ config
  - Input validation (24 ชั่วโมง max)
  - Auto-cancel previous schedules
- 🎨 **Dark Mode UI**: ธีมสีสวยงามแบบ Dark Blue พร้อม Dynamic Color Theme ตามการกระทำที่เลือก
- 🔔 **Toast Notifications**: แจ้งเตือนสถานะแบบ Overlay พร้อมสีตามประเภท และป้องกันการซ้อนกันด้วยการจัดการ memory ที่ถูกต้อง
- ⚡ **เบาและรวดเร็ว**: ไม่กินทรัพยากรระบบ
- 🔧 **Bug Fixes & Improvements**:
  - แก้ปัญหา Toast ซ้อนกันเมื่อแสดงเร็ว ๆ (ใช้ deleteLater แทน close)
  - ป้องกัน memory leak จากการจัดการ widget ที่ไม่ถูกต้อง
  - แสดงเวลาที่จะทำการกระทำแทนการนับถอยหลัง เพื่อเห็นชัดเจนยิ่งขึ้น

---

## 📋 System Requirements (ข้อกำหนดระบบ)

- **Operating System**: Windows 7/8/10/11
- **Python**: 3.12 หรือสูงกว่า (สำหรับรันจาก source code)
- **ไลบรารี่ที่ต้องใช้**:
  - PySide6 6.0+
  - PyInstaller 6.16+ (สำหรับ build .exe)

---

## 🚀 Installation (การติดตั้ง)

### วิธีที่ 1: ใช้ไฟล์ .exe (แนะนำสำหรับผู้ใช้ทั่วไป)

1. ดาวน์โหลดไฟล์ `.exe` จากหน้า [Releases](../../releases)
2. Double-click เพื่อเปิดโปรแกรม
3. เริ่มใช้งานได้เลย ไม่ต้องติดตั้ง Python

### วิธีที่ 2: รันจาก Source Code (สำหรับ Developer)

1. **Clone หรือดาวน์โหลด repository นี้**
   ```bash
   git clone https://github.com/kainapat/Windows-Shutdown-Timer.git
   cd "Windows-Shutdown-Timer"
   ```

2. **ติดตั้ง Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **รันโปรแกรม**
   ```bash
   python shutdown_timer.py
   ```

---

## 🎮 How to Use (วิธีใช้งาน)

### Quick Presets (ใช้งานเร็ว)
1. เลือกการกระทำ (Shutdown หรือ Restart)
2. กดปุ่ม Preset ที่ต้องการ (15 นาที / 30 นาที / 1 ชม. / 2 ชม.)
3. ยืนยัน แล้วรอนับถอยหลัง

### โหมดปกติ
1. **เลือกการกระทำ** (Action):
   - ปิดเครื่อง (Shutdown)
   - รีสตาร์ท (Restart)
   - พักเครื่อง (Sleep)
   - จำศีล (Hibernate)

2. **เลือกโหมดการตั้งเวลา**:
   - ✅ ระบุวันที่/เวลา: เลือกวันและเวลาที่ต้องการจากปฏิทิน
   - ✅ นับถอยหลัง (ชั่วโมง): เลือกจำนวนชั่วโมง
   - ✅ นับถอยหลัง (นาที): เลือกจำนวนนาที
   - ✅ นับถอยหลัง (วินาที): เลือกจำนวนวินาที

3. **กดปุ่ม "เริ่มตั้งเวลา"**
   - โปรแกรมจะยืนยันความต้องการอีกครั้ง
   - เมื่อยืนยันแล้ว Progress Bar และตัวนับถอยหลังจะเริ่มทำงาน

4. **ยกเลิกการตั้งเวลา** (ถ้าต้องการ):
   - กดปุ่ม "ยกเลิก" ได้ตลอดเวลาก่อนหมดเวลา

5. **ล้างค่า**:
   - กดปุ่ม "ล้างค่า" เพื่อรีเซ็ตการตั้งค่าทั้งหมด

> ⚠️ **คำเตือน**: กรุณาบันทึกงานของคุณก่อนตั้งเวลาปิดเครื่อง/รีสตาร์ท!

---

## 🔧 Build เป็น .exe (สำหรับ Developer)

หากต้องการสร้างไฟล์ `.exe` แบบ standalone:

1. **ติดตั้ง PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Build โปรแกรม**
   ```bash
   pyinstaller --onefile --windowed --name="Windows Shutdown Timer" --icon=icon.ico shutdown_timer.py
   ```

3. **ไฟล์ .exe จะอยู่ที่**
   ```
   dist/Windows Shutdown Timer.exe
   ```

---

## 📂 Project Structure

```
Windows Shutdown Timer/
│
├── .github/workflows/         # GitHub Actions for auto build
│   └── build-release.yml
├── shutdown_timer.py          # Main application source code
├── requirements.txt           # Python dependencies
├── icon.ico                   # Application icon
├── off.png                    # Additional resource
├── Windows Shutdown Timer.spec # PyInstaller spec file
├── timer_config.json          # Auto-saved settings (created at runtime)
├── build/                     # Build artifacts (gitignored)
└── dist/                      # Compiled executable (gitignored)
```

---

## 🎨 UI Preview

โปรแกรมมาพร้อมกับ **Dark Mode Theme** ที่สวยงามและทันสมัย:
- สีพื้นหลัง: Deep Blue (#1e1e2e) พร้อม Dynamic Gradient ตาม Action ที่เลือก
- สีปุ่มเริ่มต้น: ตามสีธีม (ชมพู/ส้ม/น้ำเงิน/ม่วง)
- สีปุ่มยกเลิก: Gradient แดง
- ฟอนต์: Segoe UI (Action/Controls) + Auto-detected Monospace (Countdown display)
- **Action Icons**: Emoji ที่เข้าใจง่าย (🔌 Shutdown / 🔄 Restart / 😴 Sleep / 🌙 Hibernate)
- **Countdown Font**: Fixed-pitch monospace ที่ป้องกันการกระโดดของตัวเลข
- มี Hover Effects, Drop Shadow และ Rounded Corners
- Progress Bar แสดง % + เวลาที่เหลือ (เช่น "45% - เหลือ 12:30")
- Toast Notification แสดงที่ด้านบนหน้าต่าง ไม่ซ้อนทับกัน พร้อม memory leak fix
- ขนาดหน้าต่างคงที่ 600×680px

---

## 🔒 How It Works (หลักการทำงาน)

โปรแกรมนี้ทำงานโดยส่งคำสั่งไปยัง Windows System โดยตรงผ่าน Command Line:

- **Shutdown**: `shutdown /s /t [seconds]`
- **Restart**: `shutdown /r /t [seconds]`
- **Sleep**: `rundll32.exe powrprof.dll,SetSuspendState 0,1,0`
- **Hibernate**: `rundll32.exe powrprof.dll,SetSuspendState 1,1,0`
- **Cancel**: `shutdown /a`

**Safety Features**:
- ✅ อัตโนมัติยกเลิกการตั้งเวลาเดิมก่อนตั้งเวลาใหม่
- ✅ Atomic file writes สำหรับ `timer_config.json` เพื่อหลีกเลี่ยงการเสียหาย
- ✅ Input validation เพื่อป้องกันการตั้งเวลาเกินกว่า 24 ชั่วโมง
- ✅ Error handling ที่ชัดเจนสำหรับข้อความผิดพลาด (Admin permissions, etc.)

ไม่มีการติดตั้งซอฟต์แวร์เพิ่มเติม และปลอดภัย 100%

---

## 📝 Configuration File

โปรแกรมจะบันทึกการตั้งค่าล่าสุดไว้ในไฟล์ `timer_config.json`:
```json
{
    "action": 0,
    "mode": 1,
    "date": "2026-03-02",
    "time": "20:00",
    "hours": 2,
    "minutes": 30,
    "seconds": 0
}
```

ไฟล์นี้จะถูกลบอัตโนมัติเมื่อปิดโปรแกรม เมื่อเวลานับถอยหลังถึง 0 หรือกด "ล้างค่า"

---

## 🚀 Auto Build with GitHub Actions

Repository นี้มี GitHub Actions workflow สำหรับ Build และ Release อัตโนมัติ:

- Push tag แบบ `v*` (เช่น `v1.0.0`) เพื่อ trigger build
- Build จะทำงานบน Windows และสร้าง `.exe`
- Release พร้อมไฟล์ `.exe` จะถูกสร้างโดยอัตโนมัติ

---

## 🐛 Known Issues / Limitations

- ต้องใช้สิทธิ์ Administrator เมื่อตั้งเวลา Shutdown/Restart บนระบบที่มีการป้องกันสูง
- ทำงานได้บน Windows เท่านั้น (ใช้คำสั่ง `shutdown` ของ Windows)
- Sleep/Hibernate จะทำงานทันทีและไม่รอเวลา (ตามการออกแบบเดิม)

---

## 🤝 Contributing

ยินดีรับ Pull Requests และ Suggestions ทุกรูปแบบ!

---

## 📄 License

This project is open source and available for personal and educational use.

---

## 👨‍💻 Author

Created with ❤️ for Windows users who need a simple shutdown timer.

---

## 📅 Changelog

### v1.3.0 (March 2026) - UI/UX Improvements
**Enhancements**:
- ✨ Action Combo Box: เปลี่ยนมาใช้ Emoji ที่เข้าใจง่าย (🔌🔄😴🌙) แทนสัญลักษณ์นามธรรม
- ✨ Thai-only UI: ลบข้อความภาษาอังกฤษออกจากการเลือก Action เพื่อให้อินเทอร์เฟซสะอาดกว่า
- ✨ Progress Bar Enhancement: แสดงเปอร์เซ็นต์ + เวลาที่เหลือในรูปแบบ MM:SS (เช่น "50% - เหลือ 15:45")
- 🔧 Font Detection: ปรับปรุงการเลือกฟอนต์แบบ Monospace ด้วย Smart Fallback (JetBrains Mono → Consolas → Courier New)
- 🔧 Fixed-Pitch Display: เพิ่ม setFixedPitch() เพื่อป้องกันการกระโดดของตัวเลขในตัวนับถอยหลัง

### v1.2.0 (March 2026) - Bug Fixes & Stability
**Critical Fixes**:
- 🔧 แก้ไข: QTimer memory leak - เพิ่ม `.stop()` ใน closeEvent()
- 🔧 แก้ไข: Race condition ในฟังก์ชัน update_countdown() - ปรับใช้ datetime comparison แบบตรงไป
- 🔧 แก้ไข: Config file cross-drive move error - ใช้ temp file ในไดเรกทอรีเดียวกัน
- 🔧 แก้ไข: Logger not defined error - เพิ่ม logger initialization

**Improvements**:
- ⚡ Input validation - เพิ่มการตรวจสอบค่าสูงสุด 24 ชั่วโมง
- ⚡ Shutdown scheduling - อัตโนมัติยกเลิกการตั้งเวลาเดิมก่อนตั้งใหม่
- ⚡ Error handling - ปรับปรุงข้อความแสดงข้อผิดพลาดให้ชัดเจน (รองรับ error codes)
- ⚡ Cancel timer - เพิ่ม proper cleanup และ error handling สำหรับการยกเลิก

### v1.1.0 (March 2026) - UI Improvements
- 🎨 ปรับสีตัวเลข % ใน Progress Bar เป็นสีเทา (#808080) เพื่อให้อ่านง่ายขึ้น
- 🔧 อัปเดต build ด้วย PyInstaller 6.16 + Python 3.12

### v1.0.0 (Initial Release)
- 🎯 สี่โหมดการทำงาน: Shutdown, Restart, Sleep, Hibernate
- ⚡ Quick Presets (15 นาที / 30 นาที / 1 ชม. / 2 ชม.)
- 📊 Progress Bar + Real-time Countdown
- 🎨 Dark Mode UI พร้อม Dynamic Color Theme
- 🔔 Toast Notifications
- 💾 Auto-save Config

---

**Happy Scheduling! 🎉**
