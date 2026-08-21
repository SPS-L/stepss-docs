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


DIAGRAMS = {
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
