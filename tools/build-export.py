#!/usr/bin/env python3
"""
build-export.py -- convierte slides de autoria en un HTML de export autocontenido.

POR QUE EXISTE
Las slides de /slides y /journey-lab estan escritas para el navegador: enlazan
_slide.css, cargan _fit.js, declaran @font-face con rutas relativas a /fonts y
apuntan a /assets. Todo eso funciona sirviendo el repo y se rompe en cuanto el
HTML sale de aqui. El renderer estatico que convierte HTML a Adobe Express (y
cualquier descarga del documento) no ejecuta JavaScript, no sigue CSS externo,
no resuelve rutas relativas y declara que var(--...) puede no resolverse.

El resultado eran dos fallas que se veian en cada entregable descargado:
  - el fondo de cuadraditos desaparecia (colgaba de var() anidadas),
  - el subtitulo dejaba de ser Crimson Pro SemiBold Italic y caia a Georgia
    con bold sintetico, porque el @font-face apuntaba a fonts/*.ttf relativo
    y a local(), y en un renderer sin la fuente instalada no hay ninguno.

Este script cierra las dos por construccion, para que nadie tenga que
acordarse de nada antes de exportar.

QUE HACE
  1. Concatena colors_and_type.css y _slide.css en un solo <style> en <head>.
  2. Embebe las tipografias como data: URI base64 y BORRA los src local(),
     de modo que la unica fuente posible es la que viaja en el archivo.
  3. Embebe cada imagen (.svg, .png) referenciada por src= o url() como data: URI.
  4. Quita todo <script> y neutraliza el transform: scale() de _fit.js, dejando
     cada canvas en su tamano natural de 3840x2160.
  5. Escribe la metadata que el importador necesita: hz:slide-selector,
     hz:canvas-width / hz:canvas-height y data-canvas-width / data-canvas-height
     en cada raiz.

USO
  python3 tools/build-export.py slides/*.html -o dist/deck-export.html
  python3 tools/build-export.py journey-lab/01-map-as-is.html
"""

import argparse, base64, mimetypes, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CANVAS_W, CANVAS_H = 3840, 2160

# Los archivos que solo existen para la vista en navegador y que el export no
# debe arrastrar: index del deck y el escenario que lo pagina con iframes.
SKIP = {"index.html", "deck-stage.js"}


def data_uri(path: pathlib.Path) -> str:
    mime, _ = mimetypes.guess_type(path.name)
    if mime is None:
        mime = {
            ".otf": "font/otf",
            ".ttf": "font/ttf",
            ".svg": "image/svg+xml",
        }.get(path.suffix.lower(), "application/octet-stream")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def load_css(entry: pathlib.Path) -> str:
    """Resuelve @import de forma recursiva y devuelve un solo bloque de CSS."""
    css = entry.read_text()
    def repl(m):
        target = (entry.parent / m.group(1)).resolve()
        return load_css(target) if target.exists() else ""
    return re.sub(r'@import\s+url\(["\']?([^"\')]+)["\']?\);', repl, css)


def embed_fonts(css: str, base: pathlib.Path) -> tuple[str, int]:
    """
    Reescribe cada src: de @font-face a un unico data: URI.

    Borrar local() es el punto entero. Con local() primero, un renderer que no
    tiene N27 ni Crimson Pro instaladas -- que es el caso de cualquier maquina
    de export -- pasaba al siguiente src, que era una ruta relativa muerta, y
    de ahi al fallback Georgia. El subtitulo terminaba en serif del sistema con
    weight 600 sintetizado, que es exactamente lo que se veia en los PDF.
    """
    n = 0
    def repl(m):
        nonlocal n
        body = m.group(0)
        urls = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', body)
        if not urls:
            return body
        target = (base / urls[0]).resolve()
        if not target.exists():
            print(f"  ! falta la fuente {target}", file=sys.stderr)
            return body
        n += 1
        return re.sub(
            r"src:[^;]+;",
            f'src: url("{data_uri(target)}") format("{"opentype" if target.suffix.lower() == ".otf" else "truetype"}");',
            body,
            count=1,
        )
    css = re.sub(r"@font-face\s*\{[^}]*\}", repl, css)
    return css, n


def embed_css_images(css: str, base: pathlib.Path) -> str:
    def repl(m):
        ref = m.group(1)
        if ref.startswith(("data:", "http:", "https:", "#")):
            return m.group(0)
        target = (base / ref).resolve()
        return f'url("{data_uri(target)}")' if target.exists() else m.group(0)
    return re.sub(r'url\(["\']?([^"\')]+)["\']?\)', repl, css)


def embed_html_images(html: str, base: pathlib.Path) -> tuple[str, int]:
    n = 0
    def repl(m):
        nonlocal n
        attr, ref = m.group(1), m.group(2)
        if ref.startswith(("data:", "http:", "https:", "#")):
            return m.group(0)
        target = (base / ref).resolve()
        if not target.exists():
            print(f"  ! falta el asset {target}", file=sys.stderr)
            return m.group(0)
        n += 1
        return f'{attr}="{data_uri(target)}"'
    html = re.sub(r'\b(src|href)="([^"]+\.(?:svg|png|jpg|jpeg|gif|webp))"', repl, html)
    return html, n


def extract_body(html: str) -> str:
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.S | re.I)
    body = m.group(1) if m else html
    return re.sub(r"<script\b.*?</script>", "", body, flags=re.S | re.I)


def tag_roots(body: str) -> tuple[str, int]:
    """Escribe data-canvas-* en cada raiz .agcs-canvas."""
    n = 0
    def repl(m):
        nonlocal n
        n += 1
        return m.group(0)[:-1] + f' data-canvas-width="{CANVAS_W}" data-canvas-height="{CANVAS_H}">'
    body = re.sub(r'<div[^>]*class="[^"]*\bagcs-canvas\b[^"]*"[^>]*>', repl, body)
    return body, n


# El transform: scale() de _fit.js existe para que la slide quepa en la ventana.
# En export estorba: el importador deriva el tamano del canvas del tamano
# renderizado de la raiz, y una raiz escalada a 0.333 reporta 1280 de ancho con
# todo el contenido posicionado para 3840. Se apaga y cada canvas vuelve a su
# tamano natural, apilado en flujo normal.
EXPORT_CSS = f"""
/* ---- Capa de export (la escribe tools/build-export.py) ------------------ */
html, body {{ margin: 0; padding: 0; background: #fff; overflow: visible; }}
.agcs-canvas {{
  position: relative;
  top: auto; left: auto;
  transform: none;
  width: {CANVAS_W}px;
  height: {CANVAS_H}px;
  overflow: hidden;
  page-break-after: always;
}}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("inputs", nargs="+")
    ap.add_argument("-o", "--out")
    a = ap.parse_args()

    files = [pathlib.Path(f).resolve() for f in a.inputs
             if pathlib.Path(f).name not in SKIP]
    files = [f for f in files if f.exists() and f.suffix == ".html"]
    if not files:
        print("nada que exportar", file=sys.stderr)
        return 1
    files.sort(key=lambda p: p.name)

    src_dir = files[0].parent
    css_entry = src_dir / "_slide.css"
    if not css_entry.exists():
        css_entry = next(src_dir.glob("*.css"))

    css = load_css(css_entry)
    css, nfonts = embed_fonts(css, ROOT)
    css = embed_css_images(css, ROOT)
    css += EXPORT_CSS

    bodies, nroots, nimgs = [], 0, 0
    for f in files:
        body = extract_body(f.read_text())
        body, k = embed_html_images(body, f.parent)
        body, r = tag_roots(body)
        nimgs += k
        nroots += r
        bodies.append(f"<!-- {f.name} -->\n{body.strip()}")

    out = pathlib.Path(a.out) if a.out else src_dir.parent / "dist" / f"{src_dir.name}-export.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        "<!doctype html>\n<html lang=\"es\">\n<head>\n<meta charset=\"utf-8\">\n"
        f"<title>AGCS · {src_dir.name}</title>\n"
        '<meta name="hz:slide-selector" content=".agcs-canvas">\n'
        f'<meta name="hz:canvas-width" content="{CANVAS_W}">\n'
        f'<meta name="hz:canvas-height" content="{CANVAS_H}">\n'
        f"<style>\n{css}\n</style>\n</head>\n<body>\n"
        + "\n\n".join(bodies)
        + "\n</body>\n</html>\n"
    )
    kb = out.stat().st_size / 1024
    print(f"{out}  ·  {nroots} slides · {nfonts} fuentes embebidas · {nimgs} assets · {kb:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
