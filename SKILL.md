---
name: agcs-design
description: Use this skill to generate well-branded interfaces and assets for AGCS | Studio + Lab, either for production or throwaway prototypes/mocks/etc. Contains essential design guidelines, colors, type, fonts, assets, and slide layouts for prototyping.
user-invocable: true
---

Read the README.md file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create static HTML files for the user to view. If working on production code, you can copy assets and read the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design, ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code, depending on the need.

## Hard constraints (do not violate)

1. **Color is restricted.** Core: Obsidian `#000000`, Paper `#FFFFFF`, **Lime `#C8FF29`** (v3, applied 2026-08-27; legacy v2 `#BEFF3A`. Must equal the icon library, whose baked PNGs were regenerated to this value), Carbon `#1A1A1A`, Mist `#E5E5E5`. **v3 functional palette (2026-07-20), role-bound and exact:** Data blue `#00A1F1` (data viz / system / information layers), Signal yellow `#FFFF00` (warnings / attention), Signal red `#ED1C24` (risk / critical / blockers). Functional colors are never decorative. **Any OTHER blue, green, amber, red, purple, or any gradient stays off-brand** -- decorative blues still put AGCS in the McKinsey / BCG / Deloitte cluster.
2. **Lime marks ONE point of focus per slide** -- the single thing the eye should land on: the topic icon, OR one chart bar, OR one table cell, OR one numerical callout, OR one diagram node. Never two. Never as background, body text, or decoration.
   - **The eyebrow chip is exempt.** `.chip-lime` (`RESULTS`, `WHAT'S NEXT`) is a tag that classifies the slide, not an accent competing for attention. A slide may carry one lime chip *and* one lime focus element -- that is the cover pattern. It may never carry two focus elements.
   - Practically: chip + lime topic icon = correct. Lime chart bar + lime topic icon = wrong, the icon goes `negro/`.
3. **Titulo = N27** (Bold 700, Medium 500; Regular 400 is reserve). **Sub titulo = IBM Plex Sans** (v3). **Texto / data / labels = IBM Plex Mono** (Regular 400, Medium 500). **Crimson Pro Italic = the reflective line** -- the pull quote, and the one-line promise under a cover or sign-off title (`.deck-line`). One instance per slide, never body copy, never labels. All families load LOCALLY via `@font-face` from `fonts/` -- zero CDN. The system is monospace-dominant.
4. **The Insight slide line-height is `0.92`** -- descenders intentionally touch cap-height below. Do not "fix" this.
5. **No emoji, no third-party icon sets (Lucide, Heroicons, Material, SF Symbols), no decorative SVG.** The chevron `>>` (typed mono) is the only repeating glyph in text. When iconography is required, use **only** the proprietary AGCS icon library in `assets/icons/` -- see the *Iconography* section of README.md. On slides, an icon in the `verde1` (lime) colorway counts as the slide's single Lime element.
6. **Zero radius, zero shadow.** Hierarchy comes from whitespace, ground inversion (Paper ↔ Obsidian) and the construction grid — never elevation.
7. **Canvas is 4K 16:9 (3840x2160)** for slides.
8. **Every slide picks a register** with one class on `.agcs-canvas`: `reg-studio` or `reg-lab`. Never fork a layout to change register, and never hard-code a band fill or band text color in slide HTML -- the register owns them.
   - **Studio** (`reg-studio`) -- Obsidian header band (30% on dividers, 22% on content), page number top-right. Weight and authority; the client-facing deck.
   - **Lab** (`reg-lab`) -- Paper ground, band reduced to a 1px Mist hairline, **construction grid full-bleed**, `>> LAB - v[N]` stamp top-right. The scaffolding shows. The grid is the Lab's signature -- it is what makes the register readable across the room, so it runs edge to edge, never boxed inside a sub-region.
9. **Every slide carries one topic icon on the right.** It is mandatory, and it must relate to what that slide argues -- never a generic mark.
   - The **system** owns the slot: `class="topic-icon"`, right margin `--pad-slide`, 640px default (`--icon-size` to override), `.is-hero` for the oversized cover treatment.
   - The **deck** owns the choice: which file from `assets/icons/`. That is editorial and does not belong in this skill.
   - **Colorway follows the ground, not taste:** `negro/` on Paper, `blanco/` on Obsidian, and `verde1/` **only when nothing else on the slide is lime** -- a lime icon *is* the slide's single lime element (rule 2). A slide with a lime chart bar takes a `negro/` icon.

## Key files in this skill

- `README.md` -- voice, visual foundations, font substitutions, iconography rules.
- `ui/` -- **the product-UI layer (v3)**: portable brand primitives (`chevron.jsx`, `brand-footer.jsx`, `lab-stamp.jsx`, `brand-icon.jsx`) that product apps vendor into `src/components/brand/`. See `ui/README.md` for the vendoring contract.
- `ux-rules.md` -- canonical UX & accessibility rules for product apps (states, dataviz, hierarchy without elevation, forms/gates). Subordinate to the brand rules above.
- `colors_and_type.css` -- drop-in stylesheet with all tokens (`--obsidian`, `--lime`, `--font-mono`, `--t-insight`, ...) and semantic classes (`.agcs-insight`, `.agcs-quote`, `.agcs-label`).
- `assets/agcs_mark_{white,black,lime}.svg` -- **the AGCS mark**, used at size on the logo slide only. Note `assets/agcs_lab_icon_*.svg` are NOT the mark: all four hold the same document-and-arrow *topic icon*.
- `assets/icons/` -- the proprietary AGCS icon library: `alxgdo/` (34 line icons in negro / blanco / verde1-lime / verde2 / verde3 + `animation.gif`), `icons-grid/` (16 icons drawn on the construction grid, 4 colorways), `new-icons/` (11 newer icons, 4 colorways), `grid-templates/` (14 construction grids + principal, black & white), `_source/ICONOS.pdf`. New work uses **negro on Paper, blanco on Obsidian, verde1 as the one lime accent**.
- `slides/01-cover.html` ... `slides/07-system-lab.html` -- the 7 canonical layouts. Copy and adapt; don't re-invent.
- `slides/index.html` -- flip through all 7 in a deck-stage shell.

## Voice cheatsheet

- Conclusion-first headlines. "X is true," not "we believe X."
- 2-3 line paragraphs in mono. Numbers are evidence, never decoration.
- Sentence case in body. ALL CAPS allowed only in short mono labels (`INTRO`, `SYNTHESIS`, `Q1`, `>> LAB · V03`).
- Spanish-primary; quoted English thinkers stay in English.
- Tagline: `>> Stay Forward`. Attribution: `AGCS | Studio + Lab |` (spaces around `+`).
