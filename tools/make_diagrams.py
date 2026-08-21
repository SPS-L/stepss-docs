#!/usr/bin/env python3
"""Draws the two-port control-structure diagrams as SVG, light and dark.

These were ASCII art in fenced code blocks. They wrapped on a narrow screen,
they lost their alignment the moment a line ran past the block, and in the
printed guide they came out mangled: the box-drawing characters have to be
demoted to ASCII for pdfLaTeX and the long rows are then broken by fvextra,
which scatters continuation arrows through the middle of a signal path.

Two files per diagram, not one that adapts. An SVG loaded through `<img>` can
only see `prefers-color-scheme`, which is the reader's operating system rather
than the theme they picked on the site, so a single adaptive file is wrong for
anyone whose two settings disagree. A light/dark pair swapped with Starlight's
own `dark:sl-hidden` and `light:sl-hidden` follows the theme, and is what every
screenshot on the site already does. The printed guide takes the light half,
which is what `convert_images` in the user guide's generator already does with
a pair.

    ./tools/make_diagrams.py        # rewrite public/images/models/*.svg
"""

from __future__ import annotations

import pathlib
import re

OUT = pathlib.Path(__file__).resolve().parent.parent / "public" / "images" / "models"

FONT = "Inter, -apple-system, Segoe UI, Helvetica, Arial, sans-serif"
MONO = "JetBrains Mono, SFMono-Regular, Menlo, Consolas, monospace"

THEMES = {
    "light": dict(ink="#23262f", muted="#4b5162", line="#4b5162",
                  box="#f2f4f8", edge="#b6becd", accent="#2b6cb0",
                  accent_box="#e7f0fa", accent_edge="#7ba7d4"),
    "dark": dict(ink="#e5e7eb", muted="#b8bdc9", line="#a8b0bf",
                 box="#252a33", edge="#4a5160", accent="#78aeea",
                 accent_box="#1d2b3d", accent_edge="#3f6087"),
}


class Canvas:
    """Just enough SVG to draw a signal-flow diagram."""

    def __init__(self, width: int, height: int, t: dict):
        self.w, self.h, self.t = width, height, t
        self.parts: list[str] = []
        self.maxx = self.maxy = 0.0

    def _seen(self, x, y):
        """Widen the recorded extent. render() fits the viewBox to it, so a
        diagram that outgrows its declared size is not silently clipped."""
        self.maxx = max(self.maxx, float(x))
        self.maxy = max(self.maxy, float(y))

    # -- primitives ---------------------------------------------------------
    def box(self, x, y, w, h, lines, accent=False, size=13):
        t = self.t
        fill = t["accent_box"] if accent else t["box"]
        edge = t["accent_edge"] if accent else t["edge"]
        self._seen(x + w, y + h)
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" '
            f'fill="{fill}" stroke="{edge}" stroke-width="1.2"/>'
        )
        if isinstance(lines, str):
            lines = [lines]
        total = len(lines)
        for i, line in enumerate(lines):
            cy = y + h / 2 + (i - (total - 1) / 2) * (size + 3) + size / 3
            self.parts.append(
                f'<text x="{x + w / 2}" y="{cy:.1f}" text-anchor="middle" '
                f'font-family="{FONT}" font-size="{size}" fill="{t["ink"]}">{line}</text>'
            )
        return (x, y, w, h)

    def label(self, x, y, text, anchor="middle", size=13, mono=False, muted=False, italic=False):
        t = self.t
        fam = MONO if mono else FONT
        fill = t["muted"] if muted else t["ink"]
        plain = re.sub(r"&#\d+;", "x", str(text))
        width = len(plain) * size * (0.62 if mono else 0.56)
        right = x + (width if anchor == "start" else width / 2 if anchor == "middle" else 0)
        self._seen(right, y + size * 0.3)
        style = ' font-style="italic"' if italic else ""
        self.parts.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" '
            f'font-size="{size}" fill="{fill}"{style}>{text}</text>'
        )

    def path(self, d, arrow=True, dash=False):
        t = self.t
        for a, b in re.findall(r"(-?[\d.]+)\s+(-?[\d.]+)", d):
            self._seen(a, b)
        marker = ' marker-end="url(#arrow)"' if arrow else ""
        stroke = ' stroke-dasharray="4 3"' if dash else ""
        self.parts.append(
            f'<path d="{d}" fill="none" stroke="{t["line"]}" '
            f'stroke-width="1.3"{stroke}{marker}/>'
        )

    def arrow(self, x1, y1, x2, y2):
        self.path(f"M {x1} {y1} L {x2} {y2}")

    def elbow(self, x1, y1, x2, y2, first="h"):
        """One right-angle bend, horizontal first or vertical first."""
        mid = f"L {x2} {y1}" if first == "h" else f"L {x1} {y2}"
        self.path(f"M {x1} {y1} {mid} L {x2} {y2}")

    def band(self, x, y, w, h, label=None):
        """A shaded horizontal band: a deadband, or a region around a threshold."""
        t = self.t
        self._seen(x + w, y + h)
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{t["accent_box"]}" '
            f'stroke="{t["accent_edge"]}" stroke-width="0.9" stroke-dasharray="4 3"/>')
        if label:
            self.label(x + w + 10, y + h / 2 + 4, label, anchor="start",
                       size=11, muted=True, mono=True)

    def dot(self, x, y):
        self.parts.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{self.t["line"]}"/>')

    # -- composites ---------------------------------------------------------
    def chain(self, x, y, blocks, gap=34, h=54, arrow_in=True):
        """A row of blocks joined left to right.

        `blocks` is a list of (width, lines) or (width, lines, "accent"). The
        return value is the list of boxes and the x the last arrow ends at, so
        a caller can carry on from either.
        """
        boxes = []
        cx = x
        for i, spec in enumerate(blocks):
            w, lines = spec[0], spec[1]
            accent = len(spec) > 2 and spec[2] == "accent"
            if i or arrow_in:
                self.arrow(cx, y + h / 2, cx + gap, y + h / 2)
                cx += gap
            boxes.append(self.box(cx, y, w, h, lines, accent=accent, size=12))
            cx += w
        return boxes, cx

    def mult(self, x, y, r=13):
        """A multiplying junction."""
        t = self.t
        self._seen(x + r, y + r)
        self.parts.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["box"]}" '
            f'stroke="{t["edge"]}" stroke-width="1.2"/>')
        d = r * 0.42
        self.parts.append(
            f'<path d="M {x - d} {y - d} L {x + d} {y + d} M {x - d} {y + d} '
            f'L {x + d} {y - d}" stroke="{t["edge"]}" stroke-width="1.2"/>')
        return x, y

    def summing(self, x, y, signs=("+", "+"), r=13):
        """A summing junction. `signs` are placed left and below."""
        t = self.t
        self._seen(x + r, y + r)
        self.parts.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t["box"]}" '
            f'stroke="{t["edge"]}" stroke-width="1.2"/>')
        self.parts.append(
            f'<path d="M {x - r * 0.5} {y} L {x + r * 0.5} {y} M {x} {y - r * 0.5} '
            f'L {x} {y + r * 0.5}" stroke="{t["edge"]}" stroke-width="1"/>')
        if signs[0]:
            self.label(x - r - 8, y - 4, signs[0], size=13)
        if len(signs) > 1 and signs[1]:
            self.label(x + 2, y + r + 13, signs[1], size=13)
        return x, y

    def wire(self, x, y, text, dy=-8, size=10):
        """A name for the signal on a wire."""
        self.label(x, y + dy, text, size=size, muted=True, mono=True)

    # -- output -------------------------------------------------------------
    def render(self) -> str:
        t = self.t
        w = max(self.w, int(self.maxx + 16))
        h = max(self.h, int(self.maxy + 16))
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img">\n'
            f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M 0 1 L 10 5 L 0 9 z" fill="{t["line"]}"/></marker>'
            f'<marker id="arrow-accent" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M 0 1 L 10 5 L 0 9 z" fill="{t["accent"]}"/></marker></defs>\n'
            + "\n".join(self.parts)
            + "\n</svg>\n"
        )


# ---------------------------------------------------------------- diagrams
def hvdc_lcc(t):
    """Order, then rectifier, then down and back along the DC line."""
    c = Canvas(840, 300, t)
    y = 40
    c.label(14, y + 22, "Pset", anchor="start", mono=True, size=12)
    c.label(14, y + 40, "Idset", anchor="start", mono=True, size=12)
    c.arrow(64, y + 30, 104, y + 30)
    c.box(108, y, 168, 60, ["Power or current", "order &#8594; Ides"])
    c.arrow(276, y + 30, 316, y + 30)
    c.box(320, y, 150, 60, ["1st-order filter", "Tp"])
    c.arrow(470, y + 30, 528, y + 30)
    c.label(499, y + 22, "Iord", size=11, muted=True, mono=True)
    c.box(532, y, 176, 60, ["Rectifier", "firing angle &#945;"], accent=True)

    # down from the rectifier, then leftwards along the DC line
    c.path("M 620 100 L 620 152", arrow=False)
    c.arrow(620, 152, 512, 152)
    c.label(566, 144, "Vdr", size=11, muted=True, mono=True)
    c.box(392, 130, 120, 44, ["DC line RL"])
    c.arrow(392, 152, 284, 152)
    c.label(338, 144, "Vdi", size=11, muted=True, mono=True)
    c.box(84, 122, 200, 60, ["Inverter", "voltage or &#947; control"], accent=True)

    c.label(420, 232, "Rectifier holds the current order by advancing &#945;.", size=12, muted=True, italic=True)
    c.label(420, 252, "Inverter holds Vset = Vdi + Rcomp&#183;Id.", size=12, muted=True, italic=True)
    return c


def hvdc_vsc(t):
    """One strip per axis, each ending in the inner current controller.

    The two axes share one inner controller, and it is drawn on both strips
    rather than once with two paths crossing the figure to reach it. The
    original ASCII did the same, and it keeps each signal path readable end to
    end.
    """
    c = Canvas(1010, 330, t)

    def strip(y, ref, droop_title, droop_body, integ, out_label, ff, vm):
        c.label(14, y + 20, ref, anchor="start", mono=True, size=12)
        c.arrow(122, y + 16, 158, y + 16)
        c.box(162, y - 12, 196, 56, [droop_title, droop_body])
        c.arrow(358, y + 16, 394, y + 16)
        c.box(398, y - 12, 124, 56, ["Integrator", integ])
        return 522

    # --- d axis ----------------------------------------------------------
    y = 40
    x = strip(y, "Pref, Vdcref", "P&#8211;V droop",
              "&#945;1&#183;&#916;P + &#946;1&#183;&#916;Vdc", "1 / Kid", None, None, None)
    c.arrow(x, y + 16, x + 42, y + 16)
    c.box(x + 46, y - 12, 142, 56, ["Limiter", "Idmin / Idmax"])
    c.arrow(x + 188, y + 16, x + 232, y + 16)
    c.label(x + 210, y + 6, "idref", size=10, muted=True, mono=True)
    c.box(x + 236, y - 12, 150, 56, ["Inner current PI"], accent=True)
    c.arrow(x + 386, y + 16, x + 420, y + 16)
    c.label(x + 428, y + 21, "vmd", anchor="start", mono=True, size=12)
    c.label(x + 311, y + 96, "vd, &#969;&#183;L&#183;iq", mono=True, size=12)
    c.arrow(x + 311, y + 82, x + 311, y + 46)

    # --- q axis ----------------------------------------------------------
    y2 = 196
    x = strip(y2, "Qref, Vacref", "Q&#8211;Vac droop",
              "&#945;2&#183;&#916;Q + &#946;2&#183;&#916;Vac", "1 / Kiq", None, None, None)
    c.arrow(x, y2 + 16, x + 42, y2 + 16)
    c.label(x + 21, y2 + 6, "iqref1", size=10, muted=True, mono=True)
    sx = x + 58
    c.parts.append(
        f'<circle cx="{sx}" cy="{y2 + 16}" r="14" fill="{t["box"]}" '
        f'stroke="{t["edge"]}" stroke-width="1.2"/>')
    c.label(sx, y2 + 21, "+", size=14)
    c.label(14, y2 + 96, "FRT boost", anchor="start", mono=True, size=12)
    c.arrow(96, y2 + 92, sx - 60, y2 + 92)
    c.label(300, y2 + 84, "iqref2", size=10, muted=True, mono=True)
    c.path(f"M {sx - 60} {y2 + 92} L {sx} {y2 + 92} L {sx} {y2 + 30}", arrow=False)
    c.arrow(sx + 14, y2 + 16, x + 232, y2 + 16)
    c.label(x + 160, y2 + 6, "iqref", size=10, muted=True, mono=True)
    c.box(x + 236, y2 - 12, 150, 56, ["Inner current PI"], accent=True)
    c.arrow(x + 386, y2 + 16, x + 420, y2 + 16)
    c.label(x + 428, y2 + 21, "vmq", anchor="start", mono=True, size=12)
    c.label(x + 311, y2 + 96, "vq, &#969;&#183;L&#183;id", mono=True, size=12)
    c.arrow(x + 311, y2 + 82, x + 311, y2 + 46)
    return c


def hvdc_vsc_sc(t):
    """Grid-forming: droop and inertia summed, then PI with a parallel gain."""
    c = Canvas(900, 300, t)
    c.label(14, 46, "&#969;1", anchor="start", mono=True, size=13)
    c.arrow(46, 42, 94, 42)
    c.box(98, 20, 156, 44, ["Kwi&#183;(1 &#8722; &#969;1)"])
    c.label(14, 122, "P0, &#916;P", anchor="start", mono=True, size=12)
    c.arrow(82, 118, 126, 118)
    c.box(130, 96, 124, 44, ["&#916;P / Snom"])

    # summing junction for the two outer contributions
    sx, sy = 306, 80
    c.path(f"M 254 42 L {sx} 42 L {sx} {sy - 14}", arrow=False)
    c.path(f"M 254 118 L {sx} 118 L {sx} {sy + 14}", arrow=False)
    c.parts.append(
        f'<circle cx="{sx}" cy="{sy}" r="14" fill="{t["box"]}" '
        f'stroke="{t["edge"]}" stroke-width="1.2"/>')
    c.label(sx, sy + 5, "+", size=14)
    c.arrow(sx + 14, sy, 372, sy)
    c.label(345, sy - 8, "N1", size=11, muted=True, mono=True)

    c.box(376, sy - 22, 136, 44, ["Integrator", "1 / Kip"], size=12)
    c.arrow(512, sy, 572, sy)
    c.label(542, sy - 8, "N1a", size=11, muted=True, mono=True)

    # parallel proportional branch, taken off N1
    c.dot(348, sy)
    c.path(f"M 348 {sy} L 348 176 L 400 176", arrow=False)
    c.box(404, 154, 116, 44, ["Kpp&#183;N1"])
    c.path("M 520 176 L 588 176 L 588 110", arrow=False)

    ax, ay = 588, 96
    c.parts.append(
        f'<circle cx="{ax}" cy="{ay}" r="14" fill="{t["box"]}" '
        f'stroke="{t["edge"]}" stroke-width="1.2"/>')
    c.label(ax, ay + 5, "+", size=14)
    c.path(f"M 572 {sy} L {ax} {sy} L {ax} {ay - 14}", arrow=False)
    c.arrow(ax + 14, ay, 672, ay)
    c.label(632, ay - 11, "idref_unlim", size=9, muted=True, mono=True)

    c.box(676, ay - 22, 104, 44, ["Limiter"])
    c.arrow(780, ay, 816, ay)
    c.label(824, ay + 5, "idref", anchor="start", mono=True, size=12)

    c.box(608, 214, 190, 56, ["Inner current PI"], accent=True)
    c.path("M 846 118 L 846 242 L 798 242", arrow=False)
    c.arrow(798, 242, 798, 242)
    c.arrow(608, 242, 556, 242)
    c.label(548, 247, "vmd", anchor="end", mono=True, size=12)
    return c


def dcl_vsc(t):
    c = Canvas(560, 480, t)
    c.label(280, 24, "Wind farm", size=13, muted=True)
    c.arrow(280, 32, 280, 56)
    c.box(180, 56, 200, 34, ["Bus 1 &#183; offshore AC"])
    c.arrow(280, 90, 280, 116)

    c.box(120, 116, 320, 84,
          ["Converter 1 &#183; grid-forming",
           "P/&#969; droop:  idref &#8592; P0 + &#916;P + Kwi&#183;&#916;&#969;",
           "QV droop:  iqref &#8592; &#946;V&#183;&#916;Q"], accent=True, size=12)
    c.arrow(280, 200, 280, 226)
    c.label(292, 218, "idc1, vdc1", anchor="start", mono=True, size=11, muted=True)

    c.box(120, 226, 320, 44, ["DC cable &#183; Rdc, Hdc1, Hdc2"])
    c.arrow(280, 270, 280, 296)
    c.label(292, 288, "idc2, vdc2", anchor="start", mono=True, size=11, muted=True)

    c.box(120, 296, 320, 84,
          ["Converter 2 &#183; grid-following",
           "Vdc control:  idref &#8592; Kpd&#183;&#916;Vdc + Kid&#183;&#8747;&#916;Vdc",
           "Q/Vac droop:  iqref &#8592; &#945;2&#183;&#916;Q + &#946;2&#183;&#916;Vac"], accent=True, size=12)
    c.arrow(280, 380, 280, 406)
    c.box(160, 406, 240, 34, ["Bus 2 &#183; onshore AC grid"])
    return c


# ------------------------------------------------- IEEE turbine-governors
def tor_entsoe_simp(t):
    c = Canvas(900, 170, t)
    y = 40
    c.label(14, y + 33, "&#969; &#8722; 1", anchor="start", mono=True, size=12)
    sx, sy = 120, y + 27
    c.arrow(70, sy, sx - 13, sy)
    c.summing(sx, sy, ("&#8722;", "+"))
    c.label(sx, sy + 52, "C = Tm&#183;R", size=11, muted=True, mono=True)
    c.arrow(sx, sy + 38, sx, sy + 13)
    boxes, x = c.chain(sx + 13, y, [
        (150, ["Droop 1 / R"]),
        (162, ["Lag 1 / (1 + sT1)", "limits VMIN, VMAX"]),
        (170, ["Lead-lag", "(1 + sT2) / (1 + sT3)"]),
    ])
    c.wire(x + 40, sy, "Pm")
    c.arrow(x, sy, x + 80, sy)
    c.label(x + 88, sy + 5, "Tm = Pm / &#969;", anchor="start", mono=True, size=12)
    return c


def tor_tgov1(t):
    c = Canvas(960, 240, t)
    y = 40
    c.label(14, y + 33, "&#969; &#8722; 1", anchor="start", mono=True, size=12)
    sx, sy = 120, y + 27
    c.arrow(70, sy, sx - 13, sy)
    c.summing(sx, sy, ("&#8722;", "+"))
    c.label(sx, sy + 52, "C = Tm&#183;R", size=11, muted=True, mono=True)
    c.arrow(sx, sy + 38, sx, sy + 13)
    boxes, x = c.chain(sx + 13, y, [
        (140, ["Droop 1 / R"]),
        (162, ["Lag 1 / (1 + sT1)", "limits VMIN, VMAX"]),
        (168, ["Lead-lag", "(1 + sT2) / (1 + sT3)"]),
    ])
    ax = x + 60
    c.arrow(x, sy, ax - 13, sy)
    c.summing(ax, sy, ("+", "+"))
    c.arrow(ax + 13, sy, ax + 70, sy)
    c.wire(ax + 42, sy, "Pm")
    c.label(ax + 78, sy + 5, "Tm = Pm / &#969;", anchor="start", mono=True, size=12)

    c.label(60, 196, "&#969; &#8722; 1", anchor="start", mono=True, size=12)
    c.arrow(114, 190, 300, 190)
    c.box(304, 168, 120, 44, ["Dt"], size=12)
    c.path(f"M 424 190 L {ax} 190 L {ax} {sy + 13}", arrow=False)
    return c


def tor_gast(t):
    c = Canvas(1180, 300, t)
    y = 34
    c.label(14, y + 33, "&#969; &#8722; 1", anchor="start", mono=True, size=12)
    sx, sy = 116, y + 27
    c.arrow(70, sy, sx - 13, sy)
    c.summing(sx, sy, ("&#8722;", "+"))
    c.label(sx, sy + 52, "LR = Tm", size=11, muted=True, mono=True)
    c.arrow(sx, sy + 38, sx, sy + 13)

    boxes, x = c.chain(sx + 13, y, [(126, ["Droop 1 / R"])])
    gx = x + 44
    c.arrow(x, sy, gx - 4, sy)
    c.box(gx, y, 96, 54, ["Min gate"], size=12)
    boxes2, x2 = c.chain(gx + 96, y, [
        (132, ["Limiter", "VMIN, VMAX"]),
        (128, ["Lag 1 / (1 + sT1)"]),
        (128, ["Lag 1 / (1 + sT2)"]),
    ])
    c.wire(x2 + 22, sy, "p3")
    ax = x2 + 52
    c.arrow(x2, sy, ax - 13, sy)
    c.summing(ax, sy, ("+", "+"))
    c.arrow(ax + 13, sy, ax + 64, sy)
    c.wire(ax + 40, sy, "Pm")
    c.label(ax + 72, sy + 5, "Tm = Pm / &#969;", anchor="start", mono=True, size=12)
    c.label(ax + 4, sy + 62, "Dt&#183;(&#969; &#8722; 1)", size=11, muted=True, mono=True)
    c.arrow(ax, sy + 48, ax, sy + 13)

    c.dot(x2 - 14, sy)
    c.path(f"M {x2 - 14} {sy} L {x2 - 14} 210", arrow=False)
    c.arrow(x2 - 14, 210, 700, 210)
    c.box(576, 188, 124, 44, ["Lag 1 / (1 + sT3)"], size=12)
    c.arrow(576, 210, 452, 210)
    c.box(320, 188, 132, 44, ["AT + KT(AT &#8722; p4)"], size=12)
    c.path(f"M 320 210 L {gx + 48} 210 L {gx + 48} {y + 54}", arrow=True)
    return c


def tor_degov1(t):
    c = Canvas(1010, 210, t)
    y = 34
    c.label(14, y + 33, "&#916;&#969;", anchor="start", mono=True, size=12)
    sx, sy = 106, y + 27
    c.arrow(52, sy, sx - 13, sy)
    c.summing(sx, sy, ("+", "+"))
    c.label(sx, sy + 54, "REF = V60&#183;R", size=11, muted=True, mono=True)
    c.arrow(sx, sy + 40, sx, sy + 13)
    boxes, x = c.chain(sx + 13, y, [
        (186, ["Governor lead-lag", "(1+sT3) / (1+sT1)(1+sT2)"]),
        (156, ["Actuator", "K(1+sT4) / (1+sT6)"]),
        (120, ["Lag 1 / (1 + sT5)"]),
    ])
    boxes2, x2 = c.chain(150, y + 100, [
        (150, ["Integrator", "limits TMIN, TMAX"]),
        (152, ["Engine dead time", "Pad&#233; e^(&#8722;sTD)"]),
        (120, ["Lag 1 / (1 + sTE)"]),
    ], arrow_in=False)
    c.path(f"M {x} {sy} L {x + 30} {sy} L {x + 30} {y + 127} L 190 {y + 127}", arrow=False)
    c.arrow(190, y + 127, 150, y + 127)
    c.arrow(x2, y + 127, x2 + 44, y + 127)
    c.label(x2 + 52, y + 132, "Tm", anchor="start", mono=True, size=12)
    c.label(x2 + 52, y + 152, "Pm = Tm&#183;&#969;", anchor="start", size=11, muted=True, mono=True)
    return c


def tor_hygov(t):
    c = Canvas(1180, 300, t)
    y = 30
    c.label(14, y + 33, "1 &#8722; &#969;", anchor="start", mono=True, size=12)
    sx, sy = 118, y + 27
    c.arrow(76, sy, sx - 13, sy)
    c.summing(sx, sy, ("+", "&#8722;"))
    c.label(sx, sy + 56, "R&#183;(c &#8722; P0)", size=11, muted=True, mono=True)
    c.arrow(sx, sy + 42, sx, sy + 13)
    boxes, x = c.chain(sx + 13, y, [
        (128, ["Lag 1 / (1 + sTf)"]),
        (112, ["1 / (r&#183;Tr)"]),
        (132, ["Rate limit", "&#177; VELM"]),
        (144, ["Integrator", "limits Gmin, Gmax"]),
    ])
    c.wire(x - 78, sy, "e", dy=-42)
    ax = x + 52
    c.arrow(x, sy, ax - 13, sy)
    c.summing(ax, sy, ("+", "+"))
    c.label(ax + 4, sy + 60, "e / r", size=11, muted=True, mono=True)
    c.arrow(ax, sy + 46, ax, sy + 13)
    boxes2, x2 = c.chain(ax + 13, y, [(120, ["Clip Gmin, Gmax"])])
    c.arrow(x2, sy, x2 + 40, sy)
    c.wire(x2 + 22, sy, "c")

    # Servo and water column, read right to left: the gate demand comes down
    # from the end of the governor row and the power leaves on the left.
    ry = y + 158
    c.path(f"M {x2 + 40} {sy} L 1140 {sy} L 1140 {ry + 27}", arrow=False)
    c.arrow(1140, ry + 27, 1076, ry + 27)
    c.box(942, ry, 134, 54, ["Servo 1 / (1 + sTg)"], size=12)
    c.arrow(942, ry + 27, 890, ry + 27)
    c.wire(916, ry + 27, "g", dy=-10)
    c.box(736, ry, 154, 54, ["Water column", "TW&#183;dQ/dt = dH"], size=12)
    c.arrow(736, ry + 27, 684, ry + 27)
    c.wire(710, ry + 27, "Q, h", dy=-10)
    c.box(520, ry, 164, 54, ["Turbine power", "At&#183;h&#183;(Q &#8722; qNL)"], size=12)
    c.arrow(520, ry + 27, 456, ry + 27)
    c.label(448, ry + 32, "Pm", anchor="end", mono=True, size=12)
    return c


# ---------------------------------------------------------- other governors
def tor_1storder(t):
    c = Canvas(940, 190, t)
    y = 40
    c.label(14, y + 33, "&#969; &#8722; 1", anchor="start", mono=True, size=12)
    sx, sy = 130, y + 27
    c.arrow(70, sy, sx - 13, sy)
    c.summing(sx, sy, ("&#8722;", "+"))
    c.label(sx, sy + 52, "Tm0", size=11, muted=True, mono=True)
    c.arrow(sx, sy + 38, sx, sy + 13)
    boxes, x = c.chain(sx + 13, y, [(126, ["Droop 1 / R"])])
    c.dot(x + 20, sy)
    c.wire(x + 30, sy, "Tset")
    boxes2, x2 = c.chain(x + 20, y, [(146, ["Lag 1 / (1 + sT2)"])])
    ax = x2 + 62
    c.arrow(x2, sy, ax - 13, sy)
    c.wire(x2 + 22, sy, "x1")
    c.summing(ax, sy, ("+", "+"))
    c.label(ax - 34, sy + 74, "(1 &#8722; FHP)&#183;x1 + FHP&#183;Tset", size=11, muted=True, mono=True)
    c.path(f"M {x + 20} {sy} L {x + 20} {sy + 62} L {ax} {sy + 62}", arrow=False)
    c.arrow(ax, sy + 62, ax, sy + 13)
    c.arrow(ax + 13, sy, ax + 60, sy)
    c.label(ax + 68, sy + 5, "Tm", anchor="start", mono=True, size=12)
    return c


def tor_hydro_generic1(t):
    c = Canvas(1120, 300, t)
    y = 30
    c.label(14, y + 33, "1 &#8722; &#969;", anchor="start", mono=True, size=12)
    sx, sy = 130, y + 27
    c.arrow(76, sy, sx - 13, sy)
    c.summing(sx, sy, ("+", "+"))
    c.label(sx, sy + 56, "(P0 &#8722; Pmeas)&#183;&#963;", size=11, muted=True, mono=True)
    c.arrow(sx, sy + 42, sx, sy + 13)
    boxes, x = c.chain(sx + 13, y, [
        (156, ["PI controller", "Kp + Ki / s"]),
        (140, ["Rate limit &#177; LIMz"]),
        (140, ["Gate limits 0 to 1"]),
        (138, ["Servo 1 / (1 + sTsm)"]),
    ])
    c.arrow(x, sy, x + 40, sy)
    c.wire(x + 22, sy, "z")

    ry = y + 158
    c.path(f"M {x + 40} {sy} L 1080 {sy} L 1080 {ry + 27}", arrow=False)
    c.arrow(1080, ry + 27, 1016, ry + 27)
    c.box(862, ry, 154, 54, ["Water column", "TW&#183;dQ/dt = 1 &#8722; H"], size=12)
    c.arrow(862, ry + 27, 798, ry + 27)
    c.wire(830, ry + 27, "Q, H", dy=-10)
    c.box(634, ry, 164, 54, ["Turbine power", "At&#183;H&#183;(Q &#8722; qNL)"], size=12)
    c.arrow(634, ry + 27, 570, ry + 27)
    c.label(562, ry + 32, "Pm", anchor="end", mono=True, size=12)
    return c


def tor_hydro_dg(t):
    c = Canvas(1000, 210, t)
    y = 40
    c.label(14, y + 33, "P*", anchor="start", mono=True, size=12)
    sx, sy = 118, y + 27
    c.arrow(50, sy, sx - 13, sy)
    c.summing(sx, sy, ("+", "&#8722;"))
    c.label(sx, sy + 52, "P", size=11, muted=True, mono=True)
    c.arrow(sx, sy + 38, sx, sy + 13)
    c.wire(sx + 30, sy, "e")
    boxes, x = c.chain(sx + 13, y, [
        (152, ["PI regulator", "Kp + Ki / s"]),
        (136, ["Rate limit &#177; LIMz"]),
        (134, ["Gate limits 0 to 1"]),
        (136, ["Servo 1 / (1 + sTsm)"]),
    ])
    c.arrow(x, sy, x + 44, sy)
    c.label(x + 52, sy + 5, "z", anchor="start", mono=True, size=12)
    c.label(500, 186, "Penstock and turbine exactly as HYDRO_GENERIC1.",
            size=11, muted=True, italic=True)
    return c


# ----------------------------------------------------------- other exciters
def exc_1storder(t):
    c = Canvas(820, 160, t)
    y = 36
    c.label(14, y + 33, "Vref", anchor="start", mono=True, size=12)
    sx, sy = 132, y + 27
    c.arrow(66, sy, sx - 13, sy)
    c.summing(sx, sy, ("+", "&#8722;"))
    c.label(sx, sy + 52, "V", size=11, muted=True, mono=True)
    c.arrow(sx, sy + 38, sx, sy + 13)
    boxes, x = c.chain(sx + 13, y, [
        (216, ["AVR KA / (1 + sTA)", "limits Vfmin, Vfmax"], "accent"),
    ])
    c.arrow(x, sy, x + 56, sy)
    c.label(x + 64, sy + 5, "vf", anchor="start", mono=True, size=12)
    c.label(400, 140, "Vref = V0 + Vf0 / KA at initialisation",
            size=11, muted=True, italic=True)
    return c


def exc_kundur(t):
    """The stabiliser sums into the regulator input, so the regulator sits to
    the right of the whole stabiliser chain and neither path crosses the other."""
    c = Canvas(1140, 290, t)
    y = 30
    c.label(14, y + 33, "V", anchor="start", mono=True, size=12)
    boxes, x = c.chain(52, y, [(150, ["Transducer", "1 / (1 + sTR)"])])
    sx, sy = 806, y + 27
    c.arrow(x, sy, sx - 13, sy)
    c.wire(x + 40, sy, "Vfil")
    c.summing(sx, sy, ("&#8722;", "+"))
    c.label(sx - 44, sy - 36, "Vref", size=11, muted=True, mono=True)
    c.arrow(sx, sy - 42, sx, sy - 13)
    boxes2, x2 = c.chain(sx + 13, y, [
        (216, ["AVR with TGR", "KA(1 + sTA) / (1 + sTB)"], "accent"),
    ])
    c.arrow(x2, sy, x2 + 50, sy)
    c.label(x2 + 58, sy + 5, "vf", anchor="start", mono=True, size=12)

    py = y + 160
    c.label(14, py + 33, "&#969;", anchor="start", mono=True, size=13)
    boxes3, x3 = c.chain(52, py, [
        (170, ["Washout", "KSTAB&#183;sTW / (1 + sTW)"]),
        (156, ["Lead-lag", "(1 + sT1) / (1 + sT2)"]),
        (156, ["Lead-lag", "(1 + sT3) / (1 + sT4)"]),
    ])
    c.wire(x3 + 34, py + 27, "Vs")
    c.path(f"M {x3} {py + 27} L {sx} {py + 27} L {sx} {sy + 13}", arrow=True)
    return c


# ------------------------------------------------------- IEEE exciters
def exc_ac1a(t):
    c = Canvas(1180, 330, t)
    y = 26
    c.label(14, y + 33, "Vt, P, Q", anchor="start", mono=True, size=12)
    boxes, x = c.chain(84, y, [
        (150, ["Line drop comp.", "Kv, Rc, Xc"]),
        (146, ["Transducer", "1 / (1 + sTR)"]),
    ])
    sx, sy = x + 52, y + 27
    c.arrow(x, sy, sx - 13, sy)
    c.wire(x + 22, sy, "Vc")
    c.summing(sx, sy, ("&#8722;", "&#8722;"))
    c.label(sx - 46, sy - 36, "VREF", size=11, muted=True, mono=True)
    c.arrow(sx, sy - 42, sx, sy - 13)
    boxes2, x2 = c.chain(sx + 13, y, [
        (156, ["Lead-lag", "(1 + sTC) / (1 + sTB)"]),
        (160, ["Amplifier KA / (1+sTA)", "limits VAMIN, VAMAX"]),
        (132, ["HV gate VUEL", "LV gate VOEL"]),
        (128, ["Limiter", "VRMIN, VRMAX"]),
    ])
    c.arrow(x2, sy, x2 + 40, sy)
    c.wire(x2 + 22, sy, "VR")

    ry = y + 176
    c.path(f"M {x2 + 40} {sy} L 1146 {sy} L 1146 {ry + 27}", arrow=False)
    c.arrow(1146, ry + 27, 1074, ry + 27)
    c.box(908, ry, 166, 54, ["Exciter integrator", "1 / sTE, VE &#8805; 0"], "accent")
    c.arrow(908, ry + 27, 840, ry + 27)
    c.wire(874, ry + 27, "VE", dy=-10)
    c.box(676, ry, 164, 54, ["Rectifier", "Efd = vrectif(Ifd, VE, KC)"])
    c.arrow(676, ry + 27, 606, ry + 27)
    c.label(598, ry + 32, "Efd", anchor="end", mono=True, size=12)

    # demagnetisation and saturation, and the rate feedback
    c.box(908, ry + 84, 166, 46, ["VFE = KD&#183;Ifd + (KE + SE)&#183;VE"], size=11)
    c.path(f"M 991 {ry + 84} L 991 {ry + 54}", arrow=True)
    c.box(320, ry, 200, 54, ["Rate feedback", "sKF / TF / (1 + sTF)"])
    c.path(f"M 908 {ry + 107} L 420 {ry + 107} L 420 {ry + 54}", arrow=True)
    c.path(f"M 320 {ry + 27} L {sx} {ry + 27} L {sx} {sy + 13}", arrow=True)
    c.wire(sx + 34, sy + 46, "VF", dy=0)
    return c


def exc_ac4a(t):
    c = Canvas(1160, 200, t)
    y = 40
    c.label(14, y + 33, "Vt, P, Q", anchor="start", mono=True, size=12)
    boxes, x = c.chain(84, y, [
        (146, ["Line drop comp."]),
        (140, ["Transducer 1/(1+sTR)"]),
    ])
    sx, sy = x + 50, y + 27
    c.arrow(x, sy, sx - 13, sy)
    c.wire(x + 20, sy, "Vc")
    c.summing(sx, sy, ("&#8722;", ""))
    c.label(sx - 44, sy - 36, "VREF", size=11, muted=True, mono=True)
    c.arrow(sx, sy - 42, sx, sy - 13)
    boxes2, x2 = c.chain(sx + 13, y, [
        (134, ["Input limiter", "VIMIN, VIMAX"]),
        (150, ["Lead-lag", "(1 + sTC) / (1 + sTB)"]),
        (110, ["HV gate VUEL"]),
        (168, ["Amplifier KA / (1+sTA)", "limits VRMIN, uplim"], "accent"),
    ])
    c.arrow(x2, sy, x2 + 44, sy)
    c.label(x2 + 52, sy + 5, "Efd", anchor="start", mono=True, size=12)
    c.label(x2 - 84, y + 132, "uplim = VRMAX &#8722; KC&#183;Ifd", size=11, muted=True, mono=True)
    c.arrow(x2 - 84, y + 118, x2 - 84, y + 54)
    return c


def exc_ac8b(t):
    c = Canvas(1140, 260, t)
    y = 30
    c.label(14, y + 33, "Vt", anchor="start", mono=True, size=12)
    boxes, x = c.chain(52, y, [(146, ["Transducer 1/(1+sTR)"])])
    sx, sy = x + 50, y + 27
    c.arrow(x, sy, sx - 13, sy)
    c.wire(x + 20, sy, "Vc")
    c.summing(sx, sy, ("+", "&#8722;"))
    c.label(sx - 44, sy - 36, "VREF", size=11, muted=True, mono=True)
    c.arrow(sx, sy - 42, sx, sy - 13)

    # the PID has a derivative branch beside the proportional-integral one
    c.dot(sx + 34, sy)
    c.box(sx + 62, y - 46, 168, 46, ["Derivative sKDR / (1 + sTDR)"], size=11)
    c.box(sx + 62, y + 34, 168, 46, ["PI  KPR + KIR / s"], size=11)
    c.path(f"M {sx + 34} {sy} L {sx + 34} {y - 23} L {sx + 62} {y - 23}", arrow=True)
    c.path(f"M {sx + 34} {sy} L {sx + 34} {y + 57} L {sx + 62} {y + 57}", arrow=True)
    ax = sx + 268
    c.path(f"M {sx + 230} {y - 23} L {ax} {y - 23} L {ax} {sy - 13}", arrow=False)
    c.path(f"M {sx + 230} {y + 57} L {ax} {y + 57} L {ax} {sy + 13}", arrow=False)
    c.summing(ax, sy, ("", ""))
    boxes2, x2 = c.chain(ax + 13, y, [
        (144, ["PID limits", "VPIDMIN, VPIDMAX"]),
        (150, ["Amplifier KA / (1+sTA)"]),
        (156, ["Exciter integrator", "1 / sTE, VFEMAX limit"], "accent"),
    ])
    c.arrow(x2, sy, x2 + 40, sy)
    c.wire(x2 + 22, sy, "VE")
    c.box(x2 + 44, y, 148, 54, ["Saturation SE(VE)", "and rectifier"])
    c.arrow(x2 + 192, sy, x2 + 232, sy)
    c.label(x2 + 240, sy + 5, "Efd", anchor="start", mono=True, size=12)
    return c


def exc_dc3a(t):
    c = Canvas(1080, 250, t)
    y = 34
    c.label(14, y + 33, "Vt", anchor="start", mono=True, size=12)
    boxes, x = c.chain(48, y, [(146, ["Transducer 1/(1+sTR)"])])
    sx, sy = x + 50, y + 27
    c.arrow(x, sy, sx - 13, sy)
    c.wire(x + 20, sy, "Vc")
    c.summing(sx, sy, ("&#8722;", ""))
    c.label(sx - 44, sy - 36, "VREF", size=11, muted=True, mono=True)
    c.arrow(sx, sy - 42, sx, sy - 13)
    c.wire(sx + 32, sy, "VERR")
    boxes2, x2 = c.chain(sx + 13, y, [
        (166, ["Rheostat integrator", "limits VRMIN, VRMAX"]),
        (176, ["Three-position switch", "VRMIN / VRH / VRMAX"], "accent"),
        (176, ["DC exciter", "1/sTE, KE + SE(Efd)"]),
    ])
    c.arrow(x2, sy, x2 + 44, sy)
    c.label(x2 + 52, sy + 5, "Efd", anchor="start", mono=True, size=12)
    c.label(540, 216, "The switch selects on the deadband: VERR below &#8722;KV lowers, "
                      "above +KV raises, inside holds VRH.",
            size=11, muted=True, italic=True)
    return c


def exc_ieeet5(t):
    c = Canvas(1080, 250, t)
    y = 34
    c.label(14, y + 33, "Vt", anchor="start", mono=True, size=12)
    boxes, x = c.chain(48, y, [(146, ["Transducer 1/(1+sTR)"])])
    sx, sy = x + 50, y + 27
    c.arrow(x, sy, sx - 13, sy)
    c.wire(x + 20, sy, "Vc")
    c.summing(sx, sy, ("&#8722;", ""))
    c.label(sx - 44, sy - 36, "VREF", size=11, muted=True, mono=True)
    c.arrow(sx, sy - 42, sx, sy - 13)
    c.wire(sx + 32, sy, "VERR")
    boxes2, x2 = c.chain(sx + 13, y, [
        (168, ["Deadband gate lim_civ", "&#177; KV"]),
        (166, ["Integrator 1 / sTRH", "limits VRMIN, VRMAX"]),
        (176, ["DC exciter", "1/sTE, KE + SE(Efd)"]),
    ])
    c.arrow(x2, sy, x2 + 44, sy)
    c.label(x2 + 52, sy + 5, "Efd", anchor="start", mono=True, size=12)
    c.label(540, 216, "The gate integrates only while the error is outside the deadband, "
                      "which is what makes it rheostatic.",
            size=11, muted=True, italic=True)
    return c


def exc_st1a(t):
    c = Canvas(1180, 340, t)
    y = 26
    c.label(14, y + 33, "Vt, P, Q", anchor="start", mono=True, size=12)
    boxes, x = c.chain(84, y, [
        (140, ["Line drop comp."]),
        (140, ["Transducer 1/(1+sTR)"]),
    ])
    sx, sy = x + 50, y + 27
    c.arrow(x, sy, sx - 13, sy)
    c.wire(x + 20, sy, "Vc")
    c.summing(sx, sy, ("&#8722;", "&#8722;"))
    c.label(sx - 52, sy - 36, "VREF, VPSS", size=11, muted=True, mono=True)
    c.arrow(sx, sy - 42, sx, sy - 13)
    boxes2, x2 = c.chain(sx + 13, y, [
        (126, ["Limiter", "VIMIN, VIMAX"]),
        (104, ["HV gate VUEL"]),
        (150, ["Lead-lag", "(1+sTC) / (1+sTB)"]),
        (156, ["Lead-lag", "(1+sTC1) / (1+sTB1)"]),
    ])
    c.arrow(x2, sy, x2 + 40, sy)

    ry = y + 188
    c.box(x2 + 44, y, 158, 54, ["Amplifier KA / (1+sTA)", "limits VAMIN, VAMAX"])
    c.path(f"M {x2 + 202} {sy} L 1146 {sy} L 1146 {ry + 27}", arrow=False)
    c.arrow(1146, ry + 27, 1064, ry + 27)
    c.wire(1104, ry + 27, "VA", dy=-10)
    c.box(920, ry, 144, 54, ["Field current limiter", "VLR"])
    c.arrow(920, ry + 27, 856, ry + 27)
    c.box(732, ry, 124, 54, ["HV gate VUEL", "LV gate VOEL"])
    c.arrow(732, ry + 27, 668, ry + 27)
    c.box(492, ry, 176, 54, ["Output limits scaled", "by terminal voltage"], "accent")
    c.arrow(492, ry + 27, 428, ry + 27)
    c.label(420, ry + 32, "Efd", anchor="end", mono=True, size=12)

    c.box(160, ry, 190, 54, ["Rate feedback", "sKF / TF / (1 + sTF)"])
    c.path(f"M 460 {ry + 27} L 350 {ry + 27}", arrow=True)
    c.dot(460, ry + 27)
    c.path(f"M 160 {ry + 27} L {sx} {ry + 27} L {sx} {sy + 13}", arrow=True)
    c.wire(sx + 30, sy + 48, "VF", dy=0)
    return c


def exc_st2a(t):
    c = Canvas(1160, 280, t)
    y = 30
    c.label(14, y + 33, "Vt", anchor="start", mono=True, size=12)
    boxes, x = c.chain(48, y, [(146, ["Transducer 1/(1+sTR)"])])
    sx, sy = x + 50, y + 27
    c.arrow(x, sy, sx - 13, sy)
    c.wire(x + 20, sy, "Vc")
    c.summing(sx, sy, ("&#8722;", "&#8722;"))
    c.label(sx - 52, sy - 36, "VREF, VPSS", size=11, muted=True, mono=True)
    c.arrow(sx, sy - 42, sx, sy - 13)
    boxes2, x2 = c.chain(sx + 13, y, [
        (110, ["HV gate VUEL"]),
        (150, ["PI amplifier", "KA&#183;TA, KA"]),
        (128, ["Limiter", "VRMIN, VRMAX"]),
        (150, ["Field integrator", "VR&#183;VB &#8722; KE&#183;Efd"], "accent"),
    ])
    c.arrow(x2, sy, x2 + 44, sy)
    c.label(x2 + 52, sy + 5, "Efd", anchor="start", mono=True, size=12)

    c.box(340, y + 150, 190, 50, ["Rate feedback", "sKF / TF / (1 + sTF)"])
    c.path(f"M {x2 + 22} {sy} L {x2 + 22} {y + 175} L 530 {y + 175}", arrow=True)
    c.dot(x2 + 22, sy)
    c.path(f"M 340 {y + 175} L {sx} {y + 175} L {sx} {sy + 13}", arrow=True)
    c.wire(sx + 30, sy + 48, "VF", dy=0)
    c.label(870, y + 180, "VB from the rectifier voltage VE", size=11, muted=True, italic=True)
    return c


def exc_sexs(t):
    c = Canvas(900, 180, t)
    y = 40
    c.label(14, y + 33, "Vt, VPSS", anchor="start", mono=True, size=12)
    sx, sy = 158, y + 27
    c.arrow(96, sy, sx - 13, sy)
    c.summing(sx, sy, ("&#8722;", ""))
    c.label(sx, sy + 52, "Vo", size=11, muted=True, mono=True)
    c.arrow(sx, sy + 38, sx, sy + 13)
    boxes, x = c.chain(sx + 13, y, [
        (166, ["Lead-lag", "(1 + sTA) / (1 + sTB)"]),
        (186, ["Exciter KE / (1 + sTE)", "limits EMIN, EMAX"], "accent"),
    ])
    c.arrow(x, sy, x + 48, sy)
    c.label(x + 56, sy + 5, "Efd", anchor="start", mono=True, size=12)
    c.label(450, 160, "Vo = Vt + Efd0 / KE at initialisation, so the initial error is zero.",
            size=11, muted=True, italic=True)
    return c


def exc_entsoe_simp(t):
    c = Canvas(1180, 290, t)
    y = 26
    c.label(14, y + 33, "Vt", anchor="start", mono=True, size=12)
    sx, sy = 740, y + 27
    c.arrow(48, sy, sx - 13, sy)
    c.summing(sx, sy, ("&#8722;", "+"))
    c.label(sx, sy - 46, "Vo", size=11, muted=True, mono=True)
    c.arrow(sx, sy - 40, sx, sy - 13)
    boxes, x = c.chain(sx + 13, y, [
        (150, ["Lead-lag", "(1+sTA) / (1+sTB)"]),
        (172, ["Exciter KE / (1 + sTE)", "limits EMIN, EMAX"], "accent"),
    ])
    c.arrow(x, sy, x + 44, sy)
    c.label(x + 52, sy + 5, "Efd", anchor="start", mono=True, size=12)

    py = y + 160
    c.label(14, py + 33, "&#969; &#8722; 1", anchor="start", mono=True, size=12)
    boxes2, x2 = c.chain(70, py, [
        (128, ["Washout", "sTW1 / (1+sTW1)"]),
        (128, ["Washout", "sTW2 / (1+sTW2)"]),
        (92, ["Gain KS1"]),
        (140, ["Lead-lag", "(1+sT1) / (1+sT2)"]),
        (140, ["Lead-lag", "(1+sT3) / (1+sT4)"]),
    ], gap=24)
    c.wire(x2 + 30, py + 27, "VPSS")
    c.path(f"M {x2} {py + 27} L {sx} {py + 27} L {sx} {sy + 13}", arrow=True)
    return c


# ------------------------------------------------------------ stabilisers
def pss_pss2b(t):
    c = Canvas(1160, 270, t)
    y = 26
    c.label(14, y + 33, "&#969;", anchor="start", mono=True, size=13)
    boxes, x = c.chain(46, y, [
        (128, ["Washout", "sTW1 / (1+sTW1)"]),
        (128, ["Washout", "sTW2 / (1+sTW2)"]),
        (128, ["Lag 1 / (1 + sT6)"]),
    ], gap=26)
    py = y + 120
    c.label(14, py + 33, "Pe", anchor="start", mono=True, size=12)
    boxes2, x2 = c.chain(46, py, [
        (128, ["Washout", "sTW3 / (1+sTW3)"]),
        (128, ["Washout", "sTW4 / (1+sTW4)"]),
        (128, ["Lag 1 / (1 + sT7)"]),
    ], gap=26)
    ax = x + 56
    c.path(f"M {x} {y + 27} L {ax} {y + 27} L {ax} {y + 60}", arrow=False)
    c.path(f"M {x2} {py + 27} L {ax} {py + 27} L {ax} {y + 88}", arrow=False)
    c.summing(ax, y + 74, ("", ""))
    boxes3, x3 = c.chain(ax + 13, y + 47, [
        (140, ["Ramp-track filter", "N, M stages"]),
        (140, ["Lead-lag", "(1+sT1) / (1+sT2)"]),
        (140, ["Lead-lag", "(1+sT3) / (1+sT4)"]),
        (124, ["Limits", "VSTMIN, VSTMAX"]),
    ], gap=26)
    c.arrow(x3, y + 74, x3 + 40, y + 74)
    c.label(x3 + 48, y + 79, "VPSS", anchor="start", mono=True, size=12)
    return c


def pss_pss3b(t):
    c = Canvas(1160, 260, t)
    y = 26
    c.label(14, y + 33, "VSI1", anchor="start", mono=True, size=12)
    boxes, x = c.chain(64, y, [
        (128, ["Lag 1 / (1 + sT1)"]),
        (160, ["Washout", "KS1&#183;sTW1 / (1+sTW1)"]),
    ], gap=26)
    py = y + 116
    c.label(14, py + 33, "VSI2", anchor="start", mono=True, size=12)
    boxes2, x2 = c.chain(64, py, [
        (128, ["Lag 1 / (1 + sT2)"]),
        (160, ["Washout", "KS2&#183;sTW2 / (1+sTW2)"]),
    ], gap=26)
    ax = x + 54
    c.path(f"M {x} {y + 27} L {ax} {y + 27} L {ax} {y + 58}", arrow=False)
    c.path(f"M {x2} {py + 27} L {ax} {py + 27} L {ax} {y + 84}", arrow=False)
    c.summing(ax, y + 71, ("+", "&#8722;"))
    boxes3, x3 = c.chain(ax + 13, y + 44, [
        (152, ["Washout", "KS&#183;sTW3 / (1+sTW4)"]),
        (140, ["2nd-order filter TF1"]),
        (140, ["2nd-order filter TF2"]),
    ], gap=26)
    c.arrow(x3, y + 71, x3 + 40, y + 71)
    c.label(x3 + 48, y + 76, "VPSS", anchor="start", mono=True, size=12)
    return c


def pss_pss4b(t):
    c = Canvas(1080, 300, t)
    c.label(14, 46, "&#916;&#969;", anchor="start", mono=True, size=12)
    c.arrow(48, 42, 96, 42)
    c.box(100, 20, 156, 44, ["Digital transducer"], size=12)
    c.label(14, 152, "Pe", anchor="start", mono=True, size=12)
    c.arrow(48, 148, 96, 148)
    c.box(100, 126, 156, 44, ["Two washouts", "and a low-pass"], size=11)
    bands = [
        (30, "Low band", "KL1(KL11 + sTL1)"),
        (114, "Intermediate band", "KI1(KI11 + sTI1)"),
        (198, "High band", "KH1(KH11 + sTH1)"),
    ]
    ax = 700
    for by, title, expr in bands:
        c.box(340, by, 240, 54, [title, expr])
        c.path(f"M 256 {by + 27} L 340 {by + 27}" if by != 198 else
               f"M 256 148 L 300 148 L 300 {by + 27} L 340 {by + 27}", arrow=True)
        c.path(f"M 580 {by + 27} L {ax} {by + 27} L {ax} 130", arrow=False)
    c.summing(ax, 116, ("", ""))
    c.arrow(ax + 13, 116, ax + 60, 116)
    c.box(ax + 64, 94, 130, 44, ["Limits", "VSTMIN, VSTMAX"], size=11)
    c.arrow(ax + 194, 116, ax + 234, 116)
    c.label(ax + 242, 121, "VPSS", anchor="start", mono=True, size=12)
    return c


def pss_ieeest(t):
    c = Canvas(1180, 180, t)
    y = 40
    c.label(14, y + 33, "VS1", anchor="start", mono=True, size=12)
    boxes, x = c.chain(58, y, [
        (152, ["2nd-order filter", "1 / (A2 + sA1 + ...)"]),
        (152, ["2nd-order filter", "(A6 + sA5 + ...)"]),
        (134, ["Lead-lag", "(1+sT1)/(1+sT2)"]),
        (134, ["Lead-lag", "(1+sT3)/(1+sT4)"]),
        (146, ["Washout", "KS&#183;sT5 / T6 / (1+sT6)"]),
    ], gap=24)
    c.arrow(x, y + 27, x + 40, y + 27)
    c.box(x + 44, y, 120, 54, ["Clamp", "LSMIN, LSMAX"], size=11)
    c.arrow(x + 164, y + 27, x + 200, y + 27)
    c.label(x + 208, y + 32, "VPSS", anchor="start", mono=True, size=12)
    c.label(560, 156, "The input signal is selectable: speed, electrical power, "
                      "or accelerating power.", size=11, muted=True, italic=True)
    return c


def pss_stab3(t):
    c = Canvas(1000, 170, t)
    y = 40
    c.label(14, y + 33, "Pe", anchor="start", mono=True, size=12)
    boxes, x = c.chain(50, y, [
        (140, ["Lag 1 / (1 + sTt)"]),
        (144, ["Lag 1 / (1 + sTX1)"]),
        (160, ["Washout", "&#8722;KX&#183;s / (1 + sTX2)"]),
        (128, ["Clamp &#177; VLIM"]),
    ])
    c.arrow(x, y + 27, x + 44, y + 27)
    c.label(x + 52, y + 32, "VPSS", anchor="start", mono=True, size=12)
    return c


# ------------------------------------------------------------- limiters
def exc_maxex2(t):
    c = Canvas(1120, 250, t)
    y = 30
    c.label(14, y + 33, "Ifd or Efd", anchor="start", mono=True, size=12)
    boxes, x = c.chain(96, y, [
        (176, ["Timer, three points", "(Ifd, T)"]),
        (150, ["Hysteresis latch", "when timer &#8805; 1"], "accent"),
    ])
    c.arrow(x, y + 27, x + 44, y + 27)
    c.label(x + 52, y + 32, "latched", anchor="start", size=11, muted=True, italic=True)

    py = y + 130
    c.label(14, py + 33, "Ifd,ref", anchor="start", mono=True, size=12)
    sx, sy = 128, py + 27
    c.arrow(76, sy, sx - 13, sy)
    c.summing(sx, sy, ("+", "&#8722;"))
    c.label(sx, sy + 52, "Ifd,mes", size=11, muted=True, mono=True)
    c.arrow(sx, sy + 38, sx, sy + 13)
    c.wire(sx + 30, sy, "eIFD")
    boxes2, x2 = c.chain(sx + 13, py, [
        (188, ["Limited integrator", "1 / KOEL, gated by the latch"]),
    ])
    c.arrow(x2, sy, x2 + 44, sy)
    c.label(x2 + 52, sy + 5, "VOEL", anchor="start", mono=True, size=12)
    c.label(x2 + 52, sy + 26, "injected at the reference summation",
            anchor="start", size=11, muted=True, italic=True)
    return c


def exc_integral_oel(t):
    c = Canvas(1120, 190, t)
    y = 40
    c.label(14, y + 33, "Ifd", anchor="start", mono=True, size=12)
    sx, sy = 130, y + 27
    c.arrow(52, sy, sx - 13, sy)
    c.summing(sx, sy, ("+", "&#8722;"))
    c.label(sx, sy + 54, "1.05&#183;IFDN", size=11, muted=True, mono=True)
    c.arrow(sx, sy + 40, sx, sy + 13)
    boxes, x = c.chain(sx + 13, y, [
        (166, ["Input clamp", "min(&#916;Ifd, 0.35&#183;IFDN)"]),
        (170, ["Integrator 1 / TOEL", "limits LOEL, UOEL"]),
        (166, ["Gain KOEL, clamp", "OELLI to 0"], "accent"),
    ])
    c.arrow(x, sy, x + 44, sy)
    c.label(x + 52, sy + 5, "VOEL", anchor="start", mono=True, size=12)
    c.label(560, 168, "The stator current limiter has the same structure on the "
                      "stator current.", size=11, muted=True, italic=True)
    return c


# ------------------------------------------------------ other exciters
def exc_generic1(t):
    c = Canvas(1180, 300, t)
    y = 26
    c.label(14, y + 33, "V", anchor="start", mono=True, size=12)
    sx, sy = 640, y + 27
    c.arrow(40, sy, sx - 13, sy)
    c.summing(sx, sy, ("&#8722;", "+"))
    c.label(sx - 44, sy - 36, "Vref", size=11, muted=True, mono=True)
    c.arrow(sx, sy - 42, sx, sy - 13)
    boxes, x = c.chain(sx + 13, y, [
        (178, ["AVR", "G(1 + sTA) / (1 + sTB)"]),
        (172, ["Exciter 1 / (1 + sTE)", "limits L3, L4"], "accent"),
    ])
    c.arrow(x, sy, x + 44, sy)
    c.label(x + 52, sy + 5, "vf", anchor="start", mono=True, size=12)

    py = y + 130
    c.label(14, py + 33, "&#969; or P", anchor="start", mono=True, size=12)
    boxes2, x2 = c.chain(76, py, [
        (150, ["Washout", "KPSS&#183;sTW / (1+sTW)"]),
        (140, ["Lead-lag", "(1+sT1) / (1+sT2)"]),
        (140, ["Lead-lag", "(1+sT3) / (1+sT4)"]),
    ], gap=26)
    c.wire(x2 + 30, py + 27, "VPSS")
    c.path(f"M {x2} {py + 27} L {sx} {py + 27} L {sx} {sy + 13}", arrow=True)

    oy = y + 226
    c.label(14, oy + 20, "Ifd", anchor="start", mono=True, size=12)
    c.arrow(52, oy + 16, 130, oy + 16)
    c.box(134, oy - 6, 210, 44, ["Inverse-time OEL"], size=12)
    c.path(f"M 344 {oy + 16} L {sx} {oy + 16} L {sx} {py + 27}", arrow=False)
    c.dot(sx, py + 27)
    c.wire(sx + 44, oy + 16, "VOEL", dy=-10)
    return c


def exc_avr_dg(t):
    c = Canvas(1180, 300, t)
    y = 26
    c.label(14, y + 33, "V", anchor="start", mono=True, size=12)
    sx, sy = 640, y + 27
    c.arrow(40, sy, sx - 13, sy)
    c.summing(sx, sy, ("&#8722;", "+"))
    c.label(sx - 44, sy - 36, "Vref", size=11, muted=True, mono=True)
    c.arrow(sx, sy - 42, sx, sy - 13)
    boxes, x = c.chain(sx + 13, y, [
        (178, ["AVR", "G(1 + sTA) / (1 + sTB)"]),
        (172, ["Exciter 1 / (1 + sTE)", "limits L3, L4"], "accent"),
    ])
    c.arrow(x, sy, x + 44, sy)
    c.label(x + 52, sy + 5, "vf", anchor="start", mono=True, size=12)

    py = y + 122
    c.label(14, py + 33, "&#969; or P", anchor="start", mono=True, size=12)
    boxes2, x2 = c.chain(76, py, [
        (150, ["Washout", "KPSS&#183;sTW / (1+sTW)"]),
        (140, ["Lead-lag", "(1+sT1) / (1+sT2)"]),
        (140, ["Lead-lag", "(1+sT3) / (1+sT4)"]),
    ], gap=26)
    c.wire(x2 + 30, py + 27, "VPSS")
    c.path(f"M {x2} {py + 27} L {sx} {py + 27} L {sx} {sy + 13}", arrow=True)

    qy = y + 226
    c.label(14, qy + 20, "Q* &#8722; Q", anchor="start", mono=True, size=12)
    c.arrow(84, qy + 16, 160, qy + 16)
    c.box(164, qy - 6, 214, 44, ["Reactive-power PI", "KQP + KQI / s"], "accent")
    c.path(f"M 378 {qy + 16} L {sx} {qy + 16} L {sx} {py + 27}", arrow=False)
    c.dot(sx, py + 27)
    c.wire(sx - 120, qy + 16, "&#916;VQ", dy=-10)
    c.label(760, qy + 21, "Everything else is GENERIC1, unchanged.",
            anchor="start", size=11, muted=True, italic=True)
    return c


def exc_generic2(t):
    c = Canvas(1180, 300, t)
    y = 26
    c.label(14, y + 33, "V, Id, Iq", anchor="start", mono=True, size=12)
    boxes, x = c.chain(90, y, [(160, ["Compensator", "V + Xc&#183;Iq &#8722; Rc&#183;Id"])])
    sx, sy = x + 50, y + 27
    c.arrow(x, sy, sx - 13, sy)
    c.wire(x + 20, sy, "Vc")
    c.summing(sx, sy, ("&#8722;", "+"))
    c.label(sx - 44, sy - 36, "Vref", size=11, muted=True, mono=True)
    c.arrow(sx, sy - 42, sx, sy - 13)
    boxes2, x2 = c.chain(sx + 13, y, [
        (198, ["PI + proportional", "KP + KI/s + C(1+sTC)/(1+sTB)"]),
        (150, ["Amplifier KA / (1+sTA)"]),
        (176, ["AC exciter 1 / sTE", "KE&#183;VE + SE(VE)"], "accent"),
    ])
    c.arrow(x2, sy, x2 + 40, sy)
    c.label(x2 + 48, sy + 5, "vf", anchor="start", mono=True, size=12)

    py = y + 150
    c.label(14, py + 33, "&#969; or P", anchor="start", mono=True, size=12)
    boxes3, x3 = c.chain(76, py, [
        (150, ["Washout and", "two lead-lag stages"]),
    ])
    c.wire(x3 + 30, py + 27, "VPSS")
    c.path(f"M {x3} {py + 27} L {sx} {py + 27} L {sx} {sy + 13}", arrow=True)
    c.label(14, py + 118, "Ifd", anchor="start", mono=True, size=12)
    c.arrow(52, py + 114, 130, py + 114)
    c.box(134, py + 92, 176, 44, ["OEL"], size=12)
    c.path(f"M 310 {py + 114} L {sx} {py + 114} L {sx} {py + 27}", arrow=False)
    c.dot(sx, py + 27)
    c.wire(sx + 44, py + 114, "VOEL", dy=-10)
    return c


def exc_generic(t):
    c = Canvas(1180, 290, t)
    y = 26
    c.label(14, y + 33, "V", anchor="start", mono=True, size=12)
    sx, sy = 640, y + 27
    c.arrow(40, sy, sx - 13, sy)
    c.summing(sx, sy, ("&#8722;", "+"))
    c.label(sx - 40, sy - 36, "V0", size=11, muted=True, mono=True)
    c.arrow(sx, sy - 42, sx, sy - 13)
    boxes, x = c.chain(sx + 13, y, [
        (176, ["TGR", "G(1 + sTa) / (1 + sTb)"]),
        (176, ["Exciter 1 / (1 + sTe)", "limits Vfmin, Vfmax"], "accent"),
    ])
    c.arrow(x, sy, x + 44, sy)
    c.label(x + 52, sy + 5, "vf", anchor="start", mono=True, size=12)

    py = y + 126
    c.label(14, py + 33, "&#969;", anchor="start", mono=True, size=13)
    boxes2, x2 = c.chain(50, py, [
        (150, ["Washout", "KPSS&#183;sTW / (1+sTW)"]),
        (140, ["Lead-lag", "(1+sT1) / (1+sT2)"]),
        (140, ["Lead-lag", "(1+sT3) / (1+sT4)"]),
    ], gap=26)
    c.wire(x2 + 30, py + 27, "VPSS")
    c.path(f"M {x2} {py + 27} L {sx} {py + 27} L {sx} {sy + 13}", arrow=True)

    oy = y + 216
    c.label(14, oy + 20, "Ifd", anchor="start", mono=True, size=12)
    c.arrow(52, oy + 16, 130, oy + 16)
    c.box(134, oy - 6, 210, 44, ["OEL"], size=12)
    c.path(f"M 344 {oy + 16} L {sx} {oy + 16} L {sx} {py + 27}", arrow=False)
    c.dot(sx, py + 27)
    c.wire(sx + 44, oy + 16, "VOEL", dy=-10)
    return c


# ------------------------------------------------------------- injectors
def inj_wt3(t):
    """The WECC composite structure the engine actually implements: an
    electrical chain across the top, the mechanical one below it."""
    c = Canvas(1240, 480, t)
    ey = 67
    c.label(14, ey + 5, "Pref, Vref", anchor="start", mono=True, size=12)
    c.arrow(92, ey, 140, ey)
    c.box(140, 40, 180, 54, ["Plant controller", "REPC_A"], size=12)
    c.arrow(320, ey, 500, ey)
    c.box(500, 40, 200, 54, ["Electrical controller", "REEC_A"], size=12)
    c.arrow(700, ey, 760, ey)
    c.box(760, 40, 180, 54, ["Generator interface", "REGC_A"], accent=True, size=12)
    c.arrow(940, ey, 1040, ey)
    c.label(1048, ey + 5, "ix, iy", anchor="start", mono=True, size=13)

    my = 277
    c.label(14, my + 5, "Wind speed", anchor="start", mono=True, size=12)
    c.arrow(112, my, 140, my)
    c.box(140, 250, 180, 54, ["Aerodynamic rotor", "WTGAR_A"], size=12)
    c.arrow(320, my, 380, my)
    c.box(380, 250, 200, 54, ["Two-mass drivetrain", "WTGT_A"], size=12)
    c.arrow(580, my, 700, my)
    c.wire(636, my, "&#969;g")
    c.box(700, 250, 200, 54, ["Torque controller", "WTGTRQ_A"], size=12)

    # electrical torque acts on the shaft, straight down between the two rows
    c.path("M 540 94 L 540 250", arrow=True)
    c.label(552, 178, "Te", anchor="start", mono=True, size=12, muted=True)

    # the speed-power characteristic sets the active power order
    c.path("M 900 277 L 1010 277 L 1010 160 L 600 160 L 600 94", arrow=True)
    c.label(806, 152, "Te,ref from the speed-power table", size=11, muted=True, italic=True)

    # and the same speed drives the pitch
    c.dot(650, my)
    c.path("M 650 277 L 650 407 L 580 407", arrow=True)
    c.box(380, 380, 200, 54, ["Pitch controller", "WTGPT_A"], size=12)
    c.path("M 380 407 L 230 407 L 230 304", arrow=True)
    c.label(244, 400, "pitch angle", anchor="start", size=11, muted=True, italic=True)
    return c


def inj_wt4(t):
    c = Canvas(1360, 400, t)
    ey = 67
    c.label(14, ey + 5, "Pref, Vref", anchor="start", mono=True, size=12)
    c.arrow(92, ey, 140, ey)
    c.box(140, 40, 180, 54, ["Plant controller", "REPC_A"], size=12)
    c.arrow(320, ey, 380, ey)
    c.box(380, 40, 190, 54, ["Power order ramp", "dPmax, dPmin"], accent=True, size=12)
    c.arrow(570, ey, 630, ey)
    c.box(630, 40, 200, 54, ["Electrical controller", "REEC_A"], size=12)
    c.arrow(830, ey, 890, ey)
    c.box(890, 40, 180, 54, ["Generator interface", "REGC_A"], accent=True, size=12)
    c.arrow(1070, ey, 1170, ey)
    c.label(1178, ey + 5, "ix, iy", anchor="start", mono=True, size=13)

    my = 257
    c.label(452, my + 5, "Tm", anchor="start", mono=True, size=12)
    c.arrow(500, my, 630, my)
    c.box(630, 230, 240, 54, ["Two-mass drivetrain", "WTGT_A"], size=12)
    c.arrow(870, my, 970, my)
    c.label(978, my + 5, "&#969;g", anchor="start", mono=True, size=13)
    c.path("M 710 94 L 710 230", arrow=True)
    c.label(722, 168, "Te", anchor="start", mono=True, size=12, muted=True)
    c.label(680, 330, "There is no pitch controller or aerodynamic rotor: all the power "
                      "passes through the converter.", size=11, muted=True, italic=True)
    return c


def tor_thermal_generic1(t):
    c = Canvas(1340, 520, t)
    gy = 67
    c.label(14, gy + 5, "&#969;", anchor="start", mono=True, size=13)
    c.summing(110, gy, ("+", "&#8722;"))
    c.arrow(42, gy, 97, gy)
    c.label(110, gy + 66, "1", size=13, muted=True, mono=True)
    c.arrow(110, gy + 52, 110, gy + 13)
    c.arrow(123, gy, 160, gy)
    c.box(160, 40, 90, 54, ["1 / &#963;"], size=13)
    c.arrow(250, gy, 290, gy)
    c.box(290, 40, 150, 54, ["1 / (1 + sTmes)"], size=12)
    c.summing(500, gy, ("&#8722;", "&#8722;"))
    c.label(524, gy - 24, "+", size=13)
    c.arrow(440, gy, 487, gy)
    c.label(500, 20, "P0", size=12, muted=True, mono=True)
    c.arrow(500, 26, 500, gy - 13)
    c.arrow(513, gy, 550, gy)
    c.box(550, 40, 100, 54, ["1 / Tsm"], size=13)
    c.arrow(650, gy, 690, gy)
    c.box(690, 40, 160, 54, ["Rate limits", "zdotmin, zdotmax"], accent=True, size=11)
    c.arrow(850, gy, 890, gy)
    c.box(890, 40, 140, 54, ["1 / s", "zmin, zmax"], accent=True, size=12)
    c.arrow(1030, gy, 1110, gy)
    c.label(1118, gy + 5, "z", anchor="start", mono=True, size=13)

    # the gate position closes the governor loop, and drives the turbine below
    c.dot(1070, gy)
    c.path(f"M 1070 {gy} L 1070 150 L 500 150 L 500 {gy + 13}", arrow=True)
    c.dot(1070, 150)
    c.path("M 1070 150 L 1070 200 L 60 200 L 60 277 L 120 277", arrow=True)

    ty = 277
    c.box(120, 250, 150, 54, ["1 / (1 + sThp)"], size=12)
    c.arrow(270, ty, 320, ty)
    c.box(320, 250, 150, 54, ["1 / (1 + sTr)"], size=12)
    c.arrow(470, ty, 520, ty)
    c.box(520, 250, 150, 54, ["1 / (1 + sTlp)"], size=12)
    c.arrow(670, ty, 710, ty)
    c.box(710, 250, 150, 54, ["1 &#8722; Fhp &#8722; Fmp"], size=12)

    c.summing(900, ty, ("+", "+"))
    c.arrow(860, ty, 887, ty)
    c.summing(1000, ty, ("+", "+"))
    c.arrow(913, ty, 987, ty)

    c.dot(295, ty)
    c.path("M 295 277 L 295 440 L 700 440", arrow=True)
    c.box(700, 413, 120, 54, ["Fhp"], size=13)
    c.path("M 820 440 L 1000 440 L 1000 290", arrow=True)

    c.dot(495, ty)
    c.path("M 495 277 L 495 358 L 700 358", arrow=True)
    c.box(700, 331, 120, 54, ["Fmp &#183; ivo"], size=12)
    c.path("M 820 358 L 900 358 L 900 290", arrow=True)

    c.arrow(1013, ty, 1080, ty)
    c.wire(1046, ty, "Pm")
    c.box(1080, 250, 120, 54, ["Pm / &#969;"], size=13)
    c.arrow(1200, ty, 1260, ty)
    c.label(1268, ty + 5, "Tm", anchor="start", mono=True, size=13)
    c.label(1140, 340, "&#969;", mono=True, size=12, muted=True)
    c.arrow(1140, 326, 1140, 304)
    c.label(600, 500, "The reheat stage carries the initial valve opening ivo as a "
                      "factor, in the lag and in the fraction alike.",
            size=11, muted=True, italic=True)
    return c


# --------------------------------------------- grid-following converter
def gfol_pll(t):
    c = Canvas(1140, 400, t)
    my = 161
    c.label(14, my + 5, "vx, vy", anchor="start", mono=True, size=12)
    c.arrow(76, my, 110, my)
    c.box(110, 134, 230, 54, ["vq = vy cos &#948;g &#8722; vx sin &#948;g"], size=12)
    c.path(f"M 92 {my} L 92 57 L 150 57", arrow=True)
    c.dot(92, my)
    c.box(150, 30, 170, 54, ["V = &#8730;(vx&#178; + vy&#178;)"], size=12)
    c.arrow(320, 57, 360, 57)
    c.box(360, 30, 200, 54, ["Blocking hysteresis", "block &lt; Vpllb, release &gt; Vpllu"],
          accent=True, size=11)

    # the block signal gates both integrators, on one vertical
    c.arrow(340, my, 447, my)
    c.wire(400, my, "vq")
    c.path("M 460 84 L 460 287", arrow=True)
    c.mult(460, my)

    c.arrow(473, my, 580, my)
    c.dot(520, my)
    c.box(580, 137, 130, 48, ["Kp&#969;"], size=13)
    c.path(f"M 520 {my} L 520 90 L 580 90", arrow=True)
    c.box(580, 66, 130, 48, ["Ki&#969; / s"], size=13)
    c.summing(790, my, ("+", "+"))
    c.arrow(710, my, 777, my)
    c.path(f"M 710 90 L 790 90 L 790 {my - 13}", arrow=True)
    c.arrow(803, my, 1000, my)
    c.label(1008, my + 5, "&#969;g", anchor="start", mono=True, size=13)

    # and the angle comes back round the bottom, right to left
    c.dot(950, my)
    c.path(f"M 950 {my} L 950 300 L 900 300", arrow=True)
    c.box(800, 276, 100, 48, ["&#969;N"], size=13)
    c.summing(700, 300, ("+", "&#8722;"))
    c.arrow(800, 300, 713, 300)
    c.label(700, 372, "&#969;ref", size=12, muted=True, mono=True)
    c.arrow(700, 358, 700, 313)
    c.arrow(687, 300, 473, 300)
    c.mult(460, 300)
    c.arrow(447, 300, 384, 300)
    c.box(300, 276, 84, 48, ["1 / s"], size=13)
    c.path("M 300 300 L 200 300 L 200 188", arrow=True)
    c.wire(246, 300, "&#948;g", dy=-9)
    c.label(560, 388, "The PLL freezes while the terminal voltage is below Vpllb, and "
                      "resumes above Vpllu.", size=11, muted=True, italic=True)
    return c


def gfol_currentctl(t):
    c = Canvas(1080, 430, t)
    for row, (ref, meas, out, cross, sign) in enumerate((
            ("id", "id", "vmd", "&#969;g L iq", "&#8722;"),
            ("iq", "iq", "vmq", "&#969;g L id", "+"))):
        y = 140 + row * 190
        c.label(14, y + 5, f"{ref}ref", anchor="start", mono=True, size=12)
        c.summing(150, y, ("+", "&#8722;"))
        c.arrow(70, y, 137, y)
        c.label(150, y + 62, meas, size=12, muted=True, mono=True)
        c.arrow(150, y + 48, 150, y + 13)
        c.arrow(163, y, 300, y)
        c.dot(220, y)
        c.box(300, y - 24, 110, 48, ["Kp"], size=13)
        c.path(f"M 220 {y} L 220 {y - 72} L 300 {y - 72}", arrow=True)
        c.box(300, y - 96, 110, 48, ["Ki / s"], size=13)
        c.summing(480, y, ("+", "+"))
        c.arrow(410, y, 467, y)
        c.path(f"M 410 {y - 72} L 480 {y - 72} L 480 {y - 13}", arrow=True)
        c.summing(620, y, ("+", sign))
        c.arrow(493, y, 607, y)
        c.label(620, y + 62, cross, size=12, muted=True, mono=True)
        c.arrow(620, y + 48, 620, y + 13)
        if row == 0:
            c.label(620, y - 62, "vd / r", size=12, muted=True, mono=True)
            c.arrow(620, y - 48, 620, y - 13)
        c.arrow(633, y, 730, y)
        c.label(738, y + 5, out, anchor="start", mono=True, size=13)
    return c


def gfol_pctl(t):
    c = Canvas(1200, 470, t)
    y = 130
    c.label(14, y + 5, "P", anchor="start", mono=True, size=12)
    c.arrow(44, y, 100, y)
    c.box(100, y - 27, 160, 54, ["1 / (1 + sTlpf)"], size=12)
    c.summing(340, y, ("+", "&#8722;"))
    c.arrow(260, y, 327, y)
    c.label(340, y - 62, "P0", size=12, muted=True, mono=True)
    c.arrow(340, y - 48, 340, y - 13)
    c.arrow(353, y, 450, y)
    c.dot(400, y)
    c.box(450, y - 27, 140, 54, ["Kip / s", "&#177;Idmax"], accent=True, size=12)
    c.path(f"M 400 {y} L 400 {y - 76} L 450 {y - 76}", arrow=True)
    c.box(450, y - 100, 140, 48, ["Kpp"], size=13)
    c.summing(680, y, ("+", "+"))
    c.arrow(590, y, 667, y)
    c.path(f"M 590 {y - 76} L 680 {y - 76} L 680 {y - 13}", arrow=True)
    c.arrow(693, y, 800, y)
    c.wire(746, y, "id_pi")
    c.box(800, y - 27, 150, 54, ["Limiter", "&#177;Idmax"], accent=True, size=12)
    c.arrow(950, y, 1010, y)
    c.label(1018, y + 5, "idref", anchor="start", mono=True, size=13)

    # the d-axis headroom, which the reactive current gets first claim on
    y2 = 340
    c.label(14, y2 + 5, "iq", anchor="start", mono=True, size=12)
    c.arrow(48, y2, 100, y2)
    c.box(100, y2 - 27, 190, 54, ["&#8730;max(Imax&#178; &#8722; iq&#178;, 0)"], size=12)
    c.summing(370, y2, ("+", "&#8722;"))
    c.arrow(290, y2, 357, y2)
    c.arrow(383, y2, 440, y2)
    c.box(440, y2 - 27, 110, 54, ["1 / Trlim"], size=12)
    c.arrow(550, y2, 600, y2)
    c.box(600, y2 - 27, 170, 54, ["Rate limits", "dPdt_min, dPdt_max"], accent=True, size=11)
    c.arrow(770, y2, 820, y2)
    c.box(820, y2 - 27, 150, 54, ["1 / s", "&#177;Imax"], accent=True, size=12)
    c.arrow(970, y2, 1030, y2)
    c.label(1038, y2 + 5, "Idmax", anchor="start", mono=True, size=13)
    c.dot(1000, y2)
    c.path(f"M 1000 {y2} L 1000 {y2 + 78} L 370 {y2 + 78} L 370 {y2 + 13}", arrow=True)
    c.path(f"M 875 {y2 - 27} L 875 {y - 27 + 54 + 46}", arrow=False, dash=True)
    c.path(f"M 875 {y + 74} L 875 {y + 27}", arrow=True, dash=True)
    c.label(940, y + 62, "sets the limits above", size=11, muted=True, italic=True)
    return c


def gfol_qctl(t):
    c = Canvas(1320, 470, t)
    ya, yb = 96, 204
    c.label(14, ya + 5, "Vcomp", anchor="start", mono=True, size=12)
    c.arrow(88, ya, 130, ya)
    c.box(130, ya - 24, 150, 48, ["1 / (1 + sTlpf)"], size=12)
    c.summing(350, ya, ("+", "&#8722;"))
    c.arrow(280, ya, 337, ya)
    c.label(350, ya - 54, "Vcomp0", size=11, muted=True, mono=True)
    c.arrow(350, ya - 42, 350, ya - 13)

    c.label(14, yb + 5, "Q", anchor="start", mono=True, size=12)
    c.arrow(44, yb, 130, yb)
    c.box(130, yb - 24, 150, 48, ["1 / (1 + sTlpf)"], size=12)
    c.summing(350, yb, ("+", "&#8722;"))
    c.arrow(280, yb, 337, yb)
    c.label(350, yb + 58, "Q0", size=11, muted=True, mono=True)
    c.arrow(350, yb + 44, 350, yb + 13)

    # one of the two, chosen by vqswitch, and zeroed while the voltage is very low
    sw = 470
    c.path(f"M 363 {ya} L {sw} {ya} L {sw} 136", arrow=False)
    c.path(f"M 363 {yb} L {sw} {yb} L {sw} 164", arrow=False)
    c.label(sw + 4, ya - 12, "vqswitch = 1", anchor="start", size=11, muted=True, mono=True)
    c.label(sw + 4, yb + 22, "vqswitch = 0", anchor="start", size=11, muted=True, mono=True)
    c.path(f"M {sw} 136 L {sw} 164", arrow=False, dash=True)
    c.dot(sw, ya)
    c.dot(sw, yb)
    my = 150
    c.arrow(sw, my, 587, my)
    c.mult(600, my)
    c.box(430, 320, 220, 54, ["Freeze below Vs2", "gate is 0, else 1"], accent=True, size=12)
    c.path(f"M 600 320 L 600 {my + 13}", arrow=True)
    c.label(300, 352, "V", anchor="start", mono=True, size=12)
    c.arrow(330, 347, 430, 347)

    c.arrow(613, my, 700, my)
    c.dot(660, my)
    c.box(700, my - 24, 130, 48, ["Kiv / s", "&#177;iq1max"], accent=True, size=12)
    c.path(f"M 660 {my} L 660 {my - 74} L 700 {my - 74}", arrow=True)
    c.box(700, my - 98, 130, 48, ["Kpv"], size=13)
    c.summing(900, my, ("+", "+"))
    c.arrow(830, my, 887, my)
    c.path(f"M 830 {my - 74} L 900 {my - 74} L 900 {my - 13}", arrow=True)
    c.arrow(913, my, 970, my)
    c.box(970, my - 24, 130, 48, ["&#177;iq1max"], accent=True, size=12)
    c.wire(1120, my, "iq1", dy=-11)
    c.arrow(1100, my, 1147, my)
    c.summing(1160, my, ("+", "+"))
    c.arrow(1173, my, 1220, my)
    c.box(1220, my - 24, 120, 48, ["&#177;Imax"], accent=True, size=12)
    c.arrow(1340, my, 1390, my)
    c.label(1398, my + 5, "iqref", anchor="start", mono=True, size=13)

    # the dynamic voltage support branch
    c.box(760, 320, 300, 54, ["Dynamic voltage support: 0 above Vs1,",
                              "ramping to &#8722;Imax at Vs2"], accent=True, size=11)
    c.dot(400, 347)
    c.path("M 400 347 L 400 430 L 706 430 L 706 347 L 760 347", arrow=True)
    c.path(f"M 1060 347 L 1160 347 L 1160 {my + 13}", arrow=True)
    c.wire(1118, 347, "iq2", dy=-9)
    return c


# ---------------------------------------------- grid-forming converter
def gfor_vsm(t):
    c = Canvas(1260, 400, t)
    my = 200
    c.label(14, my + 5, "P*", anchor="start", mono=True, size=12)
    c.summing(140, my, ("+", "+"))
    c.arrow(52, my, 127, my)
    c.summing(300, my, ("+", "&#8722;"))
    c.label(324, my - 26, "&#8722;", size=13)
    c.arrow(153, my, 287, my)
    c.label(300, my + 62, "Pvirt", size=12, muted=True, mono=True)
    c.arrow(300, my + 48, 300, my + 13)
    c.arrow(313, my, 380, my)
    c.box(380, my - 27, 130, 54, ["1 / 2Hs"], size=13)
    c.path(f"M 510 {my} L 620 {my}", arrow=False)
    c.wire(566, my, "&#969;m")
    c.dot(620, my)
    c.box(680, my - 27, 100, 54, ["&#969;N"], size=13)
    c.arrow(620, my, 680, my)
    c.summing(860, my, ("+", "&#8722;"))
    c.arrow(780, my, 847, my)
    c.label(860, my + 62, "&#969;ref", size=12, muted=True, mono=True)
    c.arrow(860, my + 48, 860, my + 13)
    c.arrow(873, my, 940, my)
    c.box(940, my - 27, 100, 54, ["1 / s"], size=13)
    c.arrow(1040, my, 1100, my)
    c.label(1108, my + 5, "&#948;m", anchor="start", mono=True, size=13)

    # damping against the PLL estimate of grid frequency
    ty = 62
    c.summing(620, ty, ("", "+"))
    c.path(f"M 620 {my} L 620 {ty + 13}", arrow=True)
    c.box(1000, ty - 24, 90, 48, ["PLL"], accent=True, size=13)
    c.arrow(1000, ty, 633, ty)
    c.wire(760, ty, "&#969;g")
    c.label(648, ty - 20, "&#8722;", size=13)
    c.box(400, ty - 24, 90, 48, ["D"], size=13)
    c.arrow(607, ty, 490, ty)
    c.path(f"M 400 {ty} L 300 {ty} L 300 {my - 13}", arrow=True)

    # optional droop on the same speed
    by = 340
    c.summing(620, by, ("", ""))
    c.path(f"M 620 {my} L 620 {by - 13}", arrow=True)
    c.label(598, by - 20, "&#8722;", size=13)
    c.label(648, by + 20, "+", size=13)
    c.label(720, by + 5, "1", anchor="start", mono=True, size=13)
    c.arrow(716, by, 633, by)
    c.box(400, by - 24, 100, 48, ["1 / Rdroop"], size=12)
    c.arrow(607, by, 500, by)
    c.path(f"M 400 {by} L 140 {by} L 140 {my + 13}", arrow=True)
    return c


def gfor_currentlim(t):
    c = Canvas(620, 500, t)
    ox, oy = 110, 420          # origin
    r = 250                    # the Imax circle
    tt = c.t
    c.path(f"M {ox} {oy} L {ox + 430} {oy}", arrow=True)
    c.path(f"M {ox} {oy} L {ox} {oy - 380}", arrow=False)
    c.path(f"M {ox} {oy - 380} L {ox} {oy - 392}", arrow=True)
    c.label(ox + 448, oy + 6, "id", anchor="start", mono=True, size=13)
    c.label(ox - 6, oy - 400, "iq", anchor="end", mono=True, size=13)

    # the limit circle
    c.parts.append(
        f'<path d="M {ox} {oy - r} A {r} {r} 0 0 1 {ox + r} {oy}" fill="none" '
        f'stroke="{tt["accent"]}" stroke-width="1.6"/>')
    c.label(ox + 190, oy - 230, "I = Imax", size=13, muted=True, mono=True)

    # the unsaturated command, and where it lands after scaling
    dx, dy = 350, 210
    sx, sy = 0.0, 0.0
    import math
    k = r / math.hypot(dx, dy)
    sx, sy = dx * k, dy * k
    c.path(f"M {ox} {oy} L {ox + dx} {oy - dy}", arrow=True)
    c.dot(ox + dx, oy - dy)
    c.dot(ox + sx, oy - sy)
    for px, py, xl, yl in ((dx, dy, "id*", "iq*"), (sx, sy, "ids*", "iqs*")):
        c.path(f"M {ox} {oy - py} L {ox + px} {oy - py}", arrow=False, dash=True)
        c.path(f"M {ox + px} {oy} L {ox + px} {oy - py}", arrow=False, dash=True)
        c.label(ox - 10, oy - py + 5, yl, anchor="end", mono=True, size=12, muted=True)
        c.label(ox + px, oy + 22, xl, mono=True, size=12, muted=True)

    c.parts.append(
        f'<path d="M {ox + dx - 20} {oy - dy - 6} Q {ox + 250} {oy - 290} '
        f'{ox + sx + 6} {oy - sy - 14}" fill="none" stroke="{tt["accent"]}" '
        f'stroke-width="1.6" marker-end="url(#arrow-accent)"/>')
    c.label(310, 482, "Both components are scaled by the same factor, so the angle of "
                      "the current is kept.", size=11, muted=True, italic=True)
    return c


def dctl_ltc_timing(t):
    """A tap changer is an automaton, not a transfer function, so the useful
    picture is the sequence in time rather than a signal path."""
    c = Canvas(1020, 350, t)
    x0, x1 = 96, 900
    band_top, band_bot = 92, 126
    taps = (392, 546, 700)
    dist = 226

    # -- the monitored voltage
    c.label(30, 60, "V", anchor="start", mono=True, size=13)
    c.band(x0, band_top, x1 - x0, band_bot - band_top, "Vset &#177; &#948;V")
    c.path(f"M {x0} 186 L {x1 + 30} 186", arrow=True)
    c.path(f"M {x0} 40 L {x0} 186", arrow=False)
    c.path(f"M {x0} 110 L {dist} 110 L {dist} 168 "
           f"L {taps[0]} 168 L {taps[0]} 154 "
           f"L {taps[1]} 154 L {taps[1]} 138 "
           f"L {taps[2]} 138 L {taps[2]} 114 L {x1} 114",
           arrow=False)

    # -- the tap position it produces
    c.label(18, 268, "tap", anchor="start", mono=True, size=13)
    c.path(f"M {x0} 316 L {x1 + 30} 316", arrow=True)
    c.path(f"M {x0} 232 L {x0} 316", arrow=False)
    c.path(f"M {x0} 300 L {taps[0]} 300 L {taps[0]} 278 "
           f"L {taps[1]} 278 L {taps[1]} 256 "
           f"L {taps[2]} 256 L {taps[2]} 234 L {x1} 234",
           arrow=False)
    c.label(x1 + 34, 330, "t", anchor="start", mono=True, size=13)

    # -- the instants that matter, and the delay that separates them
    for x, text in ((dist, "disturbance"), (taps[0], ""), (taps[1], ""), (taps[2], "")):
        c.path(f"M {x} 44 L {x} 322", arrow=False, dash=True)
        if text:
            c.label(x, 34, text, size=13, muted=True, italic=True)
    for a, b, text in ((dist, taps[0], "delay_first"),
                       (taps[0], taps[1], "delay_next"),
                       (taps[1], taps[2], "delay_next")):
        c.path(f"M {a} 210 L {b} 210", arrow=False)
        c.path(f"M {a} 204 L {a} 216 M {b} 204 L {b} 216", arrow=False)
        c.label((a + b) / 2, 202, text, size=13, muted=True, mono=True)

    c.label(510, 344, "The tap holds once the voltage is back inside the deadband, and "
                      "stops at ratio_min or ratio_max.",
            size=13, muted=True, italic=True)
    return c


def dctl_relay_timing(t):
    """Pickup, hold, trip; and the reset that makes a transient dip harmless."""
    c = Canvas(1020, 312, t)
    x0, x1 = 96, 900
    thr = 118

    c.label(30, 60, "V", anchor="start", mono=True, size=13)
    c.path(f"M {x0} 178 L {x1 + 30} 178", arrow=True)
    c.path(f"M {x0} 40 L {x0} 178", arrow=False)
    c.path(f"M {x0} {thr} L {x1} {thr}", arrow=False, dash=True)
    c.label(x1 + 10, thr + 4, "threshold", anchor="start", size=13, muted=True, mono=True)

    # a dip that recovers in time, then one that does not
    c.path(f"M {x0} 78 L 210 78 L 224 150 L 316 150 L 330 78 L 520 78 "
           f"L 534 158 L {x1} 158", arrow=False)

    for x in (224, 330, 534, 700):
        c.path(f"M {x} 46 L {x} 276", arrow=False, dash=True)
    c.label(277, 36, "recovers before the delay expires", size=13, muted=True, italic=True)
    c.label(617, 36, "delay", size=13, muted=True, mono=True)

    c.path("M 224 196 L 330 196", arrow=False)
    c.path("M 224 190 L 224 202 M 330 190 L 330 202", arrow=False)
    c.path("M 534 196 L 700 196", arrow=False)
    c.path("M 534 190 L 534 202 M 700 190 L 700 202", arrow=False)
    c.label(277, 214, "timer resets", size=13, muted=True, italic=True)
    c.label(617, 214, "timer completes", size=13, muted=True, italic=True)

    c.label(6, 250, "output", anchor="start", mono=True, size=13)
    c.path(f"M {x0} 278 L {x1 + 30} 278", arrow=True)
    c.path(f"M {x0} 262 L 700 262 L 700 238 L {x1} 238", arrow=False)
    c.label(790, 230, "trip", size=13, muted=True, mono=True)
    c.label(x1 + 34, 292, "t", anchor="start", mono=True, size=13)
    return c


def inj_load(t):
    c = Canvas(880, 270, t)
    y, mid = 26, 53
    c.label(14, mid + 5, "V, f", anchor="start", mono=True, size=12)
    c.arrow(46, mid, 100, mid)
    c.box(100, y, 186, 54, ["Steady-state term", "(V/V0)^&#945;s &#183; (1 + DP&#183;&#916;&#969;)"], size=12)
    sx = 316
    c.arrow(286, mid, sx - 13, mid)
    c.summing(sx, mid, ("+", "&#8722;"))
    c.arrow(sx + 13, mid, sx + 44, mid)
    c.box(sx + 44, y, 168, 54, ["1 / sTr", "limits xPmin, xPmax"], accent=True, size=12)
    xp = sx + 236
    c.wire(xp, mid, "xP")
    c.arrow(sx + 212, mid, xp + 28, mid)
    c.box(xp + 28, y, 202, 54, ["P = P0 &#183; xP &#183; (V/V0)&#178;", "&#183; (1 + DP&#183;&#916;&#969;)"], size=12)
    c.arrow(xp + 230, mid, xp + 268, mid)
    c.label(xp + 276, mid + 5, "P", anchor="start", mono=True, size=12)

    # the recovery state is scaled by the transient exponent on its way back
    fy = 176
    c.box(340, fy - 25, 178, 50, ["&#215; (V/V0)^&#945;t"], size=12)
    c.path(f"M {xp} {mid} L {xp} {fy} L 518 {fy}", arrow=True)
    c.dot(xp, mid)
    c.path(f"M 340 {fy} L {sx} {fy} L {sx} {mid + 13}", arrow=True)
    c.path(f"M 70 {mid} L 70 236 L 429 236 L 429 {fy + 25}", arrow=True)
    c.dot(70, mid)
    c.label(440, 258, "Q follows the same structure, with exponents &#946;s, &#946;t and "
                      "its own limits.", size=11, muted=True, italic=True)
    return c


def inj_ibg(t):
    c = Canvas(1180, 320, t)
    y = 26
    c.label(14, y + 33, "&#916;f", anchor="start", mono=True, size=12)
    boxes, x = c.chain(48, y, [
        (166, ["Frequency response", "deadband fdbd"]),
        (162, ["Active power order", "P = Pext(1 + b&#183;sat)"]),
    ])
    c.arrow(x, y + 27, x + 40, y + 27)
    c.wire(x + 22, y + 27, "Ip")

    py = y + 110
    c.label(14, py + 33, "Vt", anchor="start", mono=True, size=12)
    boxes2, x2 = c.chain(48, py, [
        (166, ["LVRT / HVRT logic"]),
        (170, ["Reactive boost", "kRCI&#183;(Vref &#8722; Vt)"]),
    ])
    c.arrow(x2, py + 27, x2 + 40, py + 27)
    c.wire(x2 + 22, py + 27, "Iq")

    lx = max(x, x2) + 44
    c.box(lx, y + 34, 178, 66, ["Current limit Imax", "reactive priority in LVRT"], accent=True)
    c.path(f"M {x + 40} {y + 27} L {lx - 20} {y + 27} L {lx - 20} {y + 56} "
           f"L {lx} {y + 56}", arrow=True)
    c.path(f"M {x2 + 40} {py + 27} L {lx - 20} {py + 27} L {lx - 20} {y + 80} "
           f"L {lx} {y + 80}", arrow=True)
    c.arrow(lx + 178, y + 67, lx + 218, y + 67)
    c.box(lx + 222, y + 34, 174, 66, ["Park transform", "ix, iy from &#952;PLL"])
    c.arrow(lx + 396, y + 67, lx + 436, y + 67)
    c.label(lx + 444, y + 72, "ix, iy", anchor="start", mono=True, size=12)

    ry = y + 232
    c.label(14, ry + 20, "vq", anchor="start", mono=True, size=12)
    c.arrow(52, ry + 16, 130, ry + 16)
    c.box(134, ry - 6, 214, 44, ["PLL, second-order PI", "freeze below Vmin,pll"], size=11)
    c.path(f"M 348 {ry + 16} L {lx + 309} {ry + 16} L {lx + 309} {y + 100}", arrow=True)
    c.wire(lx + 250, ry + 16, "&#952;PLL", dy=-10)
    return c


def inj_pvg(t):
    c = Canvas(1220, 240, t)
    y1, m1 = 66, 93
    c.label(14, m1 + 5, "Pref", anchor="start", mono=True, size=12)
    _, x1 = c.chain(58, y1, [
        (150, ["Ip,cmd = Pref / Vt"]),
        (172, ["LVPL limit", "piecewise in Vt"]),
        (140, ["1 / (1 + sTg)"]),
    ])
    y2, m2 = 160, 187
    c.label(14, m2 + 5, "Qref, Vt", anchor="start", mono=True, size=12)
    _, x2 = c.chain(96, y2, [
        (176, ["Iq,cmd = fQV(Vt, Qref)"]),
        (140, ["1 / (1 + sTm)"]),
    ])
    c.wire(x1 + 24, m1, "Ip")
    c.wire(x2 + 24, m2, "Iq")

    lx = max(x1, x2) + 60
    c.box(lx, 107, 170, 66, ["Current limit", "Ip&#178; + Iq&#178; &#8804; Imax&#178;"], accent=True)
    c.path(f"M {x1} {m1} L {lx - 22} {m1} L {lx - 22} 127 L {lx} 127", arrow=True)
    c.path(f"M {x2} {m2} L {lx - 22} {m2} L {lx - 22} 155 L {lx} 155", arrow=True)
    c.arrow(lx + 170, 140, lx + 204, 140)
    c.box(lx + 204, 107, 166, 66, ["Park transform", "ix, iy"])
    c.arrow(lx + 370, 140, lx + 404, 140)
    c.label(lx + 412, 145, "ix, iy", anchor="start", mono=True, size=12)

    c.label(414, 24, "Vt", mono=True, size=12)
    c.arrow(414, 32, 414, y1)
    return c


def inj_bess(t):
    c = Canvas(1180, 250, t)
    y, mid = 26, 53
    c.label(14, mid + 5, "Pref, Vref", anchor="start", mono=True, size=12)
    _, x = c.chain(104, y, [
        (156, ["Plant controller", "REPC_A"]),
        (188, ["Converter electrical", "REEC_C, Ip and Iq vs V"]),
        (166, ["Generator interface", "REGC_A"], "accent"),
    ])
    c.arrow(x, mid, x + 44, mid)
    c.label(x + 52, mid + 5, "ix, iy", anchor="start", mono=True, size=12)

    c.box(316, 140, 214, 58, ["State of charge", "clamps set Pmax, Pmin"], size=12)
    c.path(f"M 423 140 L 423 {y + 54}", arrow=True)
    c.path(f"M {x + 22} {mid} L {x + 22} 169 L 530 169", arrow=True)
    c.dot(x + 22, mid)
    c.wire(640, 169, "Pbess", dy=-9)
    c.label(430, 228, "A depleted or full battery has its dispatch limit driven to zero.",
            size=11, muted=True, italic=True)
    return c


def inj_svc_generic1(t):
    c = Canvas(1280, 330, t)
    y, mid = 26, 53
    sx = 600
    c.label(14, mid + 5, "V", anchor="start", mono=True, size=12)
    c.arrow(40, mid, sx - 13, mid)
    c.summing(sx, mid, ("&#8722;", "+"))
    c.label(sx - 44, mid - 34, "Vref", size=11, muted=True, mono=True)
    c.arrow(sx, mid - 40, sx, mid - 13)
    c.label(sx + 18, mid - 20, "+", size=13)
    _, x = c.chain(sx + 13, y, [
        (162, ["PI regulator Kp, Ki", "with droop Bp"]),
        (156, ["Susceptance limits", "Bmin, Bmax"], "accent"),
    ])
    c.arrow(x, mid, x + 40, mid)
    c.wire(x + 22, mid, "Bsvc")
    c.box(x + 44, y, 164, 54, ["Reactive current", "iy = Bsvc &#183; V"])
    c.arrow(x + 208, mid, x + 246, mid)
    c.label(x + 254, mid + 5, "Q", anchor="start", mono=True, size=12)

    # two parallel stabiliser channels, summed and limited together
    a, b = 148, 232
    c.label(14, a + 29, "Input 1", anchor="start", mono=True, size=12)
    c.arrow(78, a + 24, 124, a + 24)
    c.box(124, a, 214, 48, ["Channel 1: G1, T1, a, K1, &#177;L1"], size=12)
    c.label(14, b + 29, "Input 2", anchor="start", mono=True, size=12)
    c.arrow(78, b + 24, 124, b + 24)
    c.box(124, b, 214, 48, ["Channel 2: G2, T2, b, K2, &#177;L2"], size=12)

    jx, jy = 386, 190
    c.path(f"M 338 {a + 24} L {jx} {a + 24} L {jx} {jy - 13}", arrow=True)
    c.path(f"M 338 {b + 24} L {jx} {b + 24} L {jx} {jy + 13}", arrow=True)
    c.summing(jx, jy, ("", ""))
    c.arrow(jx + 13, jy, jx + 44, jy)
    c.box(jx + 44, jy - 24, 130, 48, ["&#177;Ltot"], accent=True, size=12)
    c.wire(jx + 194, jy, "dvpss", dy=-12)
    c.path(f"M {jx + 174} {jy} L {sx} {jy} L {sx} {mid + 13}", arrow=True)
    c.label(820, 226, "The stabiliser output shifts the voltage reference; Vref itself is "
                      "set from", size=11, muted=True, italic=True)
    c.label(820, 244, "the power flow, so the model starts in equilibrium.",
            size=11, muted=True, italic=True)
    return c


DIAGRAMS = {
    # models/ieee-governors.mdx
    "tor-entsoe-simp": tor_entsoe_simp,
    "tor-tgov1": tor_tgov1,
    "tor-gast": tor_gast,
    "tor-degov1": tor_degov1,
    "tor-hygov": tor_hygov,
    # models/custom-governors.mdx
    "tor-1storder": tor_1storder,
    "tor-hydro-generic1": tor_hydro_generic1,
    "tor-hydro-dg": tor_hydro_dg,
    # models/custom-exciters.mdx
    "exc-1storder": exc_1storder,
    "exc-kundur": exc_kundur,
    # models/ieee-exciters.md
    "exc-ac1a": exc_ac1a,
    "exc-ac4a": exc_ac4a,
    "exc-ac8b": exc_ac8b,
    "exc-dc3a": exc_dc3a,
    "exc-ieeet5": exc_ieeet5,
    "exc-st1a": exc_st1a,
    "exc-st2a": exc_st2a,
    "exc-sexs": exc_sexs,
    "exc-entsoe-simp": exc_entsoe_simp,
    "pss-pss2b": pss_pss2b,
    "pss-pss3b": pss_pss3b,
    "pss-pss4b": pss_pss4b,
    "pss-ieeest": pss_ieeest,
    "pss-stab3": pss_stab3,
    "exc-maxex2": exc_maxex2,
    "exc-integral-oel": exc_integral_oel,
    # models/custom-exciters.mdx, continued
    "exc-generic1": exc_generic1,
    "exc-avr-dg": exc_avr_dg,
    "exc-generic2": exc_generic2,
    "exc-generic": exc_generic,
    # models/custom-governors.mdx
    "tor-thermal-generic1": tor_thermal_generic1,
    # models/custom-injectors.md, wind
    "inj-wt3": inj_wt3,
    "inj-wt4": inj_wt4,
    # models/custom-injectors.md, converters
    "inj-gfol-pll": gfol_pll,
    "inj-gfol-currentctl": gfol_currentctl,
    "inj-gfol-pctl": gfol_pctl,
    "inj-gfol-qctl": gfol_qctl,
    "inj-gfor-vsm": gfor_vsm,
    "inj-gfor-currentlim": gfor_currentlim,
    # models/discrete-controllers.md
    "dctl-ltc-timing": dctl_ltc_timing,
    "dctl-relay-timing": dctl_relay_timing,
    # models/custom-injectors.md
    "inj-load": inj_load,
    "inj-ibg": inj_ibg,
    "inj-pvg": inj_pvg,
    "inj-bess": inj_bess,
    "inj-svc-generic1": inj_svc_generic1,
    # models/two-port-models.mdx
    "twop-hvdc-lcc-control": hvdc_lcc,
    "twop-hvdc-vsc-control": hvdc_vsc,
    "twop-hvdc-vsc-sc-control": hvdc_vsc_sc,
    "twop-dcl-vsc-topology": dcl_vsc,
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, build in DIAGRAMS.items():
        for theme, palette in THEMES.items():
            path = OUT / f"{name}-{theme}.svg"
            path.write_text(build(palette).render())
            print(f"  {path.relative_to(OUT.parent.parent.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
