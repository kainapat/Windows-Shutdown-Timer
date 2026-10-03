# Windows Shutdown Timer — Workflow Demo Video Design

## Goal
Create a 20-second polished 16:9 launch/demo video in Thai that explains the real usage flow of Windows Shutdown Timer from action selection through an active countdown.

## Audience
People seeing the project for the first time. After one viewing they should understand what the app does and how a scheduled Shutdown/Restart flow works.

## Creative Direction
- Tone: Polished / Professional
- Language: Thai
- Format: 1920×1080, 30 fps
- Duration: 20 seconds
- Audio: subtle background music + restrained UI sound effects; no narration
- Visual source: the real application UI, existing project assets, and project typography/colors
- Safety: never issue a real Shutdown, Restart, Sleep, or Hibernate command during video production

## Story
The video follows one concrete task: schedule a Windows shutdown with Timer Mode, show the app entering an active state, then briefly explain Cancel vs Reset before the branded outro.

## Storyboard
1. 0.0–2.0s — Hook: app icon and “Windows Shutdown Timer”; Thai line “ตั้งเวลาปิดเครื่อง Windows ได้ในไม่กี่ขั้นตอน”.
2. 2.0–5.0s — Show the real app UI; highlight the Shutdown action.
3. 5.0–9.0s — Highlight Timer Mode and animate choosing a duration such as 00:30:00.
4. 9.0–12.0s — Simulate pressing Start without invoking the OS command; transition UI into the same active state the real code would produce.
5. 12.0–16.0s — Show countdown, progress line, active status, disabled Start button, and enabled Cancel button.
6. 16.0–18.0s — Briefly distinguish Cancel from Reset: Cancel aborts an active Windows shutdown/restart; Reset only clears the UI/configuration.
7. 18.0–20.0s — Outro with app icon, “Windows Shutdown Timer”, and “ตั้งเวลา ปิดเครื่องอย่างเรียบง่าย”.
## Verified Runtime Mapping
- Shutdown/Restart scheduling path: `start_timer()` validates the selected Timer/Clock value, calls `shutdown /a`, then calls `shutdown /s|/r /t <seconds>`.
- Active UI state: the app records target time/remaining seconds, enables Cancel, disables Start, starts a 1-second `QTimer`, updates status, and persists settings.
- Countdown path: `update_countdown()` recomputes remaining time, updates `HH:MM:SS`, and updates progress.
- Cancel path: `cancel_timer()` calls `shutdown /a`, stops the local timer, resets UI state, and persists settings.
- Reset path: `clear_fields()` resets fields/configuration only and does not call `shutdown /a`.
- Sleep/Hibernate execute immediately after confirmation and are outside the primary 20-second flow.

## Safe Demo Strategy
Use a dedicated capture harness that imports the real application but replaces the module's `subprocess.run` before the window is created. The replacement must intercept every `shutdown` and `rundll32.exe` request and return a successful no-op result without spawning an OS process. Then drive the real UI through the Shutdown + Timer + Start flow so validation, state transitions, countdown, progress, and button states come from the application's actual logic while no system power action is scheduled.

## Motion
- Favor restrained zooms, cursor movement, button emphasis, and smooth cuts.
- Avoid rapid text, excessive transitions, fake metrics, invented testimonials, or generic SaaS claims.
- Keep all readable Thai text settled long enough to read.

## Validation Before Final Render
- Compare every scene against the current app UI and `shutdown_timer.py` behavior.
- Confirm no subprocess path can invoke `shutdown` or `rundll32.exe` during capture/render.
- Inspect still frames at every scene and transition for clipping, collisions, unreadable Thai text, or low contrast.
- Confirm the complete video is approximately 20 seconds and the poster frame is a settled, readable frame.

## Deliverables
`brag-output/brag.mp4`, `brag-output/brag.jpg`, `brag-output/share-copy.txt`, `brag-output/brag-plan.md`, with intermediates under `brag-output/work/`.