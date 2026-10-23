# Design guide

## Direction

A quiet, personal website for Eric Daoud Attoyan: software, music, photography, and writing. Keep the presentation minimal, monochrome, and content-first. Use whitespace and typography rather than decorative UI.

Reference: [Paper project — Personal Website](https://app.paper.design/file/01M58BFC7BW439KVSQE7FDRHYW/p-1-0).

This guide records the implemented design and subsequent decisions. Where the Paper reference differs, follow the decisions below.

## Implementation

- Static Astro site with plain Markdown blog content.
- Shared shell and theme-toggle behavior: `src/layouts/Base.astro`.
- **Theme and typography source of truth: `src/styles/global.css`**, imported by the shared layout.
- Change font family, sizes, weights, line height, and light/dark palettes there. Palette values are defined once; semantic color variables select the active palette.
- Page-specific layout styles live in their `.astro` files and reference shared color and typography tokens; do not introduce literal font sizes or palette values in pages.
- Preserve the existing stack; no UI framework or component library is needed.
- Images are served directly from `public/`.

## Layout

- Center a single column with `max-width: 700px`, including padding.
- Container padding: `3rem 1.5rem`; minimum height: `100vh`.
- Use a vertical flex shell with expanding main content so the footer stays low on short pages.
- Header: name/home link on the left, navigation on the right, aligned on the baseline.
- Navigation labels: `music`, `photography`, `blog`.
- Header bottom margin and footer top margin: `4rem`.
- Header bottom padding and footer top padding: `1rem`.
- **No divider lines in the header or footer.**
- At widths up to `500px`, stack the header with a `0.75rem` gap.

## Typography

Use Inter throughout, self-hosted through `@fontsource/inter` (weights 400, 600, and 700). Font imports and `--font-family` are centralized in `src/styles/global.css`:

```css
font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont,
  'Segoe UI', sans-serif;
```

- Base: `16px`, line height `1.7`.
- Body copy: typically `0.95rem`; paragraphs are justified.
- Page and article titles: `2rem`, weight `600`.
- Site name: `0.95rem`, normal weight (`400`).
- Navigation and dates: `0.9rem`.
- Captions: `0.85rem`, muted.
- Inline links use a thin underline with a `3px` offset.
- Inactive navigation, archive titles, and icon links have no resting underline. The active navigation link is underlined, using the shared thin underline and `3px` offset.

## Color tokens

Use the shared CSS variables in `src/styles/global.css` instead of introducing page-specific colors. Edit `--light-*` and `--dark-*` palette values to change either theme; pages consume the semantic `--color-*` variables.

| Token | Light | Dark | Purpose |
| --- | --- | --- | --- |
| `--color-bg` | `#fafafa` | `#141414` | Page background |
| `--color-text` | `#1a1a1a` | `#e0e0e0` | Main text, active navigation |
| `--color-muted` | `#666` | `#999` | Dates, captions, secondary text |
| `--color-faint` | `#888` | `#777` | Footer icons |
| `--color-border` | `#e0e0e0` | `#333` | Tag borders, code backgrounds, blockquotes |
| `--color-hover` | `#555` | `#bbb` | General link hover |

Avoid gradients, colored accents, shadows, decorative cards, and unnecessary borders.

## Theme and footer

- Follow the system color preference until the user chooses a theme.
- Store the explicit choice in `localStorage` under `theme`; apply it using `data-theme` on the document root.
- Restore a valid saved choice synchronously with an inline script in the document head, before the body renders, to avoid a flash of the system theme. If storage is unavailable, retain the system fallback and keep the toggle usable.
- The toggle icon represents the destination: **sun in dark mode, moon in light mode**.
- Footer left: GitHub and LinkedIn icons only, with a `1rem` gap. Do not restore visible platform labels.
- Footer right: theme toggle.
- Icons are `16 × 16px`, muted at rest, brighter on hover.
- Keep accessible names for icon-only links and buttons.

## Page patterns

Top-level pages do not repeat their navigation label as a visible heading (Music, Photography, Blog). Keep browser-tab titles, article titles, tag archive headings, and the 404 heading.

### Home

- Start directly with the biography.
- Do not repeat the name as a content heading or restore the “Software Engineer & CTO” tagline.
- The name remains in the shared header.

### Blog archive

File: `src/pages/blog/index.astro`.

- Do not show a visible **Blog** page heading; start directly with the year groups.
- No tag filters or selector at the top.
- Sort posts newest first and group by year.
- Desktop: muted year on the left; post list on the right.
- Year grid: `5rem minmax(0, 1fr)` with a `2rem` column gap.
- Separate year groups by `3rem`; separate posts by `1.75rem`.
- Each entry has a linked title (`1.05rem`) above a muted date (`0.9rem`, `0.25rem` top margin).
- Dates use month and day, e.g. “October 21”; the year is shown in the group heading. Format dates consistently in UTC.
- Underline post titles on hover.
- At widths up to `500px`, put the year above its list with a `1rem` gap.

### Blog article

File: `src/pages/blog/[...slug].astro`.

- Title first; date and tags share the next row.
- Metadata uses a wrapping flex row, centered vertically, with a `1rem` horizontal gap and `0.5rem` row gap.
- Tags remain links to their tag archives: `0.8rem` text, thin border, `3px` radius, padding `0.1rem 0.4rem`.
- Allow metadata to wrap naturally on narrow screens.
- Article header bottom margin: `2rem`.
- Content text: `0.95rem`; paragraph bottom margin: `1rem`.
- Images preserve aspect ratio, stay within the content width and `500px` height, and are centered with generous vertical space.
- End with a muted “← back to blog” link.

### Photography

- Keep the short introduction, without a visible page title.
- Display photographs in one vertical column, separated by `3rem`.
- Images fill the column, preserve aspect ratio, and use a subtle `4px` radius.
- Place muted captions below images with `0.75rem` top margin.
- Do not introduce a card grid or crop photographs to uniform tiles.

## Guardrails

- Preserve readable spacing and the narrow editorial column on all screen sizes.
- Use semantic headings, machine-readable dates, descriptive image alt text, and accessible icon controls.
- Keep keyboard focus visible; do not remove browser focus outlines without an equivalent replacement.
- Respect both light and dark themes for every addition.
- Prefer static HTML and CSS; add client-side JavaScript only for necessary interaction.
- After UI changes, run `npm run build` and visually check desktop/mobile layouts in both themes.
