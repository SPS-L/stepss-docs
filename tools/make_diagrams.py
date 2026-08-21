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

    # -- primitives ---------------------------------------------------------
    def box(self, x, y, w, h, lines, accent=False, size=13):
        t = self.t
        fill = t["accent_box"] if accent else t["box"]
        edge = t["accent_edge"] if accent else t["edge"]
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
        style = ' font-style="italic"' if italic else ""
        self.parts.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" '
            f'font-size="{size}" fill="{fill}"{style}>{text}</text>'
        )

    def path(self, d, arrow=True, dash=False):
        t = self.t
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

    def summing(self, x, y, signs=("+", "+"), r=13):
        """A summing junction. `signs` are placed left and below."""
        t = self.t
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
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'width="{self.w}" height="{self.h}" role="img">\n'
            f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M 0 1 L 10 5 L 0 9 z" fill="{t["line"]}"/></marker></defs>\n'
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
