# AGCS UI layer — brand primitives (v3)

The slide-first design system does NOT ship a web UI kit; this folder is the
bridge. It holds the **portable brand primitives** every AGCS product app
vendors (copy-paste, then adapt imports) plus the canonical UX rules
(`../ux-rules.md`).

**Vendoring model (deliberate):** with two apps on different stacks
(`agcs-management-system`: Next 16 + TS + Tailwind v4 · `agcs-dris-system`:
Vite + JS + Tailwind v3) an npm package doesn't pay for itself yet. Each app
copies these files into `src/components/brand/` and adapts the `cn` import.
This folder is the single source of truth — fix here first, then propagate.
Revisit packaging when a third app appears.

## Files

| File | What it is |
|---|---|
| `chevron.jsx` | The `>>` mark, typed in mono. The only repeating glyph. |
| `brand-footer.jsx` | Attribution footer: `AGCS | Studio + Lab |` + `>> Stay Forward`. |
| `lab-stamp.jsx` | Lab register stamp `>> LAB · V[NN]` (top-right, mono). |
| `brand-icon.jsx` | The only "logo" (folder/forward-arrow glyph), 3 variants. |

Reference implementations in production:
- TSX (Next): `agcs-management-system/src/components/brand/`
- JSX (Vite): `agcs-dris-system/src/components/brand/`

## Contract for product UI (summary — full rules in ../ux-rules.md)

- Page header pattern: mono eyebrow (`<Chevron /> SECCIÓN · contexto`, clase
  `.agcs-label`) + display title (N27, `.agcs-display`).
- radius 0 · shadow 0 in the base layer AND in component markup — do not rely
  on the global `!important` alone.
- States: loading = gray skeletons (no shimmer/bounce) · empty = never blank,
  explain + ONE CTA (the view's lime element) · error = qué/por qué/cómo in
  Spanish, conclusion first.
- Dataviz: no pie/donut; ordered horizontal bars; axis from zero; series in
  grays + lime for ONE datum; functional colors (data/warn/risk) exact and
  always with a label.
- Hover = opacity 0.7 or ground inversion. Never elevation, never tint shift.
