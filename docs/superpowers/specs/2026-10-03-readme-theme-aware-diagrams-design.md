# README Theme-Aware Diagram Design

## Goal

Make the GitHub README look like a polished project landing page while keeping its technical claims accurate.

## Approved visual direction

- Use a large **Architecture Diagram** as the hero visual.
- Use five smaller diagrams below it: Component, Context, Data Flow, Sequence, and System Context.
- Use SVG rather than PNG for README previews.
- Switch each preview automatically between Light and Dark SVG variants based on the GitHub theme.
- Keep each preview clickable so readers can open the full HTML diagram.

## README structure

1. Project identity: icon, title, concise description, badges.
2. Quick-start installation.
3. Feature summary with accurate scheduled-vs-immediate power behavior.
4. Theme-aware Architecture hero.
5. Theme-aware diagram gallery.
6. Interactive Archify Explorer callout.
7. Under-the-hood runtime flow.
8. Build instructions, ADRs, project layout, changelog, license.

## Rendering contract

Use GitHub-compatible HTML:

- `<picture>`
- dark `<source media="(prefers-color-scheme: dark)" ...>`
- light `<source media="(prefers-color-scheme: light)" ...>`
- `<img>` fallback points to the Light SVG.
- Wrap each `<picture>` in an `<a>` linking to the matching HTML diagram.

Do not duplicate Light and Dark images side-by-side. The active GitHub theme selects the preview automatically.

## Content constraints

- Preserve the verified distinction: Shutdown / Restart are scheduled; Sleep / Hibernate execute immediately.
- Keep Reset vs Cancel behavior explicit.
- Keep the Archify Explorer discoverable without making the README depend on JavaScript.
- Avoid adding generated QA receipts, screenshots, or browser caches to Git.
- Prefer concise sections and progressive disclosure over repeating the same diagram descriptions.

## Verification

Before commit:

- verify all README local links and SVG paths exist;
- verify every Light/Dark SVG parses;
- inspect the README diff for duplicated content and inaccurate runtime claims;
- run `git diff --check`;
- confirm only intended documentation files are staged.
