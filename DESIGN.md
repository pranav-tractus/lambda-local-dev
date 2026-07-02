---
name: tract-us-dev
description: Local Lambda orchestration dashboard for the tract-us-backend development team
colors:
  bg: "#07091A"
  surface: "#0D1127"
  surface-hi: "#111830"
  log-bg: "#050710"
  border: "#1C2645"
  border-hi: "#2A3960"
  text: "#C8D8F0"
  text-muted: "#6A87AD"
  text-dim: "#3A5070"
  amber: "#E8930A"
  green: "#34D399"
  red: "#F87171"
typography:
  title:
    fontFamily: "Space Grotesk, system-ui, sans-serif"
    fontSize: "22px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Space Grotesk, system-ui, sans-serif"
    fontSize: "14px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Space Grotesk, system-ui, sans-serif"
    fontSize: "11px"
    fontWeight: 600
    letterSpacing: "0.07em"
  mono:
    fontFamily: "JetBrains Mono, monospace"
    fontSize: "11px"
    lineHeight: 1.7
rounded:
  xs: "4px"
  sm: "5px"
  md: "8px"
  badge: "10px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "12px"
  lg: "14px"
  xl: "24px"
  2xl: "28px"
components:
  button-default:
    backgroundColor: "transparent"
    textColor: "{colors.text-muted}"
    rounded: "{rounded.sm}"
    padding: "4px 10px"
  button-default-hover:
    backgroundColor: "rgba(232,147,10,0.10)"
    textColor: "{colors.amber}"
    rounded: "{rounded.sm}"
    padding: "4px 10px"
  button-start:
    backgroundColor: "transparent"
    textColor: "{colors.green}"
    rounded: "{rounded.sm}"
    padding: "4px 10px"
  button-danger-hover:
    backgroundColor: "rgba(248,113,113,0.08)"
    textColor: "{colors.red}"
    rounded: "{rounded.sm}"
    padding: "4px 10px"
  status-badge:
    backgroundColor: "transparent"
    textColor: "{colors.text-dim}"
    rounded: "{rounded.badge}"
    padding: "2px 7px"
  status-badge-running:
    backgroundColor: "rgba(52,211,153,0.08)"
    textColor: "{colors.green}"
    rounded: "{rounded.badge}"
    padding: "2px 7px"
  status-badge-building:
    backgroundColor: "rgba(232,147,10,0.10)"
    textColor: "{colors.amber}"
    rounded: "{rounded.badge}"
    padding: "2px 7px"
---

# Design System: tract-us-dev

## 1. Overview

**Creative North Star: "The Operator's Console"**

This is purpose-built instrumentation. The visual grammar comes from the analog readout tradition — a dark field, precise numerics, state communicated in light rather than label. Nothing decorates; everything signals. The interface recedes so the engineer can focus on the work behind it: Lambda processes, SAM ports, Cloudflare tunnel URLs. Color appears only when state demands it.

The palette is deep-navy darkness broken by Warm Instrument Amber — the hue that communicates active work on an oscilloscope or industrial control panel. Green for healthy running processes, clipped red for errors. Between actions, the UI is almost monochromatic: an expanse of near-black surface, blue-gray text, and thin borders. The moment a service starts running, the card glows green at the edge.

This system explicitly rejects the following: SaaS dashboards (DataDog, Grafana) — busy widget grids, heavy chrome, persistent sidebars, tooltip forests. Vercel / Linear-style soft minimalism — large rounded cards, heavy white space, shadow stacking, the "product-design-award" register. The Operator's Console is quiet at rest, precise always, and never tries to impress.

**Key Characteristics:**
- Near-black background with tinted navy surfaces — no warm neutrals, no cream, no sand
- Warm Instrument Amber as the sole UI accent; color only carries state
- JetBrains Mono for all data (ports, URLs, log output); Space Grotesk for UI labels and headings
- Compact density — a single card packs service name, port pair, tunnel URL, action buttons, and a live log pane
- Left accent strip as the card's sole expressive element: 3px of state-keyed glow encoding process health


## 2. Colors: The Instrument Palette

One accent, three semantic signals, a full dark neutral scale. Color communicates state; it does not decorate.

### Primary
- **Warm Instrument Amber** (`#E8930A`): The primary accent. Active tab indicator, hover states on default buttons, tunnel URLs, the logo mark, and any "building" or "in-progress" state. Warm like an analog readout — not orange-as-cheerful, not amber-as-warning. The color of process: something is happening.

### Secondary
- **Running Green** (`#34D399`): Reserved for "running" service state — card strip animation, status badge, Start button text color. Never decorative. Always means "healthy and active."

### Tertiary
- **Error Red** (`#F87171`): Danger-action hover states (Clean, Kill Ports buttons) and error conditions. Always means "caution or consequence."

### Neutral
- **Deep Void** (`#07091A`): Body background. Near-black with a blue-navy tint — not pure black.
- **Console Surface** (`#0D1127`): Card background. One lightness step above the body.
- **Lifted Surface** (`#111830`): Tab bars, log panel section headers — a second step up within a card.
- **Log Pit** (`#050710`): Log pane background. Slightly darker than body — the terminal within the terminal.
- **Border** (`#1C2645`): Default border on all surfaces and dividers.
- **Border Hover** (`#2A3960`): Border color on card hover.
- **Primary Text** (`#C8D8F0`): Body and heading text. A cool blue-tinted white — readable against deep navy, never pure white.
- **Muted Text** (`#6A87AD`): Secondary text — port pairs, log output, button labels at rest.
- **Dim Text** (`#3A5070`): Tertiary — summary counts at rest, "— no output —" empty states, placeholder-level context.

### Named Rules
**The Semantic Monopoly Rule.** Amber, green, and red are reserved for state communication. If a new UI element needs color, use amber only for hover/active states and only if it does not conflict with an existing semantic use on the same screen. Decorative use of any signal color is prohibited.

**The Dark Register Rule.** The body bg is always the darkest surface on screen. Every layer above it is lighter. Log panes use `{colors.log-bg}` — they are an intentional downward exception because they represent a terminal context embedded within the UI. No new surfaces may be lighter than the body bg unless they are modal overlays.


## 3. Typography

**UI Font:** Space Grotesk, system-ui, sans-serif
**Data / Mono Font:** JetBrains Mono, monospace

**Character:** A split-register pairing. Space Grotesk carries all navigational and operational text — confident, slightly condensed, legible at 11px. JetBrains Mono carries all data — port numbers, tunnel URLs, log output — where the monospace grid is functional: alignment, precision, no ambiguous glyphs.

### Hierarchy
- **Title** (600 weight, 22px, 1.2 line-height, -0.02em tracking): Service name on detail pages. One instance per screen; the largest text in the system.
- **Headline** (600 weight, 16px, -0.01em tracking): App header title ("tract-us dev"). One instance per screen.
- **Body** (400 weight, 14px, 1.5 line-height): General prose. Rarely appears — this is an operator tool, not a document.
- **Label** (600 weight, 11–12px, 0.07–0.09em tracking, uppercase): Tab bar labels, log panel section headers, status badges. The operational voice — terse, all-caps, uppercase for visual separation from data.
- **Mono** (400 weight, 11px, 1.7 line-height, JetBrains Mono): Port numbers (`:3001 / :8080`), tunnel URLs, all log output lines.

### Named Rules
**The Register Separation Rule.** Never use Space Grotesk for port numbers, URLs, or log lines. Never use JetBrains Mono for UI labels or action buttons. The visual split between UI chrome and data is non-negotiable.

**The Label Ceiling Rule.** Uppercase tracked labels are permitted only on the tab bar and log panel section headers — both are operationally distinct, high-frequency scan targets. Do not introduce new uppercase eyebrow labels above sections, as section dividers, or as navigational markers.


## 4. Elevation

This system uses **tonal layering**, not drop shadows. Depth is expressed through the incremental lightness steps on the blue-navy ramp: body (`#07091A`) → card surface (`#0D1127`) → lifted element (`#111830`). No `box-shadow` on surfaces.

**The single exception:** The card's left accent strip uses an animated `box-shadow` cast sideways to create a pulsing glow for running (`2px 0 16px rgba(52,211,153,0.60)` at peak) and building (`2px 0 14px rgba(232,147,10,0.65)`) states. This is an instrument-panel signal, not a surface elevation effect. `prefers-reduced-motion: reduce` removes the animation; the strip color is preserved.

### Named Rules
**The Flat-By-Default Rule.** All surfaces are flat. The only `box-shadow` in the system is the card strip pulse, and it encodes process state. Any proposed shadow on a card, modal, or dropdown must justify itself against this rule by name.


## 5. Components

### Action Buttons
Transparent at rest, thin-bordered, state-keyed color on hover. Never filled by default.

- **Shape:** Gently rounded (5px — `{rounded.sm}`)
- **Default:** Transparent bg, 1px solid `{colors.border}`, `{colors.text-muted}` text. Hover: amber bg tint (`rgba(232,147,10,0.10)`), amber border, `{colors.amber}` text.
- **Start:** `{colors.green}` text and border at rest. Hover: green tint bg, full green border, green text.
- **Danger (Clean, Kill Ports):** Default style at rest. Hover: red tint bg (`rgba(248,113,113,0.08)`), red border, `{colors.red}` text.
- **Disabled:** 30% opacity, `cursor: not-allowed`. Applied when service is in "building" state — except Kill Ports, which is always active as a recovery action.
- **Padding:** 4px vertical, 10px horizontal. Font: 11px Space Grotesk, 500 weight, 0.04em tracking.
- **Transition:** 150ms on `border-color`, `background`, `color`.

### Status Badge
- **Shape:** Pill (10px radius — `{rounded.badge}`)
- **Default (stopped/unknown):** Transparent bg, `{colors.border}` border, `{colors.text-dim}` text.
- **Running:** `rgba(52,211,153,0.08)` bg, `rgba(52,211,153,0.35)` border, `{colors.green}` text. "RUNNING".
- **Building:** `rgba(232,147,10,0.10)` bg, `rgba(232,147,10,0.35)` border, `{colors.amber}` text. "BUILDING…"
- **Typography:** 10px, 600 weight, 0.08em tracking, uppercase.

### Service Card (Signature Component)
The central unit of the interface. Each card represents one Lambda service.

- **Shape:** 8px radius (`{rounded.md}`)
- **Background:** `{colors.surface}` (`#0D1127`)
- **Border:** 1px solid `{colors.border}`. Hover: `{colors.border-hi}`. 200ms transition.
- **Left Accent Strip:** 3px wide, full card height. Idle: `{colors.border}`. Running: `{colors.green}` + green pulse glow. Building: `{colors.amber}` + amber pulse. `prefers-reduced-motion: reduce` removes animation; strip color is preserved.
- **Internal structure (top to bottom):**
  - Card header: service name (14px, 600) + port pair (JetBrains Mono 11px, `{colors.text-dim}`) + expand icon button + status badge
  - Optional tunnel URL row: amber monospace link at 80% opacity + 16×16px copy button
  - Action buttons row: Start / Stop / Restart / Build / Clean / Kill Ports
  - Tab bar (SAM / PROXY / TUNNEL / BUILD)
  - Log pane (180px fixed, `{colors.log-bg}`, auto-scroll to tail)

### Log Pane
- **Background:** `{colors.log-bg}` (`#050710`)
- **Font:** JetBrains Mono 11px, 1.7 line-height, `{colors.text-muted}`
- **Empty state:** "— no output —" in `{colors.text-dim}`
- **Scrollbar:** 4px width, transparent track, `{colors.border}` thumb, 2px radius
- **Height in card:** 180px fixed. **Height in detail view:** `clamp(200px, calc((100vh - 420px) / 2), 420px)`

### Tab Bar
- **Background:** `{colors.surface-hi}`
- **Border:** 1px solid `{colors.border}` at top
- **Default tab:** `{colors.text-dim}` text, no bottom border. Hover: `{colors.text-muted}`.
- **Active tab:** `{colors.amber}` text, 2px `{colors.amber}` bottom border.
- **Typography:** 11px Space Grotesk, 500 weight, 0.07em tracking, uppercase.

### Tunnel URL Row
- **Font:** JetBrains Mono 11px, `{colors.amber}` at 80% opacity. Hover: full opacity + underline. 150ms.
- **Copy button:** 16×16px, transparent bg, `{colors.text-dim}` icon. Hover: `{colors.surface-hi}` bg, `{colors.border}` border, `{colors.text-muted}` icon. 4px radius.


## 6. Do's and Don'ts

### Do:
- **Do** use Warm Instrument Amber (`#E8930A`) only for active/hover states, "building" status, tunnel URLs, and the logo mark. Its rarity is what makes it signal rather than noise.
- **Do** use JetBrains Mono for every port number, tunnel URL, and log output line — without exception. Space Grotesk is for UI; JetBrains Mono is for data.
- **Do** keep card backgrounds at `{colors.surface}` (`#0D1127`) against the body bg `{colors.bg}` (`#07091A`). The one-step contrast is intentional; do not collapse it by using the same value for both.
- **Do** keep action buttons transparent at rest. Filled-at-rest belongs to marketing UIs; this is an operator tool.
- **Do** respect `prefers-reduced-motion: reduce` — remove the card strip pulse animation, preserve the strip color.
- **Do** keep Kill Ports always enabled regardless of service state. It is a recovery action; disabling it would prevent recovery.
- **Do** use the left accent strip exclusively for encoding process state (idle / running / building). It is the card's signature; don't repurpose it.

### Don't:
- **Don't** introduce widget-heavy chrome, persistent sidebars, or dense toolbar rows. This is not a SaaS monitoring dashboard (DataDog, Grafana).
- **Don't** use large rounded cards, heavy white space, shadow stacking, or the Vercel / Linear soft-minimalism register.
- **Don't** add warm neutral backgrounds — no cream, sand, linen, paper, beige, or any color in the OKLCH L 0.84–0.97 / C < 0.06 / hue 40–100 band. The dark blue-navy register is non-negotiable.
- **Don't** use color decoratively. Amber, green, and red carry semantic meaning; using them for visual interest corrupts the signal the entire UI depends on.
- **Don't** add uppercase tracked eyebrow labels above new sections. The tab bar and log panel headers are the only permitted uppercase contexts.
- **Don't** use `border-left` greater than 1px as a colored stripe on new cards or callouts. The left accent strip is the service card's signature — reuse corrupts the encoding.
- **Don't** use `background-clip: text` gradient text on any element. All text is a single solid color.
- **Don't** use `box-shadow` on surfaces for depth. Tonal layering only. The card strip pulse glow is the sole permitted shadow.
- **Don't** invent new accent colors. Amber, green, and red are the complete signal vocabulary. A fourth color would break the semantic clarity.
