# Journey Lab

The AGCS customer-journey method, as a component. Seven compositions and one
stylesheet — enough to run a three-day lab and produce every artefact it owes.

This is not one journey-map slide but the method — what gets produced on each of
three days, in what order, and why each composition looks the way it does. It
replaces `slides/08-journey-map.html`, which was retired: that slide carried a
client's real session data and a composition that had already been superseded,
and keeping it would have left the catalogue answering the same question twice.

Extracted from CXbD (Customer Journey Lab, 2026), where the recipe lived across
five overlapping CSS modules and one prose document. Content in these cards is
abstract on purpose: "Producto X", "Etapa 01…", no client data.

---

## The three-day method

| Day | The group produces | Composition |
|---|---|---|
| **1** | An **AS-IS** map per group, then a readout | `01-map-as-is` · `04-readout` · `05-overview` |
| **2** | **JTBD** (forces → job story), then a **TO-BE** map | `06-jtbd` · `02-map-to-be` |
| **3** | **DVFR** validation, then a **TO-BE v2** validated map | `07-dvfr` · `03-map-to-be-validated` |

Four groups per lab (A/B/C/D). Each gets its own archetype and picks its own
Moment of Truth. **The maps from a given day are identical in composition and
differ only in content.** That is deliberate and it is the whole exercise:
comparability between groups is what makes the readout possible.

---

## The seven compositions

### 01 · AS-IS map
Four bands: persona stamp, persona panel, the 5×4 matrix, an optional scope
caption. Lanes are **ACTIONS · PAINS · FEELINGS · OPPORTUNITIES**.

The composition is cloned verbatim from STEP 6/6 of the build exercise, so the
recap shows the group exactly what it saw while it was building. Do not tidy it
up afterwards.

### 02 · TO-BE map
`01` unchanged. Lanes become **ACTIONS · SOLUTIONS · FEELINGS · MOVES**, the
panel reads `(TO-BE)`, and the lime marks the *redesigned* Moment of Truth at
the same stage. The group sees its own map repaired in the same frame, cell for
cell — that identity is the argument.

### 03 · TO-BE v2 validated
`02` plus four things, all switched on by `tb2-map` **on `.agcs-canvas`**:
a Carbon `VALIDATED · DAY 3` chip, bold `AJUSTE ·` items in the SOLUTIONS lane,
an Obsidian band of the three committed builds, and an optional scope note
(which needs `has-note` on the canvas for the extra headroom).

### 04 · Group readout
One skeleton for all four groups. Conclusion-first: the 116px headline **is**
the finding, the labelled blocks are the evidence, the lime panel is the
verbatim that earned it. Day 1 blocks: `LO QUE ENCONTRAMOS · EL DOLOR · LA
OPORTUNIDAD · QUÉ SIGUE`. Day 3: `WHAT THE VALIDATION FOUND · THE ADJUSTMENT(S)
· THE JOB · VALIDATED · WHAT'S NEXT`.

### 05 · Four-group overview
The only composition that reads the groups **against each other**: four equal
columns, each closing on its own Moment of Truth. Opens a recap block.

### 06 · JTBD — forces + job story
Christensen's four forces as a 2×2 of hairlines with **no fills** — a fill turns
the matrix into four boxes and loses the fact that the forces are two opposed
pairs. Right, the job story in three parts: `CUANDO / QUIERO / PARA PODER`.

### 07 · DVFR validation step
Desirability / Feasibility / Viability / Responsibility — IDEO's original three
plus the fourth IDEO U added later. Four identical dimension slides, so the group
answers the same shape of question four times. The `WHAT IF` block's top rule is
the lime.

---

## Hard rules

**One lime element per slide. Zero is a defect.** Where it goes is not a choice:

| Composition | The lime is |
|---|---|
| Any map | `.cell.feeling.lime` — the MoT cell in the FEELINGS lane |
| Readout | `.ro-mot` — the whole panel |
| Overview | `.c-mot .chip` — one mark repeated four times, not four accents |
| JTBD | `.jt-chip` (deck) or `.lime-mark` on "para poder" (handbook) |
| DVFR | `.dv-cell.whatif` — its `border-top` |

The corollary is the part that gets forgotten: on a validated map the `AJUSTE ·`
items are **not** lime. The lime is already spent on the Moment of Truth, and a
second one would cost the first its meaning. A bold mono prefix distinguishes
them instead.

**The FEELINGS lane is not decorative.** The face is three SVG primitives and
**the curvature of the mouth is the data**. Never substitute an emoji or a
library icon — an emoji is somebody else's drawing of an emotion, and the lane
exists to carry the group's own reading of it.

**No construction grid on any of these seven.** This is the one documented
exception to the DS grid rule, and the reason is that the matrix *is* a grid:
280px + five equal stage columns against a 60px header and four lanes. A 40px
construction grid behind it is a second grid on a different module, and the two
will never align. Two grids that do not align read as sloppy — which is the same
principle the rule is built on, applied one level up.

The `.journey` panel still carries a solid Paper fill. It costs nothing, and it
keeps the composition correct if a deck ever does put it on a grid slide.

The DS rule in `README.md` and `SKILL.md` names this exemption explicitly, so a
future reader does not "fix" it back.

**Boxes are `<div>`, never `<span>`.** A chip with a border or a fill inside a
`<span>` loses its box in the PPTX export and comes out as highlighted text. The
export walker treats an element whose children are all inline as a text leaf and
stops descending. `span`→`div` is visually transparent inside a flex row.

**Geometry.** 3840×2160, 160px edge padding, absolute positioning, zero viewport
units. Fixed corner rows on all seven.

---

## Typical mistakes

- **Two limes on a validated map.** The `AJUSTE` items look important, so someone
  makes them lime. Now nothing on the slide is the Moment of Truth.
- **Changing the TO-BE composition because it "looks the same".** It is supposed
  to. Cell-for-cell comparability is the deliverable.
- **An emoji in the FEELINGS lane.** See above.
- **Adding the construction grid to a map.** The matrix is already a grid; a
  second one behind it lands on none of the same lines.
- **A `<span>` chip.** Survives the browser, dies in the export.
- **Declaring the subtitle at weight 700.** The Crimson Pro file on disk is 600.
  Ask for 700 and every subtitle in the deck renders light.

---

## Files

| | |
|---|---|
| `journey.css` | The whole module. Imports `../slides/_slide.css`, which owns the canvas, chrome rows, registers and grid. |
| `01`–`07` | One card per composition, 3840×2160, abstract content. |
| `_fit.js` | Scales the canvas to the viewport. Copy of the one in `slides/`. |

### Tokens

Every grey resolves to a design-system token: `--carbon`, `--fg-muted-light`,
`--fg-muted-dark`, `--mist`, `--paper`, `--obsidian`, `--lime`. One does not —
`--jl-head-fill: #F4F4F4`, the stage-header fill. Its nearest neighbour in the DS
is the `#F2F2F2` hardcoded in `slides/_slide.css .jm-head`, a *different* value,
so promoting one to the other would silently restyle the journey-map slide. Left
local and named until that is decided.

### Export

These cards inherit the CXbD host + driver + `_extract-slides.js` contract for
fully-editable PPTX (native shapes, zero raster). Not yet in this repo.
