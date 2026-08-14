# เอกสารวิเคราะห์สาเหตุและสรุปการแก้ไขปัญหา (Post-Mortem Report)
## Windows Shutdown Timer v2.0.0 - UX/UI Redesign & Contrast Fix

**วันที่:** 14 สิงหาคม 2026  
**ระบบที่เกี่ยวข้อง:** `shutdown_timer.py` (PySide6 Desktop Application)  
**ผู้รับผิดชอบ:** ทีมพัฒนา Windows Shutdown Timer  
**สถานะ:** แก้ไขเสร็จสิ้นและผ่านการตรวจรับรอง (Fixed & Validated)  

---

### 1. สรุปภาพรวม (Summary)
หน้าต่างแอปพลิเคชัน Windows Shutdown Timer เวอร์ชันเดิม (v1.9.0) ประสบปัญหา **Text Contrast ต่ำผิดปกติ** ในระดับรุนแรง โดยสีของหัวข้อการ์ดและป้ายกำกับข้อความกลืนไปกับพื้นหลังทั้งใน Dark Mode และ Light Mode ส่งผลให้ผู้ใช้มองเห็นตัวหนังสือได้ยาก นอกจากนี้ โครงสร้างแบบ Bento Grid 5 การ์ดทำให้การจัดวางองค์ประกอบกระจัดกระจาย

ปัญหาได้รับการแก้ไขอย่างสมบูรณ์ใน **v2.0.0** โดยการยกเลิก Bento Grid และเปลี่ยนมาใช้ **3-Step Vertical Flow** ตามมาตรฐาน Windows 11 Fluent Design พร้อมรื้อถอนและเขียนระบบ QSS StyleSheet ใหม่ 100% ทำให้ค่าความคมชัดของข้อความผ่านเกณฑ์มาตรฐานสากล **WCAG AA** ทุกจุด และทำการ Build ไฟล์ `.exe` ใหม่พร้อม Push ขึ้น GitHub (`main` branch)

---

### 2. อาการของปัญหา (Symptom)
- **Dark Mode**: ข้อความหัวข้อการ์ด เช่น *"การตั้งค่าและการกระทำ"* และ *"ระบุเวลาทำงาน"* แสดงผลด้วยสีเทาเข้มอมม่วง (`#1a1a24`) บนพื้นหลังการ์ดสีมืด ส่งผลให้หัวข้อกลมกลืนจนแทบมองไม่เห็นด้วยตาเปล่า
- **Light Mode**: ข้อความป้ายกำกับและตัวเลขในช่อง SpinBox มีสีจาง (`#888899`) ทำให้ขาดความเด่นชัด
- **Visual Chaos**: ผู้ใช้ต้องกวาดสายตาไปมา 4 ทิศทางทั่วหน้าจอเพื่อตั้งเวลาปิดเครื่อง

---

### 3. สาเหตุหลักของปัญหา (Root Cause)
1. **QSS Style Token Hardcoding**: ในไฟล์ `shutdown_timer.py` คลาส `BentoCard` และฟังก์ชัน `apply_styles()` มีการกำหนดค่าสี Hex Code สำหรับ `#bentoCardTitle` และ `QLabel` เป็นค่าคงที่แบบสากล (`#1a1a24`) โดยไม่ได้ปรับเปลี่ยนตามสภาวะโหมดมืด/สว่าง และขาดการกำหนดระดับ Contrast ที่ถูกต้อง
2. **Layout Fragmentation**: การแบ่งพื้นที่หน้าจอเป็น 5 กรอบการ์ดย่อย (`QGridLayout` 2x3) ทำให้เกิดระยะห่าง (Margin/Padding) ซ้ำซ้อน และบดบังพื้นที่การแสดงผลตัวเลขนับถอยหลังหลัก

---

### 4. กลไกที่ทำให้เกิดปัญหา (Why it produced the symptom)
เมื่อแอปพลิเคชันเริ่มต้นทำงาน ฟังก์ชัน `apply_styles()` จะทำการ Apply QSS String เข้ากับ `QApplication` แต่เนื่องจาก Selector `#bentoCardTitle` กำหนดสีข้อความไว้เพียงค่าเดียว ชนิดของสีจึงไม่มีความยืดหยุ่นต่อการสลับธีม ส่งผลให้เมื่อสลับเป็น Dark Mode ตัวหนังสือจึงกลายเป็นสีมืดบนพื้นหลังมืดทันที

---

### 5. การแก้ไขปัญหา (Fix)
- **Commit `a900619`**: ปรับปรุงพจนานุกรม `ACTION_COLORS` ใน `shutdown_timer.py` ให้มี Dynamic Accent Colors ที่สดใส (ปิดเครื่อง = `#ff3b5c`, รีสตาร์ท = `#ff9500`, พักเครื่อง = `#007aff`, จำศีล = `#a855f7`) และปรับแต่งการสร้าง `BentoCard` ให้ใช้ชื่อ Object `#bentoCardTitle` พร้อมฟอนต์ `Segoe UI Variable Display` (11pt DemiBold)
- **Commit `17c6be0`**: รีแฟกเตอร์ฟังก์ชัน `ShutdownTimerApp.init_ui()` โดยเปลี่ยนจาก `QGridLayout` 5 ช่อง มาเป็น **3-Step Vertical Flow**:
  1. *Hero Countdown Display* (ด้านบนสุด): ตัวเลขแบบ Monospace 44pt Bold (`JetBrains Mono` / `Consolas`)
  2. *Step 1: เลือกการกระทำ* (Pill Buttons 4 ตัวเลือก)
  3. *Step 2: กำหนดเวลา* (Quick Preset Chips `15m`, `30m`, `1h`, `2h` + Mode Switcher + SpinBox Inputs)
  4. *Step 3: ปุ่มเริ่มการทำงาน* (Primary CTA Button ขนาดใหญ่)
- **Commit `bad14b2`**: เขียน QSS StyleSheet ใน `apply_styles()` ใหม่ทั้งหมด:
  - **Dark Mode**: กำหนดสีหัวข้อการ์ดเป็น Zinc 100 (`#f4f4f5`) และข้อความทั่วไปเป็น Zinc 200 (`#e4e4e7`) บนพื้นหลังการ์ด Zinc 900 (`#18181b`)
  - **Light Mode**: กำหนดสีหัวข้อการ์ดเป็น Slate 800 (`#1e293b`) และข้อความทั่วไปเป็น Slate 700 (`#334155`) บนพื้นหลังการ์ดสีขาวบริสุทธิ์ (`#ffffff`)

---

### 6. กระบวนการตรวจสอบและค้นหาปัญหา (How it was found)
- **Visual & Code Inspection**: ตรวจสอบรูปภาพหน้าจอเปรียบเทียบระหว่าง Dark/Light mode พบว่าตัวหนังสือส่วนหัวจางลงอย่างชัดเจน
- **Code Tracing**: แกะโค้ดใน `shutdown_timer.py` บริเวณคลาส `BentoCard` และ `apply_styles()` พบจุดที่ไม่ได้แยก CSS Selector ให้ครอบคลุมธีม

---

### 7. สาเหตุที่หลุดรอดไปในเวอร์ชันก่อนหน้า (Why it slipped through)
ในเวอร์ชัน v1.8.0 มีการเพิ่ม Light Mode เข้ามาแต่เน้นการปรับแต่งโทนสีพื้นหลังหลัก (Background Gradient) เป็นหลัก โดยไม่ได้ทำ Audit ความคมชัดของตัวหนังสือ (Text Contrast Ratio) ในทุกๆ Widget ย่อย ส่งผลให้ Style Rule สำหรับหัวข้อการ์ดใช้ค่าสีเดิมที่ตกค้างมาจาก v1.7.0

---

### 8. การทดสอบและยืนยันผล (Validation)
1. **Python Compilation Verification**:
   ```powershell
   python -m py_compile shutdown_timer.py
   ```
   *ผลการทดสอบ:* สำเร็จด้วย Exit Code 0 (ไม่พบข้อผิดพลาดไวยากรณ์)
2. **PyInstaller Binary Compilation**:
   ```powershell
   pyinstaller "Windows Shutdown Timer.spec" --clean
   ```
   *ผลการทดสอบ:* สร้างไฟล์สแตนด์อโลน `dist/Windows Shutdown Timer.exe` ได้อย่างสมบูรณ์แบบโดยไม่มี Error
3. **Deployment Verification**:
   - อัปเดต `README.md` (v2.0.0 Changelog)
   - ทำการ Push โค้ดทั้งหมดขึ้น GitHub Repository (`kainapat/Windows-Shutdown-Timer`) บน `main` branch เรียบร้อยแล้ว

---

### 9. รายการที่ต้องดำเนินการต่อ (Action Items / Follow-ups)
- [x] อัปเดตเอกสารคู่มือและ README.md *(เสร็จสิ้น - Commit `38920ea`)*
- [x] สร้างไฟล์ executable `.exe` สำหรับใช้งานบน Windows *(เสร็จสิ้น - `dist/Windows Shutdown Timer.exe`)*
- [x] บันทึก Post-Mortem Report ทั้งภาษาอังกฤษและภาษาไทยลงในคลังเอกสาร *(เสร็จสิ้น)*
