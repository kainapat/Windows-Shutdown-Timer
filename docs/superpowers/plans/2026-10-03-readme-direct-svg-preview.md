# README Direct SVG Preview Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make all README architecture diagrams render as direct theme-aware SVG previews without making the images themselves navigate to GitHub code views.

**Architecture:** Keep the existing six Light/Dark SVG exports as the only README preview assets. Remove anchor wrappers from every diagram `<picture>`, keep GitHub-native `prefers-color-scheme` switching, and expose explicit text links for Light SVG, Dark SVG, and HTML artifact/source where useful. Do not deploy GitHub Pages in this change.

**Tech Stack:** GitHub Flavored Markdown, GitHub-safe HTML, SVG, existing diagram exports.

## Global Constraints

- Architecture remains the large hero visual.
- Component, Context, Data Flow, Sequence, and System Context remain the five gallery previews.
- Diagram images must not be wrapped in `<a>` elements.
- GitHub Light uses `*-light.svg`; GitHub Dark uses `*-dark.svg`.
- Light SVG remains the fallback `<img src>`.
- HTML files are described as repository artifacts/source, not live interactive pages.
- No runtime code, CONTEXT.md, or ADR behavior changes are part of this implementation.

---

### Task 1: Remove image navigation and clarify architecture links

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: existing `diagram/*-light.svg`, `diagram/*-dark.svg`, and `diagram/*.html`.
- Produces: direct SVG previews and explicit navigation links.

- [ ] **Step 1:** Remove the `<a>` wrapper around the Architecture hero `<picture>`.
- [ ] **Step 2:** Replace the misleading live Interactive Explorer wording with explicit `Light SVG`, `Dark SVG`, and `HTML artifact` links.
- [ ] **Step 3:** Change the header navigation so it points to the Architecture section rather than directly to an unhosted HTML file.

### Task 2: Convert gallery previews to non-clickable SVG pictures

**Files:**
- Modify: `README.md`

**Interfaces:**
- Consumes: the five existing Light/Dark SVG pairs.
- Produces: five non-clickable, theme-aware gallery previews.

- [ ] **Step 1:** Remove all anchor wrappers from Component, Context, Data Flow, Sequence, and System Context `<picture>` blocks.
- [ ] **Step 2:** Keep `<source media="(prefers-color-scheme: dark)">`, `<source media="(prefers-color-scheme: light)">`, and Light fallback `<img>` for each diagram.
- [ ] **Step 3:** Add explicit caption links for each diagram: Light SVG · Dark SVG · HTML artifact.

### Task 3: Verify GitHub rendering, review, commit, and push

**Files:**
- Verify: `README.md`
- Verify: `diagram/*-diagram-{light,dark}.svg`

**Interfaces:**
- Consumes: the final README and committed SVG exports.
- Produces: a reviewed `main` branch pushed to `origin/main`.

- [ ] **Step 1:** Parse all 12 SVG files and verify every README-local path exists.
- [ ] **Step 2:** Confirm there are exactly six `<picture>` blocks, six dark sources, and six light sources.
- [ ] **Step 3:** Confirm no diagram `<picture>` has an ancestor `<a>` in the rendered GitHub README.
- [ ] **Step 4:** Verify Light mode resolves to `*-light.svg` and Dark mode resolves to `*-dark.svg`.
- [ ] **Step 5:** Run `git diff --check` and scrutinize the README wording for misleading live/interactivity claims.
- [ ] **Step 6:** Commit the README implementation and push `main` to `origin`.
- [ ] **Step 7:** Verify local HEAD and remote `refs/heads/main` match.
