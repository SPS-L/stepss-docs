#!/usr/bin/env python3
"""Geometry checks for the generated model diagrams.

Three defects got through review by eye and are cheap to catch mechanically:

  * a wire routed straight through the boxes it was meant to feed, which is
    what the DEGOV1 return line did across all three of its blocks;
  * a label a wire runs through, which struck out DEGOV1's reference input
    and one of the IBG current names;
  * two boxes overlapping.

None of these raises an error at render time: an SVG draws exactly what it is
told to. Run this after touching make_diagrams.py.

    ./tools/check_diagrams.py     # exits non-zero on any finding
"""

from __future__ import annotations

import importlib.util
import pathlib
import re
import sys

HERE = pathlib.Path(__file__).resolve().parent
MARGIN = 5.0        # a wire may meet an edge; it may not run this far inside


def _load():
    spec = importlib.util.spec_from_file_location("md", HERE / "make_diagrams.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    md = _load()
    boxes: list = []
    segs: list = []
    labels: list = []
    _box, _path, _label = md.Canvas.box, md.Canvas.path, md.Canvas.label

    def box(self, x, y, w, h, lines, accent=False, size=13):
        text = lines if isinstance(lines, str) else " / ".join(lines)
        boxes.append((x, y, x + w, y + h, text))
        return _box(self, x, y, w, h, lines, accent, size)

    def path(self, d, arrow=True, dash=False):
        pts = [(float(a), float(b)) for a, b in re.findall(r"(-?[\d.]+)\s+(-?[\d.]+)", d)]
        segs.extend(zip(pts, pts[1:]))
        return _path(self, d, arrow, dash)

    def label(self, x, y, text, anchor="middle", size=13, mono=False,
              muted=False, italic=False):
        plain = re.sub(r"&#\d+;", "x", str(text))
        w = len(plain) * size * (0.62 if mono else 0.56)
        x1 = x if anchor == "start" else x - w if anchor == "end" else x - w / 2
        labels.append((x1, y - size * 0.78, x1 + w, y + size * 0.24, plain))
        return _label(self, x, y, text, anchor, size, mono, muted, italic)

    md.Canvas.box, md.Canvas.path, md.Canvas.label = box, path, label

    findings = 0
    for stem, fn in md.DIAGRAMS.items():
        boxes.clear()
        segs.clear()
        labels.clear()
        fn(md.THEMES["light"])

        for (x1, y1), (x2, y2) in segs:
            lox, hix = sorted((x1, x2))
            loy, hiy = sorted((y1, y2))
            for bx1, by1, bx2, by2, name in boxes:
                ox = min(hix, bx2 - MARGIN) - max(lox, bx1 + MARGIN)
                oy = min(hiy, by2 - MARGIN) - max(loy, by1 + MARGIN)
                if ox > 0 and oy > 0:
                    print(f"{stem}: wire ({x1:.0f},{y1:.0f})-({x2:.0f},{y2:.0f}) "
                          f"runs through box [{name[:44]}]")
                    findings += 1

        for lx1, ly1, lx2, ly2, txt in labels:
            for (x1, y1), (x2, y2) in segs:
                if abs(y1 - y2) < 0.5 and ly1 + 2 < y1 < ly2 - 2:
                    lo, hi = sorted((x1, x2))
                    if min(hi, lx2 - 3) - max(lo, lx1 + 3) > 0:
                        print(f"{stem}: wire y={y1:.0f} strikes label {txt[:34]!r}")
                        findings += 1
                if abs(x1 - x2) < 0.5 and lx1 + 2 < x1 < lx2 - 2:
                    lo, hi = sorted((y1, y2))
                    if min(hi, ly2 - 2) - max(lo, ly1 + 2) > 0:
                        print(f"{stem}: wire x={x1:.0f} strikes label {txt[:34]!r}")
                        findings += 1

        for i, (ax1, ay1, ax2, ay2, an) in enumerate(boxes):
            for bx1, by1, bx2, by2, bn in boxes[i + 1:]:
                if (min(ax2, bx2) - max(ax1, bx1) > 0
                        and min(ay2, by2) - max(ay1, by1) > 0):
                    print(f"{stem}: boxes overlap, [{an[:26]}] and [{bn[:26]}]")
                    findings += 1

    print(f"{len(md.DIAGRAMS)} diagrams checked, {findings} findings")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
