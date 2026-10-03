# Diagram Standards Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Regenerate all six static diagrams and the interactive Archify diagram so each uses the correct architecture/DFD/UML semantics, matches the real application behavior, and passes strict geometry/readability checks.

**Architecture:** Keep `diagram/generate_diagrams.py` as the single source for static HTML/SVG geometry, add focused primitives for C4-style relationships, DFD entities/processes/data stores, and UML sequence returns/fragments, and keep export/README workflows unchanged. Add a project-side geometry validator so overlap and connector regressions are caught automatically. Update `diagram/interactive/candidate.json` to mirror the corrected runtime architecture.

**Tech Stack:** Python, inline SVG/HTML, Playwright/Chrome export, Diagram Design checks, Archify CLI, Git.

## Global Constraints

- Static canvas: `1280 × 720`.
- Light and Dark variants use identical geometry.
- No text overlaps text, nodes, borders, connectors, arrowheads, legends, or annotations.
- No connector is clipped, broken, or routed through a non-endpoint node.
- Off-axis connectors are rounded orthogonal elbows.
- Architecture/System Context/Component semantics follow the approved C4-aligned roles.
- Context Diagram is DFD Context / Level 0.
- Data Flow Diagram is DFD Level 1 and balances with the Context Diagram.
- Sequence Diagram uses one UML `alt` fragment and dashed filled returns.
- README keeps theme-aware SVG previews.
- Runtime code is not modified.

---

### Task 1: Rebuild static diagram semantics and geometry

**Files:**
- Modify: `diagram/generate_diagrams.py`
- Regenerate: `diagram/*-diagram-{light,dark}.{html,svg}`
- Regenerate: `diagram/*-diagram-{light,dark}.png`

**Interfaces:**
- Consumes: verified behavior in `shutdown_timer.py`.
- Produces: six corrected Light/Dark diagram pairs with consistent geometry.

- [ ] **Step 1:** Set `VIEW_W, VIEW_H = 1280, 720`; reserve header/content/legend safe areas.
- [ ] **Step 2:** Add reusable primitives for C4/system boxes, DFD external entity/process/data store, relationship arrows, sequence call/return arrows, and fragment regions.
- [ ] **Step 3:** Replace `architecture_body()` with the approved runtime layered architecture.
- [ ] **Step 4:** Replace `component_body()` with the approved C4-style component view and external Windows dependency.
- [ ] **Step 5:** Replace `context_body()` with DFD Level 0: one process, Desktop User, Microsoft Windows, balanced external flows.
- [ ] **Step 6:** Replace `data_flow_body()` with DFD Level 1: 5 numbered processes, D1/D2 stores, two external entities, scheduled/immediate/cancel flows.
- [ ] **Step 7:** Replace `sequence_body()` with the verified UML interaction and one two-region `alt`.
- [ ] **Step 8:** Replace `system_context_body()` with strict C4 Level 1: Desktop User, Windows Shutdown Timer, Microsoft Windows only.
- [ ] **Step 9:** Regenerate HTML/SVG with `python diagram/generate_diagrams.py`.
- [ ] **Step 10:** Export PNG with `python diagram/export_png.py`.

### Task 2: Add geometry regression validation

**Files:**
- Create: `diagram/verify_geometry.py`
- Modify if needed: `diagram/verify_render_match.py`

**Interfaces:**
- Consumes: generated SVG files.
- Produces: PASS/FAIL geometry report for all 12 static SVG variants.

- [ ] **Step 1:** Parse SVG geometry and collect node rectangles, text anchors, connector paths/lines, masks, and legend boundary.
- [ ] **Step 2:** Fail on text bounding-box collisions using deterministic width estimates for Geist/Geist Mono/Instrument Serif.
- [ ] **Step 3:** Fail when connector line segments intersect non-endpoint node interiors.
- [ ] **Step 4:** Fail when label masks overlap non-endpoint nodes or content escapes the viewBox/safe legend region.
- [ ] **Step 5:** Run `python diagram/verify_geometry.py` and correct every reported collision.

### Task 3: Synchronize Interactive Archify topology

**Files:**
- Modify: `diagram/interactive/candidate.json`
- Regenerate/finalize: `diagram/interactive/index.html`

**Interfaces:**
- Consumes: corrected runtime architecture from Task 1.
- Produces: interactive architecture with the same ownership boundaries and verified source references.

- [ ] **Step 1:** Move Desktop User outside the application boundary and keep UI, Scheduler Controller, Countdown Engine, Settings Repository, and Windows Power Gateway inside it.
- [ ] **Step 2:** Represent Microsoft Windows as the external platform dependency.
- [ ] **Step 3:** Replace scheduler-only settings read semantics with initialization/persistence wording that matches `load_settings()` and `save_settings()`.
- [ ] **Step 4:** Update source ranges to current verified code locations.
- [ ] **Step 5:** Finalize/rebuild Archify with the installed CLI and fix every validation/layout diagnostic.
- [ ] **Step 6:** Browser-check node focus, route probe, Light/Dark rendering, and source links.

### Task 4: Full QA, README synchronization, commit, and push

**Files:**
- Modify if wording changed: `README.md`
- Verify: all generated diagram HTML/SVG/PNG files.
- Verify: `diagram/interactive/index.html`

**Interfaces:**
- Consumes: Tasks 1–3 outputs.
- Produces: reviewed and pushed documentation artifacts.

- [ ] **Step 1:** Run Diagram Design `self_check.py` against all 12 static HTML files; expected: all OK.
- [ ] **Step 2:** Run `python diagram/verify_render_match.py`; expected: all 12 MATCH.
- [ ] **Step 3:** Run `python diagram/verify_geometry.py`; expected: all 12 PASS with zero collisions.
- [ ] **Step 4:** Browser-render all six Light and six Dark static diagrams and inspect contact sheets at README scale.
- [ ] **Step 5:** Check Context ↔ Level 1 DFD balancing and trace Sequence/Architecture claims against `shutdown_timer.py`.
- [ ] **Step 6:** Update README captions/descriptions only where old scope wording is inaccurate.
- [ ] **Step 7:** Verify README has six theme-aware SVG `<picture>` blocks and no diagram image anchor wrappers.
- [ ] **Step 8:** Run `git diff --check`, stage only intended documentation/diagram files, and inspect the complete diff.
- [ ] **Step 9:** Commit corrected diagrams and push `main`.
- [ ] **Step 10:** Verify local HEAD equals remote `refs/heads/main`.
