# Visual craft

The small rules that separate a UI that looks finished from one that looks assembled. Each is cheap, each is checkable from a screenshot or the stylesheet, and each applies on every platform: the recipe column is CSS because it is the most common target, and native toolkits apply the same principle with their own API.

How it binds:

- `ui-designer` writes these into the design language and visual specs as tokens and rules. `ui-engineer` and the platform UI builders implement them. `design-director` checks them at `DD-DESIGN-LANGUAGE` and `DD-VISUAL`, and `/app-ux-review` cites a rule by its ID (`VC-07`).
- They are defaults. An app's design language may depart from one with a written reason. A departure with no reason is a finding (usually LOW or MEDIUM by `severity.md`; it is polish, never a release blocker on its own).
- Accessibility and platform convention win a conflict: contrast, focus visibility, reduced motion, forced colors and a native control's own look come first.
- Check browser or toolkit support against the app's `min_targets` before relying on a recipe, and give the newer features a usable fallback (an older declaration first, or `@supports`).

## Shape and edges

| ID | Rule | Why | Recipe |
|---|---|---|---|
| VC-01 | **Nested corners are concentric.** Inner radius = outer radius minus the gap between the two shapes (the outer padding, plus border width if any). Never the same radius on both. | Equal radii make the gap pinch at the corners, so the inner shape looks bolted on | `--radius-inner: max(0px, calc(var(--radius-outer) - var(--pad)));` When the result is zero or less, use square corners or reduce the padding. Define radii as tokens that derive from each other |
| VC-02 | **Borders use alpha, not a solid hex.** A hairline is black or white at low opacity so it takes its tone from whatever is behind it. | A fixed gray is right on one background and muddy or invisible on every other | `border: 1px solid rgb(0 0 0 / 0.1)` in light, `rgb(255 255 255 / 0.1)` in dark; `background-clip: padding-box` so the fill does not show through the border. A control boundary that must be seen still has to measure 3:1 as composited |
| VC-03 | **A ring shadow where a border would shift layout.** | A border adds to the box; a ring does not | `box-shadow: 0 0 0 1px rgb(0 0 0 / 0.08)`, combined with the elevation shadow in one declaration. Keep a real border for forced-colors (`outline: 1px solid transparent` works) |
| VC-04 | **Images get a hairline inner edge.** | A screenshot or photo whose edge matches the page color bleeds into it | `outline: 1px solid rgb(0 0 0 / 0.1); outline-offset: -1px` (white alpha in dark) |

## Color

| ID | Rule | Why | Recipe |
|---|---|---|---|
| VC-05 | **Author color in OKLCH, not HSL.** | HSL lightness is not perceived lightness: yellow and blue at the same L look nothing alike, so ramps and contrast drift per hue. OKLCH keeps perceived lightness steady across hues | `oklch(62% 0.19 255)`. Build each ramp by stepping L with H fixed. Keep chroma inside the sRGB gamut unless a `@media (color-gamut: p3)` variant is supplied. Contrast is still measured, never assumed from L |
| VC-06 | **Gradients interpolate in OKLCH (or OKLab).** | sRGB interpolation passes through a gray, desaturated middle | `linear-gradient(in oklch, var(--a), var(--b))`. Use `in oklab` when the two hues are far apart and the hue sweep is unwanted. Put a plain gradient declaration first as the fallback |
| VC-07 | **Neutrals are tinted, and never pure.** Grays carry a little of the brand hue; text is not `#000` and large surfaces are not `#fff` or `#000` unless the platform's own look calls for it. | Pure gray beside a colored accent looks dead, and pure black on pure white vibrates | `oklch(22% 0.02 <brand hue>)` for text, the same hue at low chroma up the ramp |
| VC-08 | **State colors derive from the base token.** | Hand-picked hover and pressed values drift out of step when the base changes | `color-mix(in oklch, var(--bg) 92%, black)`, or step L in OKLCH. One base token, derived states |
| VC-09 | **White-background product shots use multiply on light surfaces.** | The white box disappears into the surface without re-cutting the image | `mix-blend-mode: multiply` on the image, `isolation: isolate` on its container. Light surfaces only: on a dark surface use a real transparent cutout |

## Depth

| ID | Rule | Why | Recipe |
|---|---|---|---|
| VC-10 | **In dark themes, depth is lightness, not shadow.** Each elevation level is a slightly lighter surface. | A shadow cannot be darker than a dark background, so it does nothing | Step surface L up by 2 to 4 points per level; add a faint top highlight (`inset 0 1px 0 rgb(255 255 255 / 0.06)`) and an alpha border (VC-02). Keep a shadow only as a soft separator |
| VC-11 | **Light-theme shadows are layered and tinted.** Two or three stacked shadows with small alpha, offset downward, tinted toward the surface hue. | One hard black shadow reads as a sticker | `box-shadow: 0 1px 2px rgb(0 0 0 / 0.06), 0 4px 12px rgb(0 0 0 / 0.08)`. Light comes from above everywhere in the product |
| VC-12 | **Text over an image sits on a scrim.** | Image content is unpredictable, so contrast is unmeasurable without one | A gradient scrim under the text, measured against the worst case |

## Type and icons

| ID | Rule | Why | Recipe |
|---|---|---|---|
| VC-13 | **Icon stroke matches the weight of the text beside it.** | A hairline icon next to bold text looks like it came from another product | Starting points for a 16 to 24 px icon: regular text about 1.5 px stroke, medium or semibold about 2 px, bold about 2.5 px. Variable icon fonts (SF Symbols, Material Symbols) take the text weight directly. Icon size follows the text line height, and `currentColor` carries the color |
| VC-14 | **Changing numbers use tabular figures.** | Proportional digits make counters, timers, prices and table columns jitter | `font-variant-numeric: tabular-nums` |
| VC-15 | **Headings balance, paragraphs avoid orphans.** | A last line of one word looks unfinished | `text-wrap: balance` on headings and short labels, `text-wrap: pretty` on body text |
| VC-16 | **Tracking follows size.** Large display text tightens, small all-caps labels loosen. | Default spacing is tuned for body sizes | About -0.01 to -0.03 em on display sizes, +0.04 to +0.08 em on small caps labels |
| VC-17 | **Align optically, not only mathematically.** | Icons, play triangles and text with a leading icon look off-center when centered by their box | Slightly less padding on the icon side of a button; nudge asymmetric glyphs toward their visual center |

## Motion

| ID | Rule | Why | Recipe |
|---|---|---|---|
| VC-18 | **Swapping one icon for another crossfades with a little blur and scale.** | A hard cut reads as a glitch; a soft swap reads as one control changing state (copy to check, play to pause) | Both icons stacked in one grid cell; the outgoing one goes to `opacity: 0; filter: blur(4px); scale: 0.8`, the incoming one reverses it, about 150 to 200 ms. A small blur on an icon-sized element is cheap, which is the exception to the no-filter-animation rule. Reduced motion: instant swap |
| VC-19 | **Name the properties that transition.** | `transition: all` animates layout and theme changes by accident | `transition: background-color 150ms, transform 150ms`. No transition on a theme switch |
| VC-20 | **Easing follows the kind of change.** Ease-out for anything entering, ease-in-out for something already on screen moving from one place to another. | An entrance should arrive fast and settle; a move should leave and land gently. Linear and ease-in entrances feel sluggish | Easing tokens by purpose (`--ease-enter`, `--ease-move`, `--ease-exit`), never a raw curve per component |
| VC-21 | **Short, and exits shorter.** Dropdowns, menus and popovers take 150 to 250 ms; an exit is about 20 percent shorter than its entrance. | Past 250 ms a menu feels like waiting. Something the user dismissed should get out of the way | Duration tokens; the exit token derives from the enter token (`calc(var(--dur-enter) * 0.8)`) |
| VC-22 | **Popovers grow from their trigger and return to it.** They start at about `scale: 0.95` with opacity 0, never from zero and never from their own center, and exit back toward the trigger instead of fading in place. | The motion says where the thing came from and where it went | `transform-origin` set to the trigger's edge or corner (most popover libraries expose it as a variable); the exit reverses the entrance |
| VC-23 | **Press responds at once, and nothing tweens while held.** Buttons scale to 0.97 on press. An element being dragged, scrubbed or resized tracks the pointer directly; easing starts on release. | A transition between the finger and the object feels like lag | `:active { scale: 0.97 }`; transitions switched off for the dragged property during the gesture and restored on release |
| VC-24 | **Stagger groups, briefly.** List rows enter about 30 ms apart; a container's secondary details settle just after the container does. | A group arriving in order reads as one gesture; everything at once reads as a flash | `animation-delay: calc(var(--i) * 30ms)`, capped so the whole stagger stays under about 300 ms (stagger the first rows only on a long list). Never stagger content the user is waiting to read or click |
| VC-25 | **Old and new states overlap.** The outgoing state fades while the incoming one arrives, instead of one finishing before the other starts. | Sequential swaps leave an empty frame and double the wait | Both states in the same grid cell with overlapping transitions, as in VC-18 |
| VC-26 | **One object keeps one identity.** An element that appears in two places (a thumbnail and its detail view, a tab indicator, a card that expands) morphs between them instead of one vanishing and another appearing. | Continuity tells the user it is the same thing | A shared layout ID in the animation library, `view-transition-name` on the web, the platform's shared-element or matched-geometry transition natively |
| VC-27 | **No bounce on everyday UI.** Overshoot and spring wobble are for rare, celebratory or physical moments (a drag released, a sheet thrown), not menus, tabs or buttons used all day. Past a drag boundary the element resists and springs back; it never travels freely or stops dead. | Bounce is charming once and tiring the hundredth time. A hard stop at a boundary feels broken | Critically damped easing by default; rubber-band resistance past the limit (movement scaled down the further it goes) |
| VC-28 | **Success gets a small pulse.** A completed action confirms itself with one short pulse or the icon swap in VC-18 on the control that caused it. | The user should not have to look elsewhere for confirmation | One scale or ring pulse, about 300 ms, once. Never the only signal: pair it with the state change or text |
| VC-29 | **Reveals and color changes wipe with a mask.** Content that unfolds, and a color or theme change that should read as deliberate, are revealed with a mask or clip instead of animating size or fading every element. | Animating height or width reflows the page each frame; a mask does not | `clip-path` or `mask-image` animated on the incoming layer |
| VC-30 | **Expressive physical touches, where they fit the product.** A toggle's knob stretches about 12 percent in the direction of travel while it moves; an object crossing a large distance follows a slight arc, not a straight line. | Small deformation and curved paths make movement feel physical | Optional. Use on products with a playful or tactile character, skip on dense or utilitarian tools, and never on native controls |
| VC-31 | **Hover styles only where hover exists.** | A touch tap leaves a hover state stuck on | `@media (hover: hover) { ... }` |

All of the above yield to reduced motion: movement, scale, stagger, arcs and pulses become a fade or an instant change, and the information they carried stays.

## Layout and scrolling

| ID | Rule | Why | Recipe |
|---|---|---|---|
| VC-32 | **Scrolling edges fade with a mask, not a colored overlay.** Carousels, horizontal chip rows, long lists and tickers. | An overlay gradient must match the background exactly and breaks on images, themes and gradients. A mask fades the content itself over anything | `mask-image: linear-gradient(to right, transparent, #000 24px, #000 calc(100% - 24px), transparent)`. Fade only the edge that has more to scroll to |
| VC-33 | **Full-height layouts use dynamic viewport units.** | `100vh` on mobile Safari is the height with the toolbars hidden, so content sits under the browser chrome | `min-height: 100vh; min-height: 100dvh;` Use `svh` for anything that must not resize as the bars move. Add `env(safe-area-inset-*)` padding on notched devices |
| VC-34 | **Nothing moves when a scrollbar, spinner or late content appears.** | Layout shift looks broken and makes people miss their click | `scrollbar-gutter: stable`, reserved space for images and async content (`aspect-ratio`), skeletons the size of the real thing. Every element is anchored to its container, never positioned by siblings that come and go |
| VC-35 | **The hit area is bigger than the mark.** | Small icons are hard to hit even when they look right | A pseudo-element or padding extends the target to the platform minimum without growing the visual |
| VC-36 | **Scroll containers keep their scroll.** | Scrolling a modal should not drag the page behind it | `overscroll-behavior: contain` on modals, drawers and inner panes |
| VC-37 | **Form text is at least 16 px on phones.** | iOS Safari zooms the page on focus below that | `font-size: max(16px, 1rem)` on inputs |
| VC-38 | **Focus rings follow the shape.** | A square ring on a rounded control looks like a bug | `outline` with `outline-offset`, on `:focus-visible`; the ring's radius is the control's radius plus the offset (VC-01 in reverse) |

## Checking

- From the stylesheet or theme source: search for solid hex borders, `hsl(`, `100vh`, `transition: all`, gradients without an interpolation space, and equal radii on a parent and its padded child.
- From captures (`live-verification.md`): nested corners, borders across both themes, dark-theme elevation, icon weight beside text, and scroll-edge fades are all visible in a screenshot. Motion rules need a short recording or a frame pair.
- A rule that does not apply to the app's toolkit is marked N/A with the reason, not skipped silently.
