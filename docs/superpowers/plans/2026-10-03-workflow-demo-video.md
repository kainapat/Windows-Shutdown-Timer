# Windows Shutdown Timer Workflow Demo Video Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce a safe, polished 20-second Thai 1920×1080 workflow-demo video that shows the real Windows Shutdown Timer UI from Shutdown selection through an active countdown without executing any Windows power command.

**Architecture:** Capture real PySide6 UI states through a dedicated harness that monkey-patches the module-level `subprocess.run` before the window is created. Compose those captures into a 20-second 30fps video with restrained motion, Thai explanatory copy, subtle generated audio, a settled poster frame, and share copy. All generated/intermediate assets live under `brag-output/`.

**Tech Stack:** Python 3, PySide6, Pillow, ffmpeg/ffprobe when available, project assets from `off.png` / `off.ico`.

## Global Constraints
- Tone: Polished / Professional.
- Language: Thai.
- Format: 1920×1080, 30 fps.
- Duration: 20 seconds.
- Audio: subtle background music + restrained UI sound effects; no narration.
- Never issue a real Shutdown, Restart, Sleep, or Hibernate command during production.
- Use the real application UI and current project colors/assets.
- Story focus: Shutdown → Timer → duration → Start → active countdown → Cancel vs Reset → branded outro.

---### Task 1: Safe real-UI capture harness

**Files:**
- Create: `brag-output/work/capture_states.py`
- Create: `brag-output/work/test_capture_safety.py`

**Interfaces:**
- Consumes: `shutdown_timer.ShutdownTimerApp`.
- Produces: `capture_all(output_dir: pathlib.Path) -> dict[str, pathlib.Path]` and PNGs for `initial`, `duration`, `active`, and `controls`.

- [ ] **Step 1: Write the failing safety test**

```python
from pathlib import Path
from capture_states import FakeSubprocessRun

def test_power_commands_are_noop():
    fake = FakeSubprocessRun()
    fake(["shutdown", "/s", "/t", "1800"], check=True)
    fake(["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"], check=True)
    assert fake.calls == [
        ["shutdown", "/s", "/t", "1800"],
        ["rundll32.exe", "powrprof.dll,SetSuspendState", "0,1,0"],
    ]
    assert fake.spawned_processes == 0
```

- [ ] **Step 2: Run test and verify it fails**

Run: `python brag-output/work/test_capture_safety.py`
Expected: import/definition failure because the capture harness does not exist yet.- [ ] **Step 3: Implement the harness**

Implement `FakeSubprocessRun.__call__()` to record arguments and return `subprocess.CompletedProcess(args, 0, "", "")` without calling the real process API. Import `shutdown_timer`, replace `shutdown_timer.subprocess.run` with that instance before creating `ShutdownTimerApp`, switch the UI to Thai, and use `QWidget.grab().save(...)` after each state change.

The capture sequence must:
1. show the real default window;
2. select Shutdown + Timer and set 0h 30m 0s;
3. call the real `start_timer()` while the monkey patch is active;
4. wait/process events until countdown UI is visible;
5. save each required PNG;
6. assert every intercepted command begins with `shutdown` or `rundll32.exe` and no real process was spawned.

- [ ] **Step 4: Run safety test and capture smoke test**

Run: `python brag-output/work/test_capture_safety.py`
Expected: PASS.

Run: `python brag-output/work/capture_states.py`
Expected: PNG files in `brag-output/work/captures/` and terminal output showing intercepted no-op power commands only.

- [ ] **Step 5: Commit harness source**

```bash
git add brag-output/work/capture_states.py brag-output/work/test_capture_safety.py
git commit -m "test: add safe video capture harness"
```### Task 2: Video compositor and generated soundtrack

**Files:**
- Create: `brag-output/work/render_video.py`

**Interfaces:**
- Consumes: captured PNGs under `brag-output/work/captures/`, `off.png`.
- Produces: frame sequence `brag-output/work/frames/frame_%05d.png` and WAV audio `brag-output/work/brag_audio.wav`.

- [ ] **Step 1: Implement deterministic scene timing**

Define 600 frames at 30fps:
- 0–59: hook/outro identity styling.
- 60–149: real app UI + Shutdown emphasis.
- 150–269: Timer + 30-minute selection.
- 270–359: Start interaction / active-state reveal.
- 360–479: active countdown + progress.
- 480–539: Cancel vs Reset distinction.
- 540–599: branded outro.

Use easing functions only for restrained scale/position/opacity transitions. Every Thai line must remain fully settled long enough to read.

- [ ] **Step 2: Implement frame rendering**

Use Pillow to create each 1920×1080 frame, place the real 520×560 app capture at high-resolution scale without distortion, preserve the app's current palette, and add Thai captions:
- `ตั้งเวลาปิดเครื่อง Windows ได้ในไม่กี่ขั้นตอน`
- `เลือก Shutdown`
- `เลือก Timer และกำหนดเวลา`
- `เริ่มนับถอยหลัง`
- `Cancel = ยกเลิกคำสั่ง Windows`
- `Reset = ล้างค่าหน้าจอเท่านั้น`
- `ตั้งเวลา ปิดเครื่องอย่างเรียบง่าย`

Use a Thai-capable system font discovered from Windows; do not bundle or copy font files.

- [ ] **Step 3: Generate subtle audio**

Generate a low-volume 20-second WAV with simple sine/pad tones and soft click accents at scene transitions using Python's standard `wave` module. Keep peaks below -10 dBFS-equivalent amplitude and avoid speech.- [ ] **Step 4: Smoke-render representative frames**

Run: `python brag-output/work/render_video.py --stills-only`
Expected: representative settled and transition frames written under `brag-output/work/checks/` with no clipping.

- [ ] **Step 5: Commit compositor source**

```bash
git add brag-output/work/render_video.py
git commit -m "feat: add workflow demo video renderer"
```

### Task 3: Encode final media and poster

**Files:**
- Generate: `brag-output/brag.mp4`
- Generate: `brag-output/brag.jpg`

**Interfaces:**
- Consumes: frame sequence + WAV.
- Produces: H.264/AAC MP4, 1920×1080, 30fps, ~20s; poster JPEG from a settled frame.

- [ ] **Step 1: Detect ffmpeg/ffprobe**

Run: `ffmpeg -version` and `ffprobe -version`.
Expected: available CLI. If unavailable, use an installed Python encoder package without adding a new dependency.

- [ ] **Step 2: Encode video**

Encode the frame sequence at 30fps, yuv420p H.264, and AAC audio. The first video frame must be the chosen settled poster image rather than a transition frame.

- [ ] **Step 3: Extract poster**

Use the strongest settled frame from the active-countdown or outro scene, save as `brag-output/brag.jpg`, and ensure frame 0 of the final video matches it.

- [ ] **Step 4: Verify technical properties**

Run ffprobe to verify width=1920, height=1080, frame rate=30/1, audio present, and duration within 19.8–20.2 seconds.### Task 4: Content QA, share copy, and final delivery

**Files:**
- Create: `brag-output/brag-plan.md`
- Create: `brag-output/share-copy.txt`

**Interfaces:**
- Consumes: final MP4, poster, approved design spec.
- Produces: QA-approved deliverable set.

- [ ] **Step 1: Write `brag-plan.md`**

Record the approved Workflow Demo angle, scene timings, Thai copy, visual identity, safe-capture strategy, and audio direction exactly as implemented.

- [ ] **Step 2: Write share copy**

Use concise Thai copy:
```text
Windows Shutdown Timer — ตั้งเวลาปิดหรือรีสตาร์ต Windows ผ่าน Timer หรือ Clock พร้อม Countdown แบบเรียลไทม์ ใน UI ที่เรียบและกระชับ
```

- [ ] **Step 3: Inspect representative frames**

Inspect the first settled frame, Timer-selection frame, active-countdown frame, Cancel-vs-Reset frame, outro, and at least two mid-transition frames. Fix any collision, unreadable Thai text, low contrast, or malformed app screenshot.

- [ ] **Step 4: Verify behavioral claims**

Confirm against `shutdown_timer.py` that Shutdown/Restart schedule via `shutdown /s|/r /t`, Cancel calls `shutdown /a`, Reset does not call `shutdown /a`, and Sleep/Hibernate are immediate after confirmation.

- [ ] **Step 5: Final safety check**

Search all capture/render logs and scripts. Confirm there is no code path that can call the real `subprocess.run` for power commands during production and no real shutdown/restart remains scheduled.

- [ ] **Step 6: Deliver**

Report exact paths for `brag.mp4`, `brag.jpg`, `share-copy.txt`, and `brag-plan.md`.
