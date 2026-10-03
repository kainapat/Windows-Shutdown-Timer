# HyperFrames Workflow Demo Video — Design Specification

**Project:** Windows Shutdown Timer  
**Date:** 2026-10-03  
**Status:** Approved storyboard / pre-implementation design  
**Primary toolchain:** HyperFrames  
**Supporting skills:** brainstorming, grill-with-docs, scrutinize, domain-modeling

## 1. Goal

Create a polished 45-second product showcase that demonstrates the real workflow of Windows Shutdown Timer while retaining enough clarity to understand how the application is actually used.

The video should feel like a premium technology product film rather than a plain screen recording, but it must preserve the application's real UI and real behavior.

## 2. Audience and Destination

- Primary destination: YouTube / GitHub / Portfolio
- Aspect ratio: 16:9
- Delivery resolution: 1920×1080
- Runtime target: approximately 45 seconds

## 3. Creative Direction

### Visual style

Premium Tech / Cinematic UI.

Use the application's actual visual identity as the design system. HyperFrames should enhance the real UI rather than redesign it.

Motion vocabulary:
- smooth camera push-in / pull-out
- subtle parallax
- soft ambient glow
- light sweeps
- focus rings and highlight masks
- masked zooms
- kinetic typography
- beat-synchronized transitions
- restrained whip/morph transitions
- subtle progress-line illumination

Avoid:
- excessive glitch effects
- aggressive RGB splitting
- unreadable speed ramps
- large particles that obscure controls
- fake or recreated application UI when a real capture can be used

### Audio

- No voice-over
- Modern Electronic / Premium Tech music bed
- UI sound effects used sparingly
- Major transitions and scene reveals should align with musical beats where practical

## 4. Product Truth and Safety Constraints

The film must use real application UI states and verified behavior.

The capture workflow must never execute real operating-system power actions. Shutdown, Restart, Sleep, and Hibernate commands must be intercepted or mocked during capture.

Verified behavioral claims to preserve:

- Shutdown and Restart can be scheduled.
- Timer Mode uses a relative duration.
- Clock Mode uses an absolute date and time.
- Quick Presets include 15m, 30m, 1h, and 2h.
- A running schedule exposes countdown/status/progress UI.
- Cancel aborts an active Windows scheduled shutdown/restart.
- Reset clears the local UI/configuration and does not call `shutdown /a`.
- Sleep and Hibernate are immediate actions after confirmation.
- The application supports English/Thai and Light/Dark presentation.

## 5. Narrative Approach

Chosen concept: **Guided Cinematic Workflow**.

The film should first teach the core scheduling flow clearly, then accelerate into a short feature montage.

Time weighting:
- approximately 30 seconds for the primary workflow
- approximately 10–12 seconds for supporting-feature montage
- approximately 3–5 seconds total for opening and outro

This prevents a 45-second video from becoming an unreadable feature checklist.

## 6. Storyboard

### Scene 1 — Hero Intro
**Time:** 0:00–0:04

Visual:
- dark cinematic background
- Windows Shutdown Timer UI enters as the hero object
- subtle depth/parallax and light sweep

On-screen copy:
- `Windows Shutdown Timer`
- `Schedule shutdown beautifully.`

Motion:
- slow push-in
- soft ambient glow
- typography fade/slide reveal

### Scene 2 — Choose Action
**Time:** 0:04–0:09

Visual:
- move into the real application UI
- highlight Shutdown
- briefly show Restart as the alternate scheduled action

On-screen copy:
- `Choose your action`
- `Shutdown or Restart`

Motion:
- focus ring
- cinematic cursor-style emphasis
- restrained morph/highlight between actions

### Scene 3 — Timer Mode
**Time:** 0:09–0:15

Visual:
- enter Timer Mode
- set `00:30:00`
- briefly reveal `15m / 30m / 1h / 2h` presets

On-screen copy:
- `Set a duration`
- `Timer mode with quick presets`

Motion:
- numeric emphasis
- preset chip pop-in
- beat-synced micro transitions

### Scene 4 — Start Countdown
**Time:** 0:15–0:21

Visual:
- trigger Start using the safe mocked capture path
- transition to active state
- countdown/status/progress become visible

On-screen copy:
- `Start instantly`
- `Live countdown and status`

Motion:
- pre-start to active-state morph
- progress-line glow
- kinetic labels

### Scene 5 — Cancel vs Reset
**Time:** 0:21–0:26

Visual:
- emphasize Cancel and Reset distinctly
- use split or sequential focus treatment

On-screen copy:
- `Cancel ≠ Reset`
- `Cancel aborts the scheduled shutdown`
- `Reset clears the UI only`

Motion:
- split reveal or alternating focus
- stronger alert emphasis for Cancel
- neutral treatment for Reset

This is a key explanatory scene and must remain readable.

### Scene 6 — Clock Mode
**Time:** 0:26–0:31

Visual:
- transition from Timer Mode to Clock Mode
- show real Date Selector and Time Selector
- demonstrate exact scheduling

On-screen copy:
- `Or schedule by exact time`
- `Clock mode`

Motion:
- date/time focus
- soft panel morph
- subtle parallax

### Scene 7 — Instant Actions Montage
**Time:** 0:31–0:35

Visual:
- rapid but readable montage of Sleep and Hibernate
- communicate that these are immediate actions

On-screen copy:
- `Sleep and Hibernate`
- `Immediate actions`

Motion:
- faster cuts
- beat accents
- restrained flash emphasis

No real Sleep or Hibernate action may be executed during capture.

### Scene 8 — Personalization Montage
**Time:** 0:35–0:40

Visual:
- Light ↔ Dark
- EN ↔ TH
- quick UI-detail passes

On-screen copy:
- `Bilingual`
- `Light and Dark themes`

Motion:
- theme wipe
- language-toggle flick
- card glide / soft camera movement

### Scene 9 — Outro
**Time:** 0:40–0:45

Visual:
- return to hero framing
- application settles at center
- branded title and tagline

On-screen copy:
- `Windows Shutdown Timer`
- `Schedule shutdown beautifully.`

Motion:
- slow settle
- ambient glow
- finish on a musical beat

## 7. Capture and Asset Strategy

Use real application captures as the main visual asset.

Preferred approach:
1. Launch the application through the known safe harness that replaces module-level subprocess execution with a fake implementation.
2. Capture native Windows/PySide6 UI states at high quality.
3. Capture each state needed by the storyboard separately to avoid relying on a long live screen recording.
4. Stage those captures inside HyperFrames.
5. Add camera, depth, glow, masks, typography, transitions, and beat synchronization around the real UI.

This approach is preferred over rebuilding the interface in HTML because it preserves product truth while allowing cinematic control.

## 8. HyperFrames Capabilities to Use

Recommended capabilities:
- design spec / frame system based on the real application identity
- motion blueprints for scene reveals and focus treatments
- scene transitions
- user media staged on the timeline
- beat analysis / music-synchronized motion
- media treatments for soft polish and depth
- lightweight SFX

Not required:
- voice generation
- AI presenter
- website capture
- real map scenes
- generative UI replacement

## 9. Readability Rules

- Main UI controls must remain legible at 1080p.
- Do not move the camera while the viewer is expected to read dense copy.
- Keep important text on screen long enough to scan.
- The Cancel vs Reset distinction gets priority over decorative motion.
- Avoid text overlapping application labels.
- Avoid motion blur or glow that reduces UI contrast.
- Preserve safe margins for YouTube/GitHub playback.

## 10. Acceptance Criteria

The design is successful when:

1. The complete main scheduling flow is understandable without narration.
2. The user can distinguish Timer Mode from Clock Mode.
3. The user can understand the difference between Cancel and Reset.
4. Quick Presets, Sleep/Hibernate, Light/Dark, and EN/TH are visibly represented.
5. Real application UI remains the visual source of truth.
6. No real power command executes during capture.
7. Motion feels premium and intentional rather than decorative noise.
8. The final film is approximately 45 seconds, 1920×1080, 16:9.
9. Text, controls, and transitions remain readable at normal playback speed.
10. The final frame clearly identifies Windows Shutdown Timer.

## 11. Approved Decisions

- Complete feature flow: approved
- Runtime: 45 seconds
- No voice-over
- YouTube / GitHub / Portfolio
- 16:9, 1920×1080
- Premium Tech / Cinematic UI
- Storyboard review before build
- Automation execution after approval
- Real UI + cinematic framing
- Feature Tour / App Showcase angle
- Branded outro
- HyperFrames-generated tagline options, current default: `Schedule shutdown beautifully.`
- Main workflow receives most runtime; supporting features appear as montage
- Modern Electronic / Premium Tech music
- Guided Cinematic Workflow concept
- Application's real visual identity remains the design-system source

## 12. Non-Goals

- Rebuilding or redesigning the Windows Shutdown Timer application
- Demonstrating a real machine shutdown
- Creating a long tutorial
- Adding narration
- Turning the film into a neon/cyber or gaming-style edit
- Inventing features not present in the application
