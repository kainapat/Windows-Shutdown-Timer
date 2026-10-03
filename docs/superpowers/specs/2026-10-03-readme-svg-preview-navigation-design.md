# README SVG Preview Navigation Design

## Goal

Make architecture diagrams behave like the reference IT Assistant README: render crisp Light/Dark SVGs directly in GitHub without turning the diagram image itself into a link to source code.

## Approved behavior

- Keep the Architecture hero plus five focused diagram previews.
- Use `<picture>` with `prefers-color-scheme` for automatic GitHub Light/Dark switching.
- Do **not** wrap any diagram `<picture>` or `<img>` in an anchor.
- Clicking the diagram itself must not navigate to a repository file/code view.
- Use Light SVG as the fallback `<img src>`.
- Keep previews as SVG; PNG remains an export artifact, not the README preview format.

## Explicit links

Below the Architecture hero, provide separate text links:

- Light SVG
- Dark SVG
- Interactive Explorer only when it is hosted as an actual web page.

For the five gallery diagrams, use concise captions and separate Light SVG / Dark SVG links where useful. Do not use an HTML-file link as the click target for the image.

Until GitHub Pages or another static host is configured, label repository HTML files as source/artifact links rather than as a live interactive experience.

## Reference pattern

Follow the pattern used by `kainapatkmutnb/it-course-chatbot-main` on branch `Kainapat-manage-course`: standalone `<picture>` blocks with theme-specific SVG sources and no anchor wrapping the preview.

## Scope

This change is README presentation/navigation only. It does not change runtime behavior, domain vocabulary, or architecture decisions, so no CONTEXT.md or ADR update is required.
