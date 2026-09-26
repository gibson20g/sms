---
name: Emerald & Cyan Messaging Interface
colors:
  surface: '#faf8ff'
  surface-dim: '#d2d9f4'
  surface-bright: '#faf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f3ff'
  surface-container: '#eaedff'
  surface-container-high: '#e2e7ff'
  surface-container-highest: '#dae2fd'
  on-surface: '#131b2e'
  on-surface-variant: '#3e4947'
  inverse-surface: '#283044'
  inverse-on-surface: '#eef0ff'
  outline: '#6e7977'
  outline-variant: '#bdc9c6'
  surface-tint: '#006a63'
  primary: '#005c55'
  on-primary: '#ffffff'
  primary-container: '#0f766e'
  on-primary-container: '#a3faef'
  inverse-primary: '#80d5cb'
  secondary: '#006398'
  on-secondary: '#ffffff'
  secondary-container: '#5bb8fe'
  on-secondary-container: '#00476e'
  tertiary: '#734700'
  on-tertiary: '#ffffff'
  tertiary-container: '#945d00'
  on-tertiary-container: '#ffe6cc'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#9cf2e8'
  primary-fixed-dim: '#80d5cb'
  on-primary-fixed: '#00201d'
  on-primary-fixed-variant: '#00504a'
  secondary-fixed: '#cce5ff'
  secondary-fixed-dim: '#93ccff'
  on-secondary-fixed: '#001d31'
  on-secondary-fixed-variant: '#004b73'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#faf8ff'
  on-background: '#131b2e'
  surface-variant: '#dae2fd'
typography:
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 38px
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 32px
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 22px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 22px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 18px
  label-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 12px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  margin: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
---

## Brand & Style

This design system establishes a high-performance, contemporary messaging experience bridging the intimate immediacy of personal chats with the structural clarity of professional communication. The target audience encompasses mobile-first digital natives, cross-border communicators, and micro-entrepreneurs who navigate both personal relationships and business transactions within a singular platform.

The visual direction follows **Modern Precision Minimalism** enriched with soft tactile feedback and selective optical translucency. It balances two behavioral modes:
- **Personal Mode:** Warm, direct, human, and low-friction.
- **Professional Mode:** Organized, punctual, auditable, and tool-dense.

The emotional signature is clean, instantaneous, and trustworthy. The interface removes visual noise in favor of stark typographic hierarchy, strict horizontal spatial alignment, and disciplined accent color coding that avoids cognitive fatigue during prolonged screen time.

## Colors

The color palette integrates a deep emerald green (`#0F766E`) representing trust, growth, and personal messaging continuity, paired with an electric telegram cyan-blue (`#0284C7`) designated for enterprise actions, verified accounts, and broadcast streams.

### Semantic Color Assignments
- **Primary (`#0F766E`):** Default send buttons, user's outgoing personal chat bubbles, active navigation states for Personal Mode, active online indicators.
- **Secondary (`#0284C7`):** Professional account toggle, corporate business badge indicators, invoice/payment pills, commercial directory CTAs, outgoing professional chat bubbles.
- **Tertiary (`#F59E0B`):** System notifications, pending deliveries, pinned urgent items, priority status stories.
- **Neutral (`#0F172A`):** High-contrast text on light surfaces, deep tonal ground for elevated bottom sheets.

### Functional Tones & Surfaces
- **App Background (Canvas):** `#F8FAFC` (Cool Crisp Gray)
- **Surface Elevation 01 (Cards, Chat Rows):** `#FFFFFF`
- **Surface Elevation 02 (Segmented Toggles, Input Track):** `#F1F5F9`
- **Bubble Inbound (Received):** `#FFFFFF` with outline `#E2E8F0`
- **Bubble Outbound Personal:** `#0F766E` with text `#FFFFFF`
- **Bubble Outbound Professional:** `#0284C7` with text `#FFFFFF`
- **Borders & Separators:** `#E2E8F0` at `0.5px` hairline density
- **Text Primary:** `#0F172A` (Slate 900)
- **Text Secondary / Timestamp:** `#64748B` (Slate 500)

## Typography

This design system uses **Plus Jakarta Sans** uniformly across display, copy, and UI controls. Its geometric clarity combined with wide aperture terminals delivers maximum legibility on 390px mobile screens, retaining character definition even at tiny metadata scales (timestamps, read receipts, audio duration).

### Hierarchy Rules
- **Conversation Screen Headers:** Use `headline-sm` with a fixed line height of 24px to prevent vertical movement when switching between presence states ("typing...", "online").
- **Message Content:** Standard conversational stream uses `body-lg` (16px) for optimal tap readability. Dense multi-line previews in the primary chat list utilize `body-md` (14px) clamped to a maximum of 2 lines.
- **Micro-Data & Badges:** Use `label-sm` (10px uppercase/bold) for unread counters and commerce tag badges. Timestamps within chat bubbles are positioned in-line using `body-sm` (12px) with 60% opacity.

## Layout & Spacing

The layout is built for fluid single-column execution on mobile viewports (baseline target: 390px width) with systematic density controls.

### Structure & Grids
- **Horizontal Screen Edge Margins:** `1rem` (16px) standard margin to ensure high-speed one-handed thumb reachability without edge touch clip.
- **Horizontal Chat Canvas:** Outbound bubbles inset `48px` from the left edge; inbound bubbles inset `48px` from the right edge.
- **Vertical Spacing Cadence:** 
  - Sequential messages from the same sender: `space-xs` (4px).
  - Transition between different senders: `space-md` (12px).
  - Conversation separation in lists: `space-lg` (16px) with an inner content gutter of `space-md`.

### Reflow Behavior
- On screens wider than 600px (tablets, foldables), the interface transitions into a dual-pane master-detail arrangement where the chat list maintains a fixed width of `360px` with a persistent divider, and the messaging viewport occupies the remaining flex area.

## Elevation & Depth

Visual hierarchy is constructed primarily through **Tonal Layers** supplemented by **Targeted Optical Blurs** to ensure instant perception of layers without visual heaviness.

### Elevation Hierarchy
- **Level 0 (Base Canvas):** Flat `#F8FAFC`. Chat wallpaper patterns must maintain an opacity no greater than 4% to prevent pattern interference with text contrast.
- **Level 1 (List Cells, Message Rows):** Flat `#FFFFFF` separated by hairline borders (`0.5px solid #E2E8F0`). No drop shadow is used for baseline list items to ensure 120Hz scrolling performance.
- **Level 2 (Chat Input Dock & Top App Bar):** Background `#FFFFFF` at 85% opacity with `backdrop-filter: blur(20px)` and an ambient bottom shadow: `0px 4px 20px -2px rgba(15, 23, 42, 0.05)`.
- **Level 3 (Account Switcher, Overlays, Context Menus):** Pure `#FFFFFF` surface with a dual shadow stack:
  - Ambient: `0px 12px 32px -4px rgba(15, 23, 42, 0.08)`
  - Direct: `0px 4px 8px -2px rgba(15, 23, 42, 0.04)`
  - Perimeter: `1px solid rgba(226, 232, 240, 0.8)`
- **Level 4 (Floating Action Buttons):** Outbound dynamic action buttons use high-chroma shadow tinted with the primary hue: `0px 8px 16px -2px rgba(15, 118, 110, 0.3)`.

## Shapes

The interface employs a **Rounded** language (Scale 2), creating ergonomic surfaces that mirror modern handheld industrial hardware.

### Corner Radius Mapping
- **Message Bubbles (Standard):** `16px` border-radius (`rounded-lg`).
- **Message Bubbles (Tailed Corners):** The originating dynamic corner reduces to `4px` (`rounded-sm`) to indicate directionality.
- **Interactive Control Elements (Inputs, Buttons):** `12px` border-radius.
- **Segmented Mode Switchers & Chips:** `9999px` (Pill geometry) for tactile touch targets and instant status discrimination.
- **Avatars & Unread Badges:** Strict circular forms (`round-full`). Verified commercial accounts shift to a squircle (`rounded-md` at 8px) to provide instant visual distinction from personal contacts.

## Components

### 1. Account Switcher (Personal vs. Professional)
- **Geometry:** A high-precision segmented control located directly at the top navigation zone or within the global quick-drawer.
- **Behavior:** Sliding background indicator (`#FFFFFF`) with a micro-shadow over a sunken track (`#F1F5F9`).
- **Style Variations:**
  - *Personal Mode Active:* Primary accent is Emerald (`#0F766E`); icon is a rounded user silhouette; badge style is subtle green.
  - *Professional Mode Active:* Primary accent flips to Cyan (`#0284C7`); icon is a brief-case; quick actions expose invoice generators, catalog links, and quick-reply canned macros.

### 2. Segmented Status Bar (Stories/Updates)
- **Geometry:** Horizontal scrolling carousel at the top of the chat view.
- **Item Styling:** 64px circular avatars bounded by a 2px offset border.
- **Segmentation:** Multiple unviewed status updates divide the stroke border into equal radial SVG dashes (e.g., 3 updates = 3 distinct arcs). Unviewed status uses Emerald (`#0F766E`) for personal contacts and Cyan (`#0284C7`) for commercial entities; viewed status turns to muted `#CBD5E1`.

### 3. Message Bubbles
- **Inbound:** `#FFFFFF` fill, `0.5px` border `#E2E8F0`, Text `#0F172A`. Timestamp right-aligned in `#64748B`.
- **Outbound (Personal):** `#0F766E` fill, no border, Text `#FFFFFF`. Double checkmark status icons rendered in semi-transparent white (`rgba(255,255,255,0.7)`), transitioning to glowing Cyan (`#38BDF8`) when read.
- **Outbound (Professional):** `#0284C7` fill, no border, Text `#FFFFFF`. Contains optional metadata strip for business context (e.g., "Sent via Support Desk").

### 4. Commercial Directory Card (Local Business Guide)
- **Structure:** Card layout with `#FFFFFF` background, `1px solid #E2E8F0`, and `rounded-lg` (16px).
- **Header:** 48px squircle business logo, verified checkmark badge (`#0284C7`), distance chip (e.g., "1.2 km"), and opening hours indicator.
- **Body:** Category tags, promotional micro-banner, and an integrated direct action button: "Chat Now" or "View Catalog".

### 5. Buttons & Interaction Triggers
- **Primary Action (Send/Confirm):** 44x44px minimum circular tap area with `#0F766E` background and white iconography. Scales down to `0.94` transform scale upon active press.
- **Secondary Action:** Outlined 1px `#E2E8F0` with background `#F8FAFC` and text `#0F172A`.
- **Micro Chips:** Pill shape, padding `6px 12px`, background `#F1F5F9`, typography `label-md`. Active states invert to full accent background with white text.

### 6. Inputs & Message Composer
- **Layout:** Bottom dock container with `12px` vertical padding, incorporating expandable dynamic text area (`max-height: 120px`).
- **Composer Field:** Fully enclosed rounded shape (`rounded-xl`), background `#F1F5F9`, no outline in resting state. Gains a `1px` primary border upon active focus.
- **Attachment Dock:** Left-aligned clip icon; right-aligned audio waveform recording button supporting drag-to-lock and slide-to-cancel gestures.