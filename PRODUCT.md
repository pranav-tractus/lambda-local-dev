# Product

## Register

product

## Users

Small team of 2–5 engineers working on the tract-us-backend project. Each developer runs the tool in their own local environment. Context: mid-workflow, heads-down in a terminal, running multiple Lambda functions simultaneously and needing to quickly check status, restart services, and grab tunnel URLs without breaking focus.

## Product Purpose

Local development orchestration UI for tract-us-backend AWS Lambda functions. Surfaces the runtime status of up to 6 SAM-local Lambda services and their Cloudflare tunnels in a single view. Primary tasks: start/stop/restart/build services, monitor per-process logs, copy tunnel URLs, kill port conflicts. Success means zero context-switching to the terminal for routine operational checks.

## Brand Personality

Precise · Minimal · Fast

Internal developer tool; voice is direct and terse. No marketing language. State is communicated immediately; actions have no ceremony.

## Anti-references

- **SaaS dashboards (DataDog, Grafana)**: Busy, widget-heavy, lots of chrome, sidebar navigation, dense tooltip overlays. This tool has no nav chrome, no sidebar, no widget grid.
- **Vercel / Linear style**: Slick soft-minimalism, heavy white space, large rounded cards, subtle shadow layering. This tool lives in the terminal register, not the product-design-award register.

## Design Principles

1. **Signal over structure** — every visual element earns its place by communicating state. No decorative chrome, no empty section headers.
2. **Respect the terminal** — stay in the aesthetic register developers already trust: monospace data, deep dark backgrounds, amber/green status semantics.
3. **Density serves speed** — pack information when it reduces clicks; don't pad for visual comfort.
4. **Quiet when idle, loud when active** — color communicates state (green = running, amber = building, red = error). Silence is the default.
5. **Zero ceremony** — actions are immediate, confirmations are rare. The tool does not get in the way of the workflow it serves.

## Accessibility & Inclusion

No formal WCAG compliance required (internal dev tool). Respect `prefers-reduced-motion` for animations. Maintain readable contrast for extended use in dark environments.
