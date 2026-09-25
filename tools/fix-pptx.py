#!/usr/bin/env python3
"""
fix-pptx.py -- repara un .pptx exportado desde Claude Design.

POR QUE EXISTE
El convertidor a PPTX (PptxGenJS, se ve en docProps/app.xml) no rasteriza:
mapea cada elemento del DOM a una forma nativa de PowerPoint. Eso es bueno
-- el deck sale editable -- pero el formato PPTX no sabe hacer dos cosas que
el sistema AGCS da por hechas, y las dos se vieron en los entregables
descargados el 2026-09-13:

1. GRID. El convertidor no lo entrega de una sola manera: ~150 rectangulos
   sueltos por slide (2026-09-13), un solo rectangulo con degradado que no
   dibuja ninguna cuadricula (2026-09-21, el deck _MALO), o una imagen. Aun
   en el mejor caso son 150 formas que se seleccionan y se arrastran al
   editar, y a los valores viejos (2px, 4%) en una slide de 3840px = 40
   PULGADAS que PowerPoint muestra a un tercio, ni siquiera se ven.
   v5.4: el script lo quita de cada slide, en la forma que venga, y lo
   reconstruye una vez, como rectangulos nativos agrupados a los valores de
   v5.2 (3px, 9% sobre Paper, 11% sobre Obsidian), en un layout propio:
   "AGCS · Grid Paper" / "AGCS · Grid Obsidian". En PowerPoint queda de
   fondo: debajo de todo, no seleccionable, vector, nunca imagen.

2. FUENTE. PPTX no tiene pesos: tiene el booleano bold. Un subtitulo de 600
   sale como typeface="Crimson Pro" con b="1" i="1", y en la familia legacy
   "Crimson Pro" hay Regular, Italic y Bold pero NO Bold Italic. PowerPoint
   no encuentra la cara y sintetiza un falso bold sobre la italica de 400.
   La cara correcta se pide por su nombre legacy: familia
   "Crimson Pro SemiBold", estilo Italic, sin bold.

DONDE ESTA EL ARREGLO DE RAIZ
En el origen, y ya esta hecho en este repo: los valores del grid en
colors_and_type.css (v5.2) y el @font-face con el nombre legacy mas
`--font-subtitle` a peso 400 (v5.3). Este script es la red para los archivos
que salen de una fuente que todavia no tiene esos dos cambios -- hoy, Claude
Design. El grid no tiene arreglo en el origen: el CSS no puede pedirle al
convertidor un layout, asi que esa parte del script siempre trabaja.

LO QUE NO ARREGLA
El .pptx no embebe ninguna fuente (no hay ppt/fonts/ ni embeddedFontLst, y
embeber es una funcion de PowerPoint para Windows). En una maquina sin N27,
Crimson Pro y IBM Plex Mono instaladas se sustituye todo, diga lo que diga
el typeface. Para entrega externa, el PDF es el formato honesto.

USO
  python3 tools/fix-pptx.py deck.pptx -o deck-fix.pptx
  python3 tools/fix-pptx.py deck.pptx -o deck-fix.pptx --solo-grid
"""

import argparse, io, pathlib, re, sys, zipfile
import xml.etree.ElementTree as ET

# El grid se reconstruye en un layout: paso 48px (v5.6, el mismo formato
# que agcs-ui: 16px vistos a 1280), linea 3px (v5.2), negro al 9% sobre Paper, blanco al 11% sobre Obsidian. Todo en
# pixeles del canvas de 3840 y escalado al ancho real del .pptx, para que
# un deck de 13.33in reciba el mismo grid que uno de 40in.
CANVAS_PX   = 3840
STEP_PX     = 48
LINE_PX     = 3
ALPHA_LIGHT = 6000      # negro al 6% sobre Paper      (v5.6; era 9%)
ALPHA_DARK  = 8000      # blanco al 8% sobre Obsidian  (v5.6; era 11%)
ALPHA_MAX   = 12000     # por encima de 12% ya no es una linea de grid
LAYOUT_NAME = {"light": "AGCS · Grid Paper", "dark": "AGCS · Grid Obsidian"}

# Familia que pide el pptx -> familia que PowerPoint sabe encontrar.
# Solo Crimson Pro, y solo en italica. La familia legacy "N27" SI tiene una
# cara Bold propia, asi que typeface="N27" con b="1" resuelve bien y no se
# toca: reescribirla a "N27 Medium" bajaria los titulos de 700 a 500. Igual
# con IBM Plex Mono. El unico peso sin donde caer es el 600 italico.
FACE_FIX = {"Crimson Pro": "Crimson Pro SemiBold"}

SLIDE_PART = re.compile(r"ppt/(slides|slideMasters|slideLayouts)/[^/]+\.xml$")
SLIDE_XML  = re.compile(r"ppt/slides/slide(\d+)\.xml$")
OFF   = re.compile(r'<a:off x="(-?\d+)" y="(-?\d+)"/>\s*<a:ext cx="(\d+)" cy="(\d+)"/>')
SOLID = re.compile(r'<a:solidFill><a:srgbClr val="(000000|FFFFFF)"><a:alpha val="(\d+)"/>')
GRAD  = re.compile(r'<a:gradFill\b.*?</a:gradFill>', re.S)
STOP  = re.compile(r'<a:srgbClr val="(\w{6})">(?:<a:alpha val="(\d+)"/>)?')
BG    = re.compile(r'<p:bg>.*?<a:srgbClr val="(\w{6})"', re.S)
RPR   = re.compile(r"<a:(rPr|defRPr|endParaRPr)\b[^>]*>")
LATIN = re.compile(r'<a:latin typeface="([^"]+)"')


# ---- 1. GRID: encontrarlo en la forma en que venga, y sacarlo de la slide ----
#
# El convertidor no entrega el grid de una sola manera. Se han visto tres:
#   lineas   ~150 rectangulos sueltos de 2-3px, uno por linea (el caso bueno,
#            y aun asi mal: se seleccionan, se arrastran, estorban al editar)
#   smear    UN rectangulo del tamano de la slide con un degradado de negro al
#            9% a transparente -- el linear-gradient del CSS leido como
#            degradado, no como patron. No hay cuadricula, hay una mancha
#            (Slide_deck_about_AGCS_system_MALO.pptx, 2026-09-21)
#   imagen   un PNG del tamano de la slide con el grid rasterizado
# Los tres se quitan de la slide y el grid vuelve como vector en el layout.

def _is_grid_line(sp: str, W: int, H: int) -> bool:
    if "<p:txBody>" in sp or 'prst="rect"' not in sp:
        return False
    g, f = OFF.search(sp), SOLID.search(sp)
    if not (g and f) or int(f.group(2)) > ALPHA_MAX:
        return False
    cx, cy = int(g.group(3)), int(g.group(4))
    thin = 8 * W // CANVAS_PX           # hasta 8px de canvas cuenta como linea
    return (cx <= thin and cy >= 0.9 * H) or (cy <= thin and cx >= 0.9 * W)


def _is_grid_smear(sp: str, W: int, H: int) -> bool:
    if "<p:txBody>" in sp:
        return False
    g, grad = OFF.search(sp), GRAD.search(sp)
    if not (g and grad):
        return False
    cx, cy = int(g.group(3)), int(g.group(4))
    if cx < 0.98 * W or cy < 0.98 * H:
        return False
    stops = STOP.findall(grad.group(0))
    return bool(stops) and all(c in ("000000", "FFFFFF") and a and int(a) <= ALPHA_MAX
                               for c, a in stops)


def _is_grid_image(pic: str, W: int, H: int, media: dict) -> bool:
    """Un PNG a sangre casi todo transparente, con opacidad baja: un grid."""
    g = OFF.search(pic)
    if not g or int(g.group(3)) < 0.98 * W or int(g.group(4)) < 0.98 * H:
        return False
    rid = re.search(r'r:embed="([^"]+)"', pic)
    data = media.get(rid.group(1)) if rid else None
    if not data:
        return False
    try:
        from PIL import Image
    except ImportError:
        return False
    im = Image.open(io.BytesIO(data)).convert("RGBA")
    im.thumbnail((960, 540))
    a = im.getchannel("A").histogram()
    total = sum(a)
    return sum(a[:40]) / total > 0.6 and sum(a[64:]) / total < 0.02


def strip_grid(xml: str, W: int, H: int, media: dict, stats: dict):
    """Quita el grid de una slide. Devuelve (xml, 'light'|'dark'|None)."""
    found, colors = 0, []

    def sp(m: re.Match) -> str:
        nonlocal found
        s = m.group(0)
        if _is_grid_line(s, W, H):
            found += 1; colors.append(SOLID.search(s).group(1)); stats["lineas"] += 1
            return ""
        if _is_grid_smear(s, W, H):
            found += 1; colors.append(STOP.search(GRAD.search(s).group(0)).group(1)); stats["smear"] += 1
            return ""
        return s

    def pic(m: re.Match) -> str:
        nonlocal found
        if _is_grid_image(m.group(0), W, H, media):
            found += 1; stats["imagen"] += 1
            return ""
        return m.group(0)

    xml = re.sub(r"<p:sp>.*?</p:sp>", sp, xml, flags=re.S)
    xml = re.sub(r"<p:pic>.*?</p:pic>", pic, xml, flags=re.S)
    if not found:
        return xml, None
    bg = BG.search(xml)
    dark = (bg and bg.group(1).upper() in ("000000", "1A1A1A")) or (colors and colors[0] == "FFFFFF")
    return xml, ("dark" if dark else "light")


# ---- 2. GRID: reconstruirlo, nativo y agrupado, en un layout ----
#
# En el layout el grid es fondo: PowerPoint lo pinta debajo de todo lo de la
# slide, no se selecciona al editar, no se arrastra, y viaja con la slide si
# se copia a otro deck. Siguen siendo rectangulos nativos, nunca una imagen.

def grid_group(W: int, H: int, tone: str) -> str:
    step = W * STEP_PX // CANVAS_PX
    line = W * LINE_PX // CANVAS_PX
    color, alpha = ("FFFFFF", ALPHA_DARK) if tone == "dark" else ("000000", ALPHA_LIGHT)
    fill = f'<a:solidFill><a:srgbClr val="{color}"><a:alpha val="{alpha}"/></a:srgbClr></a:solidFill>'
    rects, i = [], 100
    def rect(x, y, cx, cy):
        nonlocal i
        i += 1
        rects.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="grid {i}"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr>'
                     f'<p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
                     f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>{fill}<a:ln><a:noFill/></a:ln></p:spPr></p:sp>')
    for k in range(0, (W + step - 1) // step):
        rect(k * step, 0, line, H)
    for k in range(0, (H + step - 1) // step):
        rect(0, k * step, W, line)
    return ('<p:grpSp><p:nvGrpSpPr><p:cNvPr id="100" name="AGCS grid"/>'
            '<p:cNvGrpSpPr><a:grpSpLocks noGrp="1" noUngrp="1" noSelect="1" noMove="1" noResize="1"/></p:cNvGrpSpPr>'
            '<p:nvPr userDrawn="1"/></p:nvGrpSpPr>'
            f'<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{W}" cy="{H}"/>'
            f'<a:chOff x="0" y="0"/><a:chExt cx="{W}" cy="{H}"/></a:xfrm></p:grpSpPr>'
            + "".join(rects) + "</p:grpSp>")


def add_grid_layouts(files: dict, grid_slides: dict, W: int, H: int) -> None:
    """Crea un layout por tono con el grid y apunta cada slide de grid a el."""
    ct = files["[Content_Types].xml"].decode()
    rel_re = re.compile(r'(<Relationship [^>]*Type="[^"]*/slideLayout" Target=")([^"]+)(")')
    for tone in sorted(set(grid_slides.values())):
        first = next(n for n, t in grid_slides.items() if t == tone)
        srels = f"ppt/slides/_rels/slide{first}.xml.rels"
        base = rel_re.search(files[srels].decode()).group(2).split("/")[-1]
        base_xml = files[f"ppt/slideLayouts/{base}"].decode()
        base_rels = files[f"ppt/slideLayouts/_rels/{base}.rels"].decode()
        master = re.search(r'Target="\.\./slideMasters/([^"]+)"', base_rels).group(1)

        k = 1
        while f"ppt/slideLayouts/slideLayout{k}.xml" in files:
            k += 1
        name = f"slideLayout{k}.xml"
        lay = re.sub(r'<p:cSld name="[^"]*"', f'<p:cSld name="{LAYOUT_NAME[tone]}"', base_xml, count=1)
        lay = lay.replace("</p:grpSpPr>", "</p:grpSpPr>" + grid_group(W, H, tone), 1)
        files[f"ppt/slideLayouts/{name}"] = lay.encode()
        files[f"ppt/slideLayouts/_rels/{name}.rels"] = base_rels.encode()
        ct = ct.replace("</Types>", f'<Override PartName="/ppt/slideLayouts/{name}" '
                        'ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/></Types>')

        mpath, mrels = f"ppt/slideMasters/{master}", f"ppt/slideMasters/_rels/{master}.rels"
        mr = files[mrels].decode()
        rid = 1
        while f'Id="rId{rid}"' in mr:
            rid += 1
        mr = mr.replace("</Relationships>", f'<Relationship Id="rId{rid}" Type="http://schemas.openxmlformats.org/'
                        f'officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/{name}"/></Relationships>')
        files[mrels] = mr.encode()
        used = {int(v) for part in files for v in re.findall(r'<p:(?:sldLayoutId|sldMasterId) id="(\d+)"',
                                                               files[part].decode(errors="ignore"))
                if part.endswith(".xml") and ("slideMasters" in part or part == "ppt/presentation.xml")}
        lid = max(used | {2147483648}) + 1
        mx = files[mpath].decode()
        mx = mx.replace("</p:sldLayoutIdLst>", f'<p:sldLayoutId id="{lid}" r:id="rId{rid}"/></p:sldLayoutIdLst>')
        files[mpath] = mx.encode()

        for n, t in grid_slides.items():
            if t == tone:
                p = f"ppt/slides/_rels/slide{n}.xml.rels"
                files[p] = rel_re.sub(lambda m: m.group(1) + "../slideLayouts/" + name + m.group(3),
                                      files[p].decode(), count=1).encode()
    files["[Content_Types].xml"] = ct.encode()


def fix_fonts(xml: str, stats: dict) -> str:
    """
    Pide la cara semibold por su nombre legacy en vez de por bold.

    Los bloques rPr no se anidan, asi que se recorren a mano: uno autocerrado
    no tiene cuerpo y uno abierto llega hasta su cierre. Con una sola regex,
    un rPr autocerrado se tragaba el bloque siguiente y el arreglo alcanzaba
    a un run de cada doce.
    """
    out, i = [], 0
    while True:
        m = RPR.search(xml, i)
        if not m:
            out.append(xml[i:])
            return "".join(out)
        out.append(xml[i:m.start()])
        head = m.group(0)
        if head.endswith("/>"):
            block, i = head, m.end()
        else:
            close = f"</a:{m.group(1)}>"
            j = xml.find(close, m.end())
            j = len(xml) if j < 0 else j + len(close)
            block, i = xml[m.start():j], j
        tf = LATIN.search(block)
        if tf and tf.group(1) in FACE_FIX and ' b="1"' in head and ' i="1"' in head:
            block = block.replace(f'typeface="{tf.group(1)}"', f'typeface="{FACE_FIX[tf.group(1)]}"')
            block = block.replace(head, head.replace(' b="1"', ""), 1)
            stats["font"] += 1
        out.append(block)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--solo-grid", action="store_true", help="no toca las fuentes")
    ap.add_argument("--solo-fuente", action="store_true", help="no toca el grid")
    a = ap.parse_args()

    src, out = pathlib.Path(a.src), pathlib.Path(a.out)
    if src.resolve() == out.resolve():
        print("la salida no puede ser el archivo de entrada", file=sys.stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    stats = {"lineas": 0, "smear": 0, "imagen": 0, "font": 0, "slides": 0}

    with zipfile.ZipFile(src) as zin:
        infos = zin.infolist()
        files = {i.filename: zin.read(i.filename) for i in infos}

    W, H = map(int, re.search(r'<p:sldSz cx="(\d+)" cy="(\d+)"', files["ppt/presentation.xml"].decode()).groups())
    grid_slides = {}
    for name in list(files):
        if not SLIDE_PART.match(name):
            continue
        xml = files[name].decode("utf-8")
        m = SLIDE_XML.match(name)
        if m:
            stats["slides"] += 1
            if not a.solo_fuente:
                rels = files.get(f"ppt/slides/_rels/slide{m.group(1)}.xml.rels", b"").decode()
                media = {rid: files.get("ppt/" + t.replace("../", ""))
                         for rid, t in re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels)}
                xml, tone = strip_grid(xml, W, H, media, stats)
                if tone:
                    grid_slides[int(m.group(1))] = tone
        if not a.solo_grid:
            xml = fix_fonts(xml, stats)
        ET.fromstring(xml)          # si el XML quedo roto, aqui truena
        files[name] = xml.encode("utf-8")

    if grid_slides:
        add_grid_layouts(files, grid_slides, W, H)
        for name in files:
            if name.startswith("ppt/slideLayouts/slideLayout") and name.endswith(".xml"):
                ET.fromstring(files[name])

    tmp = out.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        names = [i.filename for i in infos]
        for name in names + [n for n in files if n not in names]:
            zout.writestr(name, files[name])
    tmp.replace(out)

    formas = [f"{stats[k]} {k}" for k in ("lineas", "smear", "imagen") if stats[k]]
    print(f"{out.name}  ·  {stats['slides']} slides  ·  "
          f"grid en {len(grid_slides)} slides, movido al layout"
          + (f" (llego como {', '.join(formas)})" if formas else "")
          + f"  ·  {stats['font']} runs a Crimson Pro SemiBold")
    ya = sum(1 for n in files if n.startswith("ppt/slideLayouts/slideLayout") and n.endswith(".xml")
             and b'name="AGCS grid"' in files[n])
    if not grid_slides and ya:
        print(f"  el grid ya estaba en {ya} layout(s) AGCS · Grid: nada que mover")
    elif not grid_slides and not a.solo_fuente:
        print("  ! ninguna slide con grid en el archivo: o el deck no lleva grid,\n"
              "    o el origen dejo de exportarlo -- revisalo antes de entregar")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
