# /fonts -- Local font slot

Local-only delivery for the AGCS type system. Several client deployments (banking, government, regulated industries) sit behind networks that block `fonts.googleapis.com` -- everything that touches the workhorse path lives here.

## Installed -- loaded by `colors_and_type.css`

### N27 (display, headings, covers, insight headlines)

```
N27-Regular.otf    (weight 400 -- reserve; confirm with Max before use)
N27-Medium.otf     (weight 500 -- subheads)
N27-Bold.otf       (weight 700 -- display, insight headlines, covers)
```

### IBM Plex Mono (body, data, labels, stamps, footers)

```
IBMPlexMono-Regular.ttf    (weight 400 -- the default body face)
IBMPlexMono-Medium.ttf     (weight 500 -- emphasis runs, used sparingly)
```

### Crimson Pro (quote slide layout only)

```
CrimsonPro-Italic.ttf      (weight 400 italic -- the only quote face)
```

All three families are referenced via `@font-face` blocks at the top of `../colors_and_type.css`. Each block tries `local()` first, then falls back to the bundled file here. **Zero CDN dependencies** -- the system runs fully air-gapped.

## `_reserve/` -- NOT loaded

```
_reserve/N27-Thin.otf            _reserve/N27-ThinItalic.otf
_reserve/N27-ExtraLight.otf      _reserve/N27-ExtraLightItalic.otf
_reserve/N27-Light.otf           _reserve/N27-LightItalic.otf
_reserve/N27-RegularItalic.otf
_reserve/N27-MediumItalic.otf
_reserve/N27-BoldItalic.otf

_reserve/CrimsonPro-Regular.ttf
_reserve/CrimsonPro-Light.ttf
_reserve/CrimsonPro-ExtraLight.ttf
_reserve/CrimsonPro-Medium.ttf
_reserve/CrimsonPro-SemiBold.ttf
_reserve/CrimsonPro-Bold.ttf
```

These weights ship with the N27 license bundle but are NOT part of the v2 system. They are kept on disk so any future promotion is a one-line CSS change, not a re-licensing round-trip. Do not reference them from system styles without confirming with Max -- the brand's two-weight discipline is intentional.

## What's NOT here

- **IBM Plex Sans** -- not a system family. The brand is monospace-dominant by design; a sans body would dilute the signature.
- **Graphik** -- legacy from a previous identity, not part of v2.

## License notes

- **N27** -- commercial license, do not redistribute. Keep these `.otf` files inside the AGCS project tree only.
- **IBM Plex Mono** -- SIL Open Font License 1.1. Bundling and redistribution explicitly permitted.
- **Crimson Pro** -- SIL Open Font License 1.1. Bundling and redistribution explicitly permitted.
