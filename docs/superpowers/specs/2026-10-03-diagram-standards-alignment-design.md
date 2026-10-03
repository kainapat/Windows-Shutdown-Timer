# Diagram Standards Alignment Design

## Goal

Bring every project diagram into a clear, standards-aligned role while preserving the existing Light/Dark visual system and README delivery format.

The corrected set must be semantically accurate to `shutdown_timer.py`, visually readable at README scale, and free of text collisions, clipped connectors, broken arrow paths, hidden labels, or misleading boundaries.

## Scope

Update:

- Architecture Diagram
- Component Diagram
- Context Diagram
- Data Flow Diagram
- Sequence Diagram
- System Context Diagram
- Interactive Archify architecture

Regenerate Light and Dark HTML/SVG/PNG outputs from the shared generator where applicable.

## Standards and roles

### Architecture Diagram — runtime layered architecture

Purpose: show the application's major runtime responsibilities and ownership boundaries.

Use four conceptual regions:

1. External Actor
   - Desktop User
2. Presentation
   - PySide6 UI
   - Timer / Clock State
3. Application / Infrastructure
   - Scheduler Controller
   - Countdown Engine
   - Settings Repository
   - Windows Power Gateway
4. External Platform
   - Microsoft Windows

Rules:

- Desktop User is outside the application boundary.
- Windows Power Gateway and Settings Repository are internal application components, not Windows platform components.
- Microsoft Windows is the external platform boundary.
- Primary flow remains left-to-right.
- Keep node count within the diagram-design budget.

### Component Diagram — C4-style component view

Purpose: show the logical components inside the Windows Shutdown Timer application and the dependencies between them.

Container:
- Windows Shutdown Timer [PySide6 Desktop Application]

Components:
- Main Window / UI
- Compatibility Adapters
- Scheduler Controller
- Countdown Engine
- Settings Repository
- Windows Power Gateway
- Theme & Localization

Rules:

- Relationships must follow real call/dependency direction from `shutdown_timer.py`.
- Compatibility Adapters serve UI/backward-compatibility access patterns; they are not the scheduler's upstream controller.
- Settings Repository represents both timer and window JSON persistence.
- Windows Power Gateway owns `shutdown.exe` and `rundll32 / powrprof` invocation.
- External Microsoft Windows may appear outside the application container as the downstream dependency.
- The component diagram must not imply these are separate deployed processes; they are logical components currently co-located in `shutdown_timer.py`.

### Context Diagram — DFD Context / Level 0

Purpose: show the whole application as a single process and only the external entities and major data/control flows crossing its boundary.

Process:
- 0. Windows Shutdown Timer

External entities:
- Desktop User
- Microsoft Windows

Major flows:
- Desktop User → app: power action, Timer/Clock selection, Start/Cancel
- app → Desktop User: confirmation, status, countdown/progress, errors
- app → Microsoft Windows: schedule/cancel/power command
- Microsoft Windows → app: command result/error

Rules:

- No internal component, Local Config, data store, or System State appears in this figure.
- The process boundary represents the entire application.
- Flows should balance with the Level 1 Data Flow Diagram.

### Data Flow Diagram — DFD Level 1

Purpose: decompose the Level 0 application process into internal processes, data stores, and external entities while preserving the same external inputs/outputs.

External entities:
- Desktop User
- Microsoft Windows

Processes:
- 1.0 Capture Request
- 2.0 Validate & Route
- 3.0 Execute / Schedule Power Action
- 4.0 Update UI State
- 5.0 Persist Preferences

Data stores:
- D1 Timer Settings
- D2 Window Preferences

Behavioral accuracy:
- Shutdown / Restart path validates Timer or Clock target, enforces future/non-zero/72h rules, aborts any prior Windows shutdown request, schedules the new command, starts countdown state, and persists timer selections.
- Sleep / Hibernate branches before Timer/Clock validation and executes immediately after confirmation.
- Cancel reaches Windows through `shutdown /a`.
- Window preferences persist theme, language, and window position separately from timer settings.

Rules:
- Use recognizable DFD semantics: external entities, numbered processes, named data stores, labeled flows.
- Do not use role swimlanes or numbered pipeline headers in this figure.
- External flows must balance with the Context Diagram.
- Do not imply timer settings are read or written by Microsoft Windows.

### Sequence Diagram — UML interaction

Purpose: show the actual time-ordered interaction for Start, including the scheduled and immediate branches.

Lifelines:
- Desktop User
- PySide6 UI
- ShutdownTimerApp
- Windows CLI / Power API
- Settings Store

Required flow:
1. User chooses action/time and presses Start.
2. UI invokes `start_timer()`.
3. Controller requests confirmation.
4. User confirms.

`alt` branch A — Shutdown / Restart:
- validate Timer/Clock target
- `shutdown /a` previous Windows request
- `shutdown /s|/r /t <seconds>`
- command result
- start 1-second QTimer/countdown state
- `save_settings()`
- scheduled status/update to UI

`else` branch B — Sleep / Hibernate:
- delegate to immediate execution confirmation
- user confirms
- `rundll32.exe powrprof.dll,SetSuspendState ...`
- command result
- executing status/update to UI

Rules:
- Time flows top-to-bottom.
- Returns use dashed lines with filled arrowheads.
- Use one `alt` combined fragment with two regions.
- Activation bars reflect actual control ownership and must not imply Windows CLI remains active during the application's countdown.

### System Context Diagram — C4 Level 1

Purpose: show the software system in its environment at the highest useful software-architecture level.

People:
- Desktop User

System of interest:
- Windows Shutdown Timer

External software system:
- Microsoft Windows

Relationships:
- Desktop User → Windows Shutdown Timer: configures and controls power actions.
- Windows Shutdown Timer → Microsoft Windows: schedules, cancels, or immediately invokes power operations.
- Windows Shutdown Timer → Desktop User: presents confirmation, countdown/status, and errors.

Rules:

- Do not show Local File System, JSON stores, GitHub Release, or internal runtime components.
- Do not show deployment/distribution concerns in this C4 context diagram.
- Relationship labels state intent, not protocol-level implementation.
- Keep the diagram intentionally sparse.

### Interactive Archify architecture

Purpose: provide an interactive runtime architecture explorer consistent with the corrected static Architecture Diagram.

Nodes:
- Desktop User
- PySide6 UI
- Scheduler Controller
- Countdown Engine
- Settings Repository
- Windows Power Gateway
- Microsoft Windows

Boundaries:
- Windows Shutdown Timer application
- Microsoft Windows platform

Rules:

- Desktop User remains outside the application boundary.
- UI, Scheduler Controller, Countdown Engine, Settings Repository, and Windows Power Gateway are inside the application boundary.
- Microsoft Windows is outside the app and inside the platform boundary.
- `load_settings()` is represented as application initialization/persistence interaction, not as a scheduler-only read.
- Scheduler writes timer settings after successful scheduled/cancel operations as implemented.
- Source references must point to the current verified lines or nearest stable ranges.
- Existing guided views may be retained only when their semantics remain correct after topology changes.

## Visual and geometry acceptance criteria

All static diagrams must satisfy the diagram-design rules and these explicit requirements:

- No text may overlap another text element, node, border, connector, arrowhead, legend, or annotation.
- No connector may be clipped, visually broken, or disappear behind a non-endpoint node.
- Off-axis connectors use rounded orthogonal elbows; no accidental diagonal shortcuts.
- Multiple connectors sharing a node edge use distinct attachment points where required.
- Arrow labels use opaque masks and retain a visible gap from their connector.
- No label mask may overlap a node that is drawn later.
- Sequence lifelines and activation bars must remain continuous and readable through the combined fragment.
- Legends stay in the bottom legend strip and never cover diagram content.
- Light and Dark variants must preserve identical geometry.
- Every SVG keeps `role="img"`, a first-child `<title>`, a meaningful `<desc>`, and unique prefixed IDs.
- README-scale text must remain legible without shrinking below the role/type ramp used by the diagram-design skill.
- Diagram density remains within the appropriate complexity budget; split or simplify rather than shrinking text.

## Output and visual system

- Static diagrams use the existing project Light/Dark palette and typography identity.
- Normalize static diagram canvas to the diagram-design `doc-wide` preset: `1280 × 720`.
- Use the standard role ramp appropriate for documentation; do not shrink node names to force content into the frame.
- HTML remains the source of truth; SVG and PNG are generated/exported from the HTML/SVG body using the existing project workflow.
- README continues to embed the generated SVG variants through theme-aware `<picture>` elements.
- Do not introduce animation into the six static diagrams.

## Verification gates

Before any corrected diagram is accepted:

1. Run the diagram-design `self_check.py` on all 12 Light/Dark HTML outputs.
2. Run project HTML/SVG/PNG render-match verification for all 12 variants.
3. Run an automated geometry check that detects:
   - text-to-text overlap;
   - text intersecting non-parent nodes;
   - label masks intersecting nodes;
   - connectors passing through non-endpoint nodes;
   - duplicate connector attachment points that visually merge;
   - content escaping the SVG viewBox or legend safe area.
4. Browser-render all six Light and six Dark diagrams and inspect representative screenshots at README/document scale.
5. Verify static Light and Dark variants use identical structural geometry.
6. Verify each diagram's claims against the current `shutdown_timer.py` execution paths.
7. Regenerate README previews only after the static artifacts pass all gates.
8. Rebuild/finalize Archify and run its validation/browser visual checks after topology changes.

## Documentation impact

This correction changes diagram semantics and diagram-type discipline, not application behavior or domain terminology.

- No `CONTEXT.md` glossary change is required.
- No ADR is required because the change is documentation alignment rather than a hard-to-reverse runtime architecture decision.
- README diagram descriptions should be updated only where diagram names or scope descriptions become inaccurate after regeneration.
