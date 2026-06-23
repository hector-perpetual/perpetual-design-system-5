#!/usr/bin/env python3
"""
Genera la version HTML autocontenida del template "Marketing" (mismas 13 slides
que el .pptx), para inspeccionar en navegador y conectar a herramientas de diseno.
Armin Grotesk embebida en base64, logos SVG inline. Coordenadas = pulgadas x 96px.
"""
import os, base64

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
OUT = os.path.join(HERE, "perpetual-infographics.html")

# --- fuentes OTF -> @font-face base64 ---
FONTS = [("Normal", 300), ("Regular", 400), ("Semi_Bold", 600), ("Black", 800)]
faces = []
for name, weight in FONTS:
    data = open(os.path.join(ASSETS, "fonts", f"ArminGrotesk_{name}.otf"), "rb").read()
    b64 = base64.b64encode(data).decode()
    faces.append("@font-face{font-family:'Armin Grotesk';font-weight:%d;font-display:swap;"
                 "src:url(data:font/otf;base64,%s) format('opentype');}" % (weight, b64))
FONT_FACES = "\n".join(faces)


def _svg(path):
    return open(os.path.join(ASSETS, "logo", path)).read().split("?>", 1)[-1].strip()
LOGO_COLOR, LOGO_DARK = _svg("perpetual-color.svg"), _svg("perpetual-dark.svg")

# --- tokens ---
ACCENT, ACCENT2, YELLOW = "#1a56db", "#f97316", "#fbb900"
BGD, TEXT, DIM, MUTED = "#0b1220", "#111827", "#374151", "#6b7280"
SURFACE, SURFACE2, BORDER, WHITE, DBE4FF = "#f8f9fc", "#eef1f8", "#dde1ef", "#ffffff", "#dbe4ff"
PXIN = 96


def _p(v):
    return f"{v * PXIN:.1f}px"


def box(x, y, w, h, fill=None, r=0, oval=False, shadow=False, line=None):
    st = f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(w)};height:{_p(h)};"
    st += "border-radius:50%;" if oval else (f"border-radius:{r}px;" if r else "")
    if fill: st += f"background:{fill};"
    if line: st += f"border:1px solid {line};"
    if shadow: st += "box-shadow:0 8px 26px rgba(20,40,90,.13);"
    return f'<div style="{st}"></div>'


def txt(x, y, w, h, content, size, color=TEXT, weight=400, align="left",
        valign="top", spacing=None, upper=False, lh=1.1):
    just = {"top": "flex-start", "middle": "center", "bottom": "flex-end"}[valign]
    st = (f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(w)};height:{_p(h)};"
          f"display:flex;flex-direction:column;justify-content:{just};overflow:hidden;"
          f"font-size:{size*1.333:.1f}px;color:{color};font-weight:{weight};"
          f"text-align:{align};line-height:{lh};")
    if align == "center": st += "align-items:center;"
    if spacing: st += f"letter-spacing:{spacing}px;"
    if upper: st += "text-transform:uppercase;"
    return f'<div style="{st}">{content}</div>'


def logo(x, y, w, dark=False):
    svg = LOGO_DARK if dark else LOGO_COLOR
    st = f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(w)};"
    return f'<div class="lg" style="{st}">{svg}</div>'


def hexagon(x, y, size, fill):
    st = (f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(size)};height:{_p(size)};"
          f"background:{fill};clip-path:polygon(25% 0,75% 0,100% 50%,75% 100%,25% 100%,0 50%);")
    return f'<div style="{st}"></div>'


def blob(x, y, d, fill):
    return box(x, y, d, d, fill=fill, oval=True)


def pill(x, y, w, label, fill=ACCENT, fg=WHITE, arrow=True):
    out = [box(x, y, w, 0.62, fill=fill, r=31, shadow=True),
           txt(x + 0.34, y, w - 1.0, 0.62, label, 11.5, fg, 600, "left", "middle",
               spacing=0.8, upper=True)]
    if arrow:
        out.append(box(x + w - 0.74, y + 0.1, 0.42, 0.42, fill=WHITE, oval=True))
        out.append(txt(x + w - 0.74, y + 0.02, 0.42, 0.42, "&rsaquo;", 17, fill, 800, "center", "middle"))
    return "".join(out)


def photo_ph(x, y, w, h, r=12, tint="#E3ECFB"):
    d = min(w, h) * 0.24
    cxp, cyp = x + w / 2, y + h / 2
    return (box(x, y, w, h, fill=tint, r=r)
            + box(cxp - d / 2, cyp - d / 2, d, d, fill=WHITE, oval=True)
            + box(cxp - d * 0.16, cyp - d * 0.16, d * 0.32, d * 0.32, fill=ACCENT, oval=True))


ICONS = {
 "estrategia": '<line x1="12" y1="2" x2="12" y2="4"/><line x1="12" y1="20" x2="12" y2="22"/><line x1="2" y1="12" x2="4" y2="12"/><line x1="20" y1="12" x2="22" y2="12"/><circle cx="12" cy="12" r="7"/><polygon points="12,8 14.5,13.5 12,12.5 9.5,13.5" fill="currentColor" stroke="none"/><circle cx="12" cy="12" r="1.5" fill="currentColor" stroke="none"/>',
 "crecimiento": '<polyline points="3,17 8,10 13,13 20,5"/><polyline points="15,5 20,5 20,10"/>',
 "analitica": '<rect x="3" y="12" width="4" height="9" rx="1"/><rect x="10" y="7" width="4" height="14" rx="1"/><rect x="17" y="3" width="4" height="18" rx="1"/>',
 "inversion": '<circle cx="12" cy="12" r="9"/><path d="M9 14.5c0 1.1 1.3 2 3 2s3-.9 3-2-1.3-2-3-2-3-.9-3-2 1.3-2 3-2 3 .9 3 2"/><line x1="12" y1="7.5" x2="12" y2="9"/><line x1="12" y1="17" x2="12" y2="18.5"/>',
 "idea": '<path d="M9 21h6"/><path d="M10 17h4"/><path d="M12 3a6 6 0 0 1 6 6c0 2.2-1.2 4.1-3 5.2V17H9v-2.8A6 6 0 0 1 6 9a6 6 0 0 1 6-6z"/>',
 "equipo": '<circle cx="9" cy="7" r="3"/><path d="M3 21v-2a5 5 0 0 1 5-5h2"/><circle cx="17" cy="9" r="3"/><path d="M13 21v-2a5 5 0 0 1 5-5h1a5 5 0 0 1 5 5v2"/>',
 "objetivo": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="2" fill="currentColor" stroke="none"/>',
 "mercado": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18"/><path d="M12 3a15 15 0 0 1 0 18"/><path d="M12 3a15 15 0 0 0 0 18"/>',
 "producto": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27,6.96 12,12.01 20.73,6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>',
 "automatizacion": '<path d="M12 2a10 10 0 1 0 10 10"/><path d="M12 6v6l4 2"/><polyline points="18,2 22,2 22,6"/>',
 "tiempo": '<rect x="3" y="4" width="18" height="17" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="7" y1="14" x2="11" y2="14"/><line x1="7" y1="17" x2="15" y2="17"/>',
 "seguridad": '<path d="M12 3l8 4v5c0 4.4-3.4 8.5-8 9.5C7.4 20.5 4 16.4 4 12V7z"/><polyline points="9,12 11,14 15,10"/>',
 "alcance": '<path d="M5.5 5.5A8.38 8.38 0 0 0 3 12a9 9 0 0 0 9 9 9 9 0 0 0 9-9 8.38 8.38 0 0 0-2.5-6.5"/><path d="M8.5 8.5A4.24 4.24 0 0 0 7 12a5 5 0 0 0 5 5 5 5 0 0 0 5-5 4.24 4.24 0 0 0-1.5-3.5"/><circle cx="12" cy="12" r="2" fill="currentColor" stroke="none"/>',
 "innovacion": '<circle cx="12" cy="12" r="2"/><ellipse cx="12" cy="12" rx="10" ry="4"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(60 12 12)"/><ellipse cx="12" cy="12" rx="10" ry="4" transform="rotate(120 12 12)"/>',
}


def line_icon(x, y, size, color, name, circle=True):
    inner = ICONS[name]
    isz = size * 96 * 0.5
    svg = (f'<svg viewBox="0 0 24 24" width="{isz:.0f}" height="{isz:.0f}" fill="none" '
           f'stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{inner}</svg>')
    base = f"position:absolute;left:{_p(x)};top:{_p(y)};width:{_p(size)};height:{_p(size)};display:flex;align-items:center;justify-content:center;"
    if circle:
        base += f"border-radius:50%;background:{color}1f;"
    return f'<div style="{base}">{svg}</div>'


def graphic(x, y, w, h, tint="#DBE7FB", variant="abstract", r=12, shadow=False):
    """Grafico de marca (en vez de foto): composicion abstracta on-brand.
    En Perpetual no usamos fotos de personas salvo en la slide de equipo."""
    out = [box(x, y, w, h, fill=tint, r=r, shadow=shadow)]
    cx, cy = x + w / 2, y + h / 2
    if variant == "growth":
        n, bw, gap = 4, w * 0.13, w * 0.06
        total = n * bw + (n - 1) * gap
        bx, base = cx - total / 2, y + h * 0.8
        cols = [ACCENT, ACCENT2, YELLOW, ACCENT]
        for i in range(n):
            bh = h * (0.16 + 0.13 * i)
            out.append(box(bx + i * (bw + gap), base - bh, bw, bh, fill=cols[i], r=4))
        out.append(box(cx - w * 0.3, y + h * 0.16, h * 0.2, h * 0.2, fill=ACCENT, oval=True))
        out.append(hexagon(cx + w * 0.16, y + h * 0.14, h * 0.16, YELLOW))
    elif variant == "quote":
        out.append(txt(x, y + h * 0.06, w, h * 0.45, "&ldquo;", 92, ACCENT, 800, "center"))
        out.append(txt(x, y + h * 0.62, w, h * 0.2,
                       "&#9733; &#9733; &#9733; &#9733; &#9733;", 17, YELLOW, 700, "center"))
    else:  # abstract: circulos + hexagono de marca
        out.append(box(cx - w * 0.28, cy - h * 0.16, h * 0.34, h * 0.34, fill=ACCENT, oval=True))
        out.append(box(cx + w * 0.03, cy - h * 0.02, h * 0.22, h * 0.22, fill=ACCENT2, oval=True))
        out.append(box(cx - w * 0.02, cy + h * 0.16, h * 0.13, h * 0.13, fill=YELLOW, oval=True))
        out.append(hexagon(cx + w * 0.12, cy - h * 0.26, h * 0.17, WHITE))
    return "".join(out)


def title(runs, x=0.7, y=0.7, w=7.5, size=33):
    return logo(0.6, 0.5, 1.15) + txt(x, y + 0.55, w, 1.2, runs, size, TEXT, 800, lh=1.0)


def footer(page):
    return (txt(0.7, 7.0, 7, 0.3, "Confidencial &middot; Perpetual Technologies &copy; 2026",
                8.5, MUTED, 400, "left", "middle")
            + txt(11.7, 7.0, 1.1, 0.3, str(page).zfill(2), 8.5, MUTED, 400, "right", "middle"))


def AC(t):  # helper: envuelve en span de acento
    return f'<span style="color:{ACCENT}">{t}</span>'


# --- paleta de datos ---
GREEN, VIOLET = "#059669", "#7e22ce"
DATA = [ACCENT, ACCENT2, GREEN, YELLOW, VIOLET, MUTED]


# ===========================================================================
# Helpers nuevos para graficas simples
# ===========================================================================
def bars(x, y, w, h, vals, colors=None, gap=0.14, r=4, labels=None,
         label_color=MUTED, vmax=None):
    """Barras verticales (divs). vals normalizados a vmax."""
    colors = colors or DATA
    vmax = vmax or max(vals)
    n = len(vals)
    bw = (w - gap * (n - 1)) / n
    base = y + h
    out = []
    for i, v in enumerate(vals):
        bh = (v / vmax) * h
        bx = x + i * (bw + gap)
        out.append(box(bx, base - bh, bw, bh, fill=colors[i % len(colors)], r=r))
        if labels:
            out.append(txt(bx - 0.1, base + 0.08, bw + 0.2, 0.3, labels[i], 9,
                           label_color, 600, "center"))
    return "".join(out)


def donut(x, y, d, segments, thickness=22, track="#e5e9f4"):
    """Donut SVG. segments = [(valor, color), ...]."""
    total = sum(s[0] for s in segments) or 1
    px = d * PXIN
    rad = (px - thickness) / 2
    cx = cy = px / 2
    circ = 2 * 3.14159265 * rad
    parts = [f'<svg width="{px:.1f}" height="{px:.1f}" '
             f'style="position:absolute;left:{_p(x)};top:{_p(y)};transform:rotate(-90deg);overflow:visible">']
    parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad:.1f}" fill="none" '
                 f'stroke="{track}" stroke-width="{thickness}"/>')
    offset = 0.0
    for val, color in segments:
        frac = val / total
        dash = frac * circ
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{rad:.1f}" fill="none" '
                     f'stroke="{color}" stroke-width="{thickness}" '
                     f'stroke-dasharray="{dash:.2f} {circ - dash:.2f}" '
                     f'stroke-dashoffset="{-offset:.2f}" stroke-linecap="butt"/>')
        offset += dash
    parts.append("</svg>")
    return "".join(parts)


def line_chart(x, y, w, h, vals, color=ACCENT, vmax=None, vmin=None,
               dots=True, area=True, sw=3):
    """Linea SVG (polyline) sobre un area opcional."""
    pw, ph = w * PXIN, h * PXIN
    vmax = vmax if vmax is not None else max(vals)
    vmin = vmin if vmin is not None else min(vals)
    rng = (vmax - vmin) or 1
    n = len(vals)
    pad = pw * 0.04
    step = (pw - 2 * pad) / (n - 1) if n > 1 else 0
    pts = []
    for i, v in enumerate(vals):
        px = pad + i * step
        py = ph - ph * 0.08 - ((v - vmin) / rng) * (ph * 0.84)
        pts.append((px, py))
    poly = " ".join(f"{p[0]:.1f},{p[1]:.1f}" for p in pts)
    out = [f'<svg width="{pw:.1f}" height="{ph:.1f}" '
           f'style="position:absolute;left:{_p(x)};top:{_p(y)};overflow:visible">']
    if area:
        ap = f"{pts[0][0]:.1f},{ph:.1f} " + poly + f" {pts[-1][0]:.1f},{ph:.1f}"
        out.append(f'<polygon points="{ap}" fill="{color}" opacity="0.10"/>')
    out.append(f'<polyline points="{poly}" fill="none" stroke="{color}" '
               f'stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"/>')
    if dots:
        for p in pts:
            out.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="6" fill="#fff" '
                       f'stroke="{color}" stroke-width="{sw}"/>')
    out.append("</svg>")
    return "".join(out), pts


def connector(x1, y1, x2, y2, color=BORDER, w=2):
    """Linea fina recta entre dos puntos (pulgadas)."""
    import math
    dx, dy = (x2 - x1) * PXIN, (y2 - y1) * PXIN
    length = math.hypot(dx, dy)
    ang = math.degrees(math.atan2(dy, dx))
    st = (f"position:absolute;left:{_p(x1)};top:{_p(y1)};width:{length:.1f}px;"
          f"height:{w}px;background:{color};transform-origin:0 50%;"
          f"transform:rotate({ang:.2f}deg);")
    return f'<div style="{st}"></div>'


# ===========================================================================
# Slides (template "Infografias ejecutivas")
# ===========================================================================
def m01():
    """Portada."""
    return (box(0, 6.05, 13.333, 1.45, fill=SURFACE)
            + logo(0.7, 0.7, 1.5)
            # composicion: capas apiladas con profundidad (informacion en capas)
            + box(9.7, 1.5, 2.9, 2.0, fill="#dbe7fb", r=16)
            + box(9.25, 2.0, 2.9, 2.0, fill="#9dbcfb", r=16)
            + box(8.8, 2.5, 2.9, 2.0, fill="#3b82f6", r=16)
            + box(8.35, 3.0, 2.9, 2.0, fill=ACCENT, r=16, shadow=True)
            + box(8.75, 3.5, 0.2, 0.2, fill=WHITE, oval=True)
            + box(9.1, 3.5, 0.2, 0.2, fill=WHITE, oval=True)
            + box(9.45, 3.5, 0.2, 0.2, fill=WHITE, oval=True)
            + blob(11.95, 1.15, 0.85, YELLOW)
            + blob(7.95, 5.05, 0.6, ACCENT2)
            # texto
            + txt(0.65, 1.85, 7.6, 2.0, f"Infografias {AC('ejecutivas.')}", 50, TEXT, 800, lh=0.98)
            + txt(0.7, 3.85, 6.6, 0.3, "Plantilla de presentacion", 13, ACCENT, 600, upper=True, spacing=0.8)
            + txt(0.7, 4.3, 6.6, 1.0,
                  "Sistema visual para comunicar datos, procesos y estrategia con claridad ejecutiva.",
                  13.5, MUTED, 400, lh=1.35)
            + pill(0.7, 5.55, 3.0, "Ver plantilla", fill=ACCENT, fg=WHITE))


def m02():
    """5 opciones numeradas."""
    out = [title(f"Cinco {AC('opciones.')}"),
           txt(0.7, 2.35, 9.0, 0.4,
               "Comparativa de alternativas estrategicas en un mismo nivel de decision.",
               12.5, MUTED, 400, lh=1.3)]
    cols = [ACCENT, BGD, MUTED, "#cbd5e1", "#60a5fa"]
    descs = ["Inversion en medios pagados", "Optimizacion de conversion",
             "Expansion de canales organicos", "Alianzas y co-marketing",
             "Automatizacion de procesos"]
    n = 5
    x0, w, gap = 0.7, 2.18, 0.27
    for i in range(n):
        x = x0 + i * (w + gap)
        fg = TEXT if cols[i] == "#cbd5e1" else WHITE
        out += [txt(x, 2.65, w, 0.3, f"Opcion {i+1:02d}", 11, ACCENT, 600, upper=True, spacing=0.6),
                box(x, 3.05, w, 2.55, fill=cols[i], r=12, shadow=True),
                txt(x, 3.35, w, 1.1, f"{i+1:02d}", 56, fg, 800, "center"),
                txt(x + 0.25, 4.55, w - 0.5, 0.95, descs[i], 11, fg, 600, "center", lh=1.25)]
    out.append(footer(2))
    return "".join(out)


def m03():
    """Proceso: linea ascendente con 3 hitos."""
    out = [title(f"Proceso de {AC('crecimiento.')}"),
           txt(0.7, 2.4, 9.0, 0.4,
               "Evolucion del volumen de reportes procesados a lo largo del despliegue.",
               12.5, MUTED, 400, lh=1.3)]
    vals = [15, 22, 28, 35, 40, 45]
    chart, pts = line_chart(0.9, 2.7, 11.5, 3.4, vals, color=ACCENT, vmin=10, vmax=48)
    out.append(chart)
    # hitos en 3 nodos (indices 0, 3, 5)
    hitos = [(0, "Inicio", "Reportes 15.000"), (3, "Escalado", "Reportes 35.000"),
             (5, "Consolidacion", "Reportes 45.000")]
    for idx, lab, val in hitos:
        px, py = pts[idx]
        ix = 0.9 + px / PXIN
        iy = 2.7 + py / PXIN
        out += [blob(ix - 0.11, iy - 0.11, 0.22, ACCENT2),
                txt(ix - 1.1, iy - 0.85, 2.2, 0.3, lab, 11.5, TEXT, 600, "center"),
                txt(ix - 1.1, iy - 0.55, 2.2, 0.3, val, 11, ACCENT, 600, "center")]
    out.append(footer(3))
    return "".join(out)


def m04():
    """Mind-map: nodo central + 4 tarjetas INFODATA."""
    out = [title(f"Mapa de {AC('informacion.')}")]
    ncx, ncy = 2.6, 4.1  # centro nodo
    nr = 0.95  # radio del nodo central (circulo)
    out += [box(ncx - nr, ncy - nr, nr * 2, nr * 2, fill=ACCENT, oval=True, shadow=True),
            box(ncx - 0.28, ncy - 0.28, 0.56, 0.56, fill=WHITE, oval=True),
            blob(ncx - 0.11, ncy - 0.11, 0.22, ACCENT),
            txt(ncx - 1.5, ncy + nr + 0.18, 3.0, 0.3, "Eje central", 11, TEXT, 600, "center", upper=True, spacing=0.6)]
    cards = [
        ("INFODATA 01", "Fuentes de datos", "Integracion de canales y CRM en un repositorio unico."),
        ("INFODATA 02", "Modelado", "Normalizacion y enriquecimiento de la informacion."),
        ("INFODATA 03", "Analisis", "Tableros y metricas accionables por area."),
        ("INFODATA 04", "Activacion", "Decisiones y campanas basadas en evidencia."),
    ]
    cx, cw, ch = 7.0, 5.6, 1.05
    ys = [1.55, 2.85, 4.15, 5.45]
    for (tag, t, d), y in zip(cards, ys):
        cardcy = y + ch / 2
        out += [connector(ncx + nr, ncy, cx, cardcy, color=BORDER, w=2),
                blob(ncx + nr - 0.06, ncy - 0.06, 0.12, ACCENT2),
                box(cx, y, cw, ch, fill=WHITE, r=12, shadow=True, line=BORDER),
                box(cx, y, 0.09, ch, fill=ACCENT, r=4),
                txt(cx + 0.35, y + 0.16, cw - 0.6, 0.3, tag, 10, ACCENT, 600, upper=True, spacing=0.8),
                txt(cx + 0.35, y + 0.42, cw - 0.6, 0.3, t, 13, TEXT, 600),
                txt(cx + 0.35, y + 0.72, cw - 0.6, 0.3, d, 10.5, MUTED, 400, lh=1.2)]
    out.append(footer(4))
    return "".join(out)


def m05():
    """4 hexagonos de metricas."""
    out = [title(f"Indicadores {AC('clave.')}"),
           txt(0.7, 2.4, 9.0, 0.4, "Usuarios activos por segmento de plataforma.",
               12.5, MUTED, 400, lh=1.3)]
    metrics = [("17,2", ACCENT, WHITE, "Mayor adopcion en el canal principal."),
               ("15,2", BGD, WHITE, "Base estable con retencion sostenida."),
               ("21,2", "#60a5fa", WHITE, "Crecimiento acelerado del trimestre."),
               ("18,2", "#cbd5e1", TEXT, "Segmento maduro con margen de mejora.")]
    x0, size, gap = 0.85, 2.55, 0.45
    hy = 2.95
    for i, (val, fill, fg, side) in enumerate(metrics):
        x = x0 + i * (size + gap)
        out += [hexagon(x, hy, size, fill),
                txt(x, hy + size * 0.28, size, 0.7, val, 32, fg, 800, "center"),
                txt(x, hy + size * 0.55, size, 0.3, "Millon usuarios", 9.5, fg, 600, "center",
                    upper=True, spacing=0.4),
                txt(x - 0.1, hy + size + 0.15, size + 0.2, 0.8, side, 10, MUTED, 400, "center", lh=1.25)]
    out.append(footer(5))
    return "".join(out)


def m06():
    """Org chart 'Creativo'."""
    out = [title(f"Estructura {AC('creativa.')}")]
    # nodo superior
    top_x, top_w = 5.07, 3.2
    out += [box(top_x, 2.0, top_w, 1.0, fill=BGD, r=12, shadow=True),
            txt(top_x, 2.0, top_w, 1.0, "CREATIVO", 18, WHITE, 800, "center", "middle", spacing=1)]
    children = [("EQUIPO", "Talento y roles", ACCENT, 1.4),
                ("ESTRATEGIA", "Direccion y foco", ACCENT2, 5.07),
                ("NEGOCIO", "Valor y resultados", GREEN, 8.73)]
    cw = 3.0
    cy = 4.4
    parent_bottom_x = top_x + top_w / 2
    for t, sub, col, x in children:
        child_top_x = x + cw / 2
        out += [connector(parent_bottom_x, 3.0, parent_bottom_x, 3.7, color=BORDER, w=2),
                connector(child_top_x, 3.7, child_top_x, cy, color=BORDER, w=2)]
    out += [connector(1.4 + cw / 2, 3.7, 8.73 + cw / 2, 3.7, color=BORDER, w=2)]
    for t, sub, col, x in children:
        out += [box(x, cy, cw, 1.5, fill=WHITE, r=12, shadow=True, line=BORDER),
                box(x, cy, 0.09, 1.5, fill=col, r=4),
                txt(x + 0.35, cy + 0.32, cw - 0.6, 0.4, t, 15, TEXT, 700, spacing=0.6),
                txt(x + 0.35, cy + 0.8, cw - 0.6, 0.4, sub, 11.5, MUTED, 400)]
    out.append(footer(6))
    return "".join(out)


def m07():
    """Proceso 01-06 en fila/abanico."""
    out = [title(f"Flujo en {AC('seis pasos.')}"),
           txt(0.7, 2.4, 9.0, 0.4, "Secuencia operativa de extremo a extremo.",
               12.5, MUTED, 400, lh=1.3)]
    steps = [("Descubrir", ACCENT), ("Definir", ACCENT2), ("Disenar", GREEN),
             ("Desarrollar", YELLOW), ("Desplegar", VIOLET), ("Medir", MUTED)]
    n = 6
    x0, w, gap = 0.7, 1.78, 0.22
    base_y = 3.0
    for i, (t, col) in enumerate(steps):
        x = x0 + i * (w + gap)
        y = base_y + (0.45 if i % 2 else 0)  # leve abanico alternado
        out += [box(x, y, w, 2.1, fill=col, r=12, shadow=True),
                txt(x, y + 0.25, w, 0.9, f"{i+1:02d}", 38, WHITE, 800, "center"),
                txt(x + 0.15, y + 1.35, w - 0.3, 0.6, t, 12.5, WHITE, 600, "center", lh=1.1)]
    out.append(footer(7))
    return "".join(out)


def m08():
    """Piramide de 4 niveles + leyenda de %."""
    out = [title(f"Piramide de {AC('audiencia.')}")]
    levels = [("Viewers Uno", "10%", ACCENT, 2.0),
              ("Viewers Dos", "20%", ACCENT2, 3.2),
              ("Viewers Tres", "30%", GREEN, 4.4),
              ("Viewers Cuatro", "40%", "#cbd5e1", 5.6)]
    cx = 4.3
    top_y = 2.45
    lh = 1.0
    for i, (name, pct, col, w) in enumerate(levels):
        y = top_y + i * lh
        x = cx - w / 2
        fg = TEXT if col == "#cbd5e1" else WHITE
        out += [box(x, y, w, lh - 0.12, fill=col, r=8, shadow=True),
                txt(x, y, w, lh - 0.12, name, 12.5, fg, 600, "center", "middle")]
    # leyenda a la derecha
    lx = 8.6
    out.append(txt(lx, 2.5, 4.0, 0.3, "Distribucion", 11, ACCENT, 600, upper=True, spacing=0.6))
    for i, (name, pct, col, w) in enumerate(levels):
        y = 3.05 + i * 0.85
        out += [box(lx, y + 0.05, 0.28, 0.28, fill=col, r=5),
                txt(lx + 0.45, y, 2.4, 0.35, name, 12, TEXT, 600),
                txt(lx + 2.7, y, 1.3, 0.35, pct, 14, col if col != "#cbd5e1" else MUTED, 800, "right")]
    out.append(footer(8))
    return "".join(out)


def m09():
    """Timeline horizontal con 4 hitos por ano."""
    out = [title(f"Linea de {AC('tiempo.')}")]
    y_line = 4.0
    out.append(box(1.2, y_line - 0.015, 10.9, 0.04, fill=BORDER))
    events = [("1996", "Fundacion", "Inicio de operaciones con foco en consultoria.", True),
              ("2003", "Expansion", "Apertura de nuevas lineas de servicio.", False),
              ("2015", "Digital", "Transformacion hacia data y performance.", True),
              ("2021", "Escala", "Consolidacion regional del portafolio.", False)]
    xs = [2.0, 5.0, 8.0, 11.0]
    cols = [ACCENT, ACCENT2, GREEN, VIOLET]
    cw = 2.5
    for (year, t, d, up), x, col in zip(events, xs, cols):
        nx = x
        out.append(blob(nx - 0.13, y_line - 0.13, 0.26, col))
        out.append(box(nx - 0.04, y_line - 0.04, 0.08, 0.08, fill=WHITE, oval=True))
        if up:
            cy = y_line - 1.65
            out.append(connector(nx, y_line, nx, cy + 1.4, color=col, w=2))
        else:
            cy = y_line + 0.55
            out.append(connector(nx, y_line, nx, cy, color=col, w=2))
        out += [box(nx - cw / 2, cy, cw, 1.4, fill=WHITE, r=12, shadow=True, line=BORDER),
                txt(nx - cw / 2 + 0.3, cy + 0.2, cw - 0.6, 0.4, year, 18, col, 800),
                txt(nx - cw / 2 + 0.3, cy + 0.62, cw - 0.6, 0.3, t, 12, TEXT, 600),
                txt(nx - cw / 2 + 0.3, cy + 0.92, cw - 0.6, 0.45, d, 9.5, MUTED, 400, lh=1.2)]
    out.append(footer(9))
    return "".join(out)


def m10():
    """4 iconos circulares con hexagono blanco dentro."""
    out = [title(f"Pilares de {AC('valor.')}"),
           txt(0.7, 2.4, 9.0, 0.4, "Las cuatro dimensiones que sostienen la propuesta.",
               12.5, MUTED, 400, lh=1.3)]
    items = [("Inversion", ACCENT, "inversion", "Asignacion eficiente de presupuesto."),
             ("Estrategia", ACCENT2, "estrategia", "Direccion clara y priorizada."),
             ("Crecimiento", GREEN, "crecimiento", "Resultados sostenibles y medibles."),
             ("Creatividad", VIOLET, "idea", "Ideas que diferencian la marca.")]
    d = 1.85
    x0, gap = 1.05, 0.95
    for i, (t, col, icon, desc) in enumerate(items):
        x = x0 + i * (d + gap)
        out += [line_icon(x, 2.7, d, col, icon),
                txt(x - 0.25, 2.7 + d + 0.2, d + 0.5, 0.4, t, 14, TEXT, 700, "center"),
                txt(x - 0.25, 2.7 + d + 0.62, d + 0.5, 0.7, desc, 10.5, MUTED, 400, "center", lh=1.25)]
    out.append(footer(10))
    return "".join(out)


SLIDES = [m01, m02, m03, m04, m05, m06, m07, m08, m09, m10]
stages = "\n".join(f'<div class="slide">{fn()}</div>' for fn in SLIDES)

HTML = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Perpetual &middot; Infografias ejecutivas</title>
<style>
{FONT_FACES}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#c9ccd6;font-family:'Armin Grotesk',system-ui,sans-serif;padding:30px 0}}
.deck{{width:1280px;margin:0 auto;display:flex;flex-direction:column;gap:24px}}
.slide{{position:relative;width:1280px;height:720px;background:#fff;overflow:hidden;
  border-radius:16px;box-shadow:0 10px 40px rgba(0,0,0,.18)}}
.lg svg{{display:block;width:100%;height:auto}}
</style></head><body>
<div class="deck">
{stages}
</div>
</body></html>"""

with open(OUT, "w", encoding="utf-8") as f:
    f.write(HTML)
print("OK:", OUT, "|", round(len(HTML) / 1024), "KB |", len(SLIDES), "slides")
