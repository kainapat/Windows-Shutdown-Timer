# 🕒 Windows Shutdown Timer

โปรแกรมตั้งเวลาปิดเครื่อง/รีสตาร์ท/พักเครื่อง/จำศีลคอมพิวเตอร์ Windows อัตโนมัติ ที่มาพร้อมกับ GUI สวยงามและใช้งานง่าย

A beautiful and user-friendly Windows shutdown/restart/sleep/hibernate timer application with dark mode UI.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/PySide6-6.0+-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

---

## ✨ Features (คุณสมบัติเด่น)

- 🎯 **สี่โหมดการทำงาน**: Shutdown, Restart, Sleep, Hibernate
- ⚡ **Quick Presets**: ปุ่มลัด 15 นาที, 30 นาที, 1 ชั่วโมง, 2 ชั่วโมง
- ⏰ **หลากหลายรูปแบบการตั้งเวลา**:
  - ระบุวัน/เวลาเจาะจง (Specific Date/Time)
  - นับถอยหลังแบบชั่วโมง (1-24 ชั่วโมง)
  - นับถอยหลังแบบนาที (1-60 นาที)
  - นับถอยหลังแบบวินาที (10-300 วินาที)
- 📊 **Progress Bar**: แสดงความคืบหน้าการนับถอยหลังเป็น %
- 📊 **ตัวนับถอยหลังแบบเรียลไทม์**: แสดงเวลาที่เหลืออย่างชัดเจน
- 💾 **บันทึกการตั้งค่าอัตโนมัติ**: เปิดครั้งหน้าไม่ต้องตั้งใหม่
- 🎨 **Dark Mode UI**: ธีมสีสวยงามแบบ Navy Blue
- 📐 **ปรับขนาดหน้าต่างได้**: UI ย่อ/ขยายได้ตามต้องการ
- ⚡ **เบาและรวดเร็ว**: ไม่กินทรัพยากรระบบ

---

## 📋 System Requirements (ข้อกำหนดระบบ)

- **Operating System**: Windows 7/8/10/11
- **Python**: 3.8 หรือสูงกว่า (สำหรับรันจาก source code)
- **ไลบรารี่ที่ต้องใช้**:
  - PySide6

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
- สีพื้นหลัง: Navy Blue (#1e1e2e)
- สีปุ่ม: Blue/Pink/Gray accents
- ฟอนต์: Segoe UI
- มี Hover Effects และ Rounded Corners
- Progress Bar แสดง % การนับถอยหลัง
- UI ย่อ/ขยายขนาดได้

---

## 🔒 How It Works (หลักการทำงาน)

โปรแกรมนี้ทำงานโดยส่งคำสั่งไปยัง Windows System โดยตรงผ่าน Command Line:

- **Shutdown**: `shutdown /s /t [seconds]`
- **Restart**: `shutdown /r /t [seconds]`
- **Sleep**: `rundll32.exe powrprof.dll,SetSuspendState 0,1,0`
- **Hibernate**: `rundll32.exe powrprof.dll,SetSuspendState 1,1,0`
- **Cancel**: `shutdown /a`

ไม่มีการติดตั้งซอฟต์แวร์เพิ่มเติม และปลอดภัย 100%

---

## 📝 Configuration File

โปรแกรมจะบันทึกการตั้งค่าล่าสุดไว้ในไฟล์ `timer_config.json`:
```json
{
    "action": 0,
    "mode": 1,
    "date": "2025-11-20",
    "time": "20:00",
    "hours": 2,
    "minutes": 30,
    "seconds": 0
}
```

ไฟล์นี้จะถูกลบอัตโนมัติเมื่อปิดโปรแกรม หรือกด "ล้างค่า"

---

## 🚀 Auto Build with GitHub Actions

Repository นี้มี GitHub Actions workflow สำหรับ Build และ Release อัตโนมัติ:

- Push tag แบบ `v*` (เช่น `v1.0.0`) เพื่อ trigger build
- Build จะทำงานบน Windows และสร้าง `.exe`
- Release พร้อมไฟล์ `.exe` จะถูกสร้างโดยอัตโนมัติ

---

## 🐛 Known Issues / Limitations

- ต้องใช้สิทธิ์ Administrator บางครั้ง (ขึ้นกับ Windows settings)
- ทำงานได้บน Windows เท่านั้น (ใช้คำสั่ง `shutdown` ของ Windows)

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

**Happy Scheduling! 🎉**
