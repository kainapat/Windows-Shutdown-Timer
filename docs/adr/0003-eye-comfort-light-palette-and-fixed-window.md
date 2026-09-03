# ADR 0003: Eye-Comfort Light Palette (#D8D8D8) & Fixed Utility Window Dimensions

## Status
Accepted

## Date
2026-09-04

## Context
Following the initial Raycast/Linear style redesign, user feedback revealed two ergonomic issues during real-world usage:
1. **Unnatural Maximized Layout**: When maximized or resized to large desktop resolutions, an internal vertical stretch pushed the countdown, action, and duration cards to the top of the monitor while stranding the bottom action bar (`Cancel`, `Reset`, `Start Countdown`) at the bottom edge of the screen, creating an awkward 400px empty void in between.
2. **Eye Strain in Light Mode**: The default light mode background (`#f8fafc` pure white/slate) was excessively glaring and caused eye fatigue.

## Decision
1. **Fixed Utility Footprint (580x690 px)**:
   - Establish the application as a dedicated desktop precision utility (comparable to Windows Calculator, Raycast, and Clock widgets).
   - Enforce `setFixedSize(580, 690)`, eliminating the maximize button and preventing disproportionate window stretching.
   - Remove the detached vertical stretch so the bottom action bar connects snugly below the `DURATION` card with standard 10–12px spacing.
2. **Eye-Comfort Light Palette**:
   - Update window and central widget background to soft concrete grey `#D8D8D8`.
   - Use crisp white `#FFFFFF` for card surfaces and input controls with `#C0C0C0` subtle 1px borders.
   - Use `#CECECE` for segmented pill container surfaces with `#B8B8B8` borders.
   - Adjust typography color tokens (`#1e293b`, `#475569`, `#52525b`) to maintain WCAG AAA contrast against `#D8D8D8` and `#FFFFFF`.

## Consequences
- The interface feels solid, cohesive, and intentional regardless of desktop display resolution.
- Eye comfort in light mode is drastically improved with reduced glare.
- Full functional parity is strictly maintained.
