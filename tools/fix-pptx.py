#!/usr/bin/env python3
"""
fix-pptx.py -- repara un .pptx exportado desde Claude Design.

POR QUE EXISTE
El convertidor a PPTX (PptxGenJS, se ve en docProps/app.xml) no rasteriza:
mapea cada elemento del DOM a una forma nativa de PowerPoint. Eso es bueno
-- el deck sale editable -- pero el formato PPTX no sabe hacer dos cosas que
el sistema AGCS da por hechas, y las dos se vieron en los entregables
descargados el 2026-09-13:

1. GRID. Se exporta, no falta: son ~150 rectangulos por slide, paso 40px.
   Lo que no sobrevive son los valores viejos. Con 2px de ancho y
   <a:alpha val="4000"> (4%), y una diapositiva de 3840px = 40 PULGADAS que
   PowerPoint muestra a un tercio, la linea cae a 0.67px y el antialias
   reparte ese 4% en ~3%: el grid esta ahi y no se ve. Es el mismo defecto
   que el ruling de v5.2 arreglo en el repo -- 3px y 9% sobre Paper, 11%
   sobre Obsidian -- solo que por la ruta PPTX, donde el arreglo del var()
   no interviene porque el convertidor nunca lee el background CSS.

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
Design. Cuando Claude Design quede al dia, `-o` no deberia cambiar nada y el
script lo dira imprimiendo cero.

LO QUE NO ARREGLA
El .pptx no embebe ninguna fuente (no hay ppt/fonts/ ni embeddedFontLst, y
embeber es una funcion de PowerPoint para Windows). En una maquina sin N27,
Crimson Pro y IBM Plex Mono instaladas se sustituye todo, diga lo que diga
el typeface. Para entrega externa, el PDF es el formato honesto.

USO
  python3 tools/fix-pptx.py deck.pptx -o deck-fix.pptx
  python3 tools/fix-pptx.py deck.pptx -o deck-fix.pptx --solo-grid
"""

import argparse, pathlib, re, zipfile
import xml.etree.ElementTree as ET

GRID_W_OLD  = 19050     # 2px @96dpi, en EMU -- lo que exporta Claude Design hoy
GRID_W_NEW  = 28575     # 3px -- v5.2
ALPHA_MAX   = 6000      # un rectangulo con <=6% de alpha es una linea de grid
ALPHA_LIGHT = 9000      # negro al 9% sobre Paper      (v5.2)
ALPHA_DARK  = 11000     # blanco al 11% sobre Obsidian (v5.2)
ALPHA_OK    = {ALPHA_LIGHT, ALPHA_DARK}

# Familia que pide el pptx -> familia que PowerPoint sabe encontrar.
# Solo Crimson Pro, y solo en italica. La familia legacy "N27" SI tiene una
# cara Bold propia, asi que typeface="N27" con b="1" resuelve bien y no se
# toca: reescribirla a "N27 Medium" bajaria los titulos de 700 a 500. Igual
# con IBM Plex Mono. El unico peso sin donde caer es el 600 italico.
FACE_FIX = {"Crimson Pro": "Crimson Pro SemiBold"}

SLIDE_PART = re.compile(r"ppt/(slides|slideMasters|slideLayouts)/[^/]+\.xml$")
EXT   = re.compile(r'<a:ext cx="(\d+)" cy="(\d+)"/>')
FILL  = re.compile(r'<a:srgbClr val="(000000|FFFFFF)"><a:alpha val="(\d+)"/>')
RPR   = re.compile(r"<a:(rPr|defRPr|endParaRPr)\b[^>]*>")
LATIN = re.compile(r'<a:latin typeface="([^"]+)"')


def fix_grid(xml: str, stats: dict) -> str:
    """Sube cada linea de grid de 2px/4% a 3px/9-11%."""
    def repl(sp: re.Match) -> str:
        s = sp.group(0)
        ext, fill = EXT.search(s), FILL.search(s)
        if not (ext and fill):
            return s
        cx, cy, color, alpha = int(ext.group(1)), int(ext.group(2)), fill.group(1), int(fill.group(2))
        vertical   = cy > 1_000_000
        horizontal = cx > 1_000_000
        if alpha in ALPHA_OK and GRID_W_NEW in (cx, cy) and (vertical or horizontal):
            stats["ya_ok"] += 1
            return s
        if alpha > ALPHA_MAX:
            return s
        if not ((cx == GRID_W_OLD and vertical) or (cy == GRID_W_OLD and horizontal)):
            return s
        stats["grid"] += 1
        new_cx = GRID_W_NEW if cx == GRID_W_OLD else cx
        new_cy = GRID_W_NEW if cy == GRID_W_OLD else cy
        s = s.replace(ext.group(0), f'<a:ext cx="{new_cx}" cy="{new_cy}"/>')
        nuevo = ALPHA_DARK if color == "FFFFFF" else ALPHA_LIGHT
        return s.replace(fill.group(0), f'<a:srgbClr val="{color}"><a:alpha val="{nuevo}"/>')
    return re.sub(r"<p:sp>.*?</p:sp>", repl, xml, flags=re.S)


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
        print("la salida no puede ser el archivo de entrada", file=__import__("sys").stderr)
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    stats = {"grid": 0, "font": 0, "ya_ok": 0, "slides": 0}

    tmp = out.with_suffix(".tmp")
    with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if SLIDE_PART.match(item.filename):
                xml = data.decode("utf-8")
                if not a.solo_fuente:
                    xml = fix_grid(xml, stats)
                if not a.solo_grid:
                    xml = fix_fonts(xml, stats)
                ET.fromstring(xml)          # si el XML quedo roto, aqui truena
                data = xml.encode("utf-8")
                stats["slides"] += item.filename.startswith("ppt/slides/")
            zout.writestr(item, data)
    tmp.replace(out)

    print(f"{out.name}  ·  {stats['slides']} slides  ·  "
          f"{stats['grid']} lineas de grid a 3px/9-11%  ·  "
          f"{stats['font']} runs a Crimson Pro SemiBold")
    if stats["ya_ok"]:
        print(f"  {stats['ya_ok']} lineas ya venian correctas")
    if not stats["grid"] and not stats["ya_ok"] and not a.solo_fuente:
        print("  ! ninguna linea de grid en el archivo: o el deck no lleva grid,\n"
              "    o el origen dejo de exportarlo -- revisalo antes de entregar")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
