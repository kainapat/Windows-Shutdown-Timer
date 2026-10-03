# README Theme-Aware Diagrams Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the README into a polished GitHub project landing page with a large theme-aware Architecture hero and five theme-aware SVG diagram previews.

**Architecture:** Keep README rendering static and GitHub-native. Each preview uses a `<picture>` element with dark/light `prefers-color-scheme` sources and a Light SVG fallback, wrapped in a link to the matching full HTML diagram. Preserve all verified runtime documentation and avoid JavaScript-dependent README behavior.

**Tech Stack:** GitHub Flavored Markdown, GitHub-safe HTML, SVG, existing diagram HTML/SVG exports.

## Global Constraints

- Hero Architecture diagram is large and visually primary.
- Gallery contains Component, Context, Data Flow, Sequence, and System Context.
- GitHub Light uses `*-light.svg`; GitHub Dark uses `*-dark.svg`.
- Every diagram preview links to its matching HTML diagram.
- Shutdown / Restart remain documented as scheduled actions.
- Sleep / Hibernate remain documented as immediate actions.
- Reset vs Cancel behavior remains explicit.
- No QA receipts, screenshots, caches, or browser evidence are added to Git.

---

### Task 1: Restructure README visual hierarchy

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: existing project summary, badges, verified runtime documentation.
- Produces: a concise landing-page flow with Architecture visuals before deep implementation details.

- [ ] **Step 1:** Keep project identity, badges, Getting Started, and verified behavior copy.
- [ ] **Step 2:** Move the Architecture visual section high enough that readers see the system design before long implementation details.
- [ ] **Step 3:** Remove duplicated gallery copy and keep one concise explanation per diagram family.

### Task 2: Add theme-aware SVG previews

**Files:**
- Modify: `README.md`
- Consume: `diagram/*-diagram-light.svg`
- Consume: `diagram/*-diagram-dark.svg`

**Interfaces:**
- Consumes: existing verified Light/Dark SVG exports.
- Produces: GitHub theme-aware hero and gallery.

- [ ] **Step 1:** Add a full-width Architecture hero using:
  ```html
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="diagram/architecture-diagram-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="diagram/architecture-diagram-light.svg">
    <img src="diagram/architecture-diagram-light.svg" alt="Windows Shutdown Timer architecture diagram">
  </picture>
  ```
- [ ] **Step 2:** Add five smaller theme-aware diagram previews using the same contract.
- [ ] **Step 3:** Wrap every preview in an anchor to its matching `*-light.html` full view.
- [ ] **Step 4:** Keep the Interactive Archify Explorer as a separate callout for interactive exploration.

### Task 3: Verify, scrutinize, commit, and push

**Files:**
- Verify: `README.md`
- Verify: `diagram/*.svg`
- Verify: `docs/superpowers/specs/2026-10-03-readme-theme-aware-diagrams-design.md`
- Verify: `docs/superpowers/plans/2026-10-03-readme-theme-aware-diagrams.md`

**Interfaces:**
- Consumes: final README and existing diagram exports.
- Produces: reviewed commits on `main` pushed to `origin/main`.

- [ ] **Step 1:** Parse all twelve Light/Dark SVG files and verify README-local paths exist.
- [ ] **Step 2:** Run `git diff --check`.
- [ ] **Step 3:** Scrutinize the full README against `shutdown_timer.py` for runtime-claim drift and duplicated sections.
- [ ] **Step 4:** Stage only intended documentation changes.
- [ ] **Step 5:** Commit the implementation with a documentation-focused message.
- [ ] **Step 6:** Push `main` to `origin` and verify local and remote HEAD match.
