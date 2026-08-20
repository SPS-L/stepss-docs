# Screenshot harness

Regenerates every figure under `public/images/screenshots/`. There are three
capture paths because there are three things to photograph, and one shared
library.

| Script | Produces | Drives |
|---|---|---|
| `capture-gui.sh light` / `dark` | the 22 `gui-*` pairs | STEPSS GUI, through xdotool on an Xvfb display |
| `capture-cgstudio.py` | the 6 `cg-studio-*` figures | CODEGEN Studio, through Playwright |
| `capture-python.py` | the 5 `py-*` pairs | the `stepss` package, through matplotlib |
| `shotlib.sh` | shell helpers | shared by the first two |
| `launch.sh` | one seeded STEPSS session | called by `capture-gui.sh` |

## Why this exists

The set before this one shipped five figures as a solid black rectangle:
`gui-analysis-light`, `gui-codegen-light`, `gui-dynamic-simulation-light`,
`gui-system-data-light` and `cg-studio-settings`. Nothing was wrong with the
applications. The captures were grabbed window by window off an Xvfb display
running **without backing store and without a window manager**, so a window
that was momentarily obscured came back from the X server as whatever was in
front of it, which on an empty root is black.

Four rules here exist only to stop that happening again, and none of them is
optional:

- **Xvfb runs with `+bs`.** Without backing store, X does not keep the pixels
  of an obscured window and has nothing truthful to return.
- **openbox runs.** With no window manager nothing owns the stacking order, so
  "raise this window" is not a request anyone honours.
- **Every figure is cropped out of a full root capture**, after raising the
  target and waiting for the repaint, rather than read back from the window's
  own buffer. A stale or clipped buffer then cannot reach a file.
- **`check_black` rejects a shot that is more than 12% black.** This is the
  one that would have caught the last set. A capture harness with no assertion
  about its output is a harness that fails silently.

That last check belongs to the X11 path and to it alone. Run it against a
CODEGEN Studio figure and it reports about 80% black, because that application
paints its own background `#0f1117`, which is below the threshold: the figure
is correct and the detector is measuring the app's design. `capture-cgstudio.py`
therefore does not call it. Before "fixing" a CG Studio figure that a
brightness check complains about, open it.

## Prerequisites

- `Xvfb`, `openbox`, `xdotool`, `xprop`, `xwininfo`, ImageMagick (`import`,
  `convert`, `identify`), Python with Pillow.
- STEPSS GUI installed, so `/opt/stepss/lib/app/stepss.jar` and the JDK on
  `PATH` can be used. `launch.sh` runs the jar directly rather than
  `/usr/bin/stepss`, because it needs to point the JVM at a **private
  preferences root**.
- The `stepss` Python package, for `capture-python.py`.
- Playwright with its Chromium, for `capture-cgstudio.py`, and the CG Studio
  server running on `127.0.0.1:8765`:

  ```sh
  cd ../../stepss-cg-studio && PYTHONPATH=src python3 -m cg_studio --no-browser
  ```

  It loads Drawflow from a CDN, so that capture needs the network.

- The bundled examples unpacked into `~/stepss-examples`. `capture-gui.sh`
  opens the Kundur case itself; `capture-python.py` also needs `five-bus`, and
  says so if it is missing.

## Running it

```sh
export SHOT_WORK=${TMPDIR:-/tmp}/stepss-shots     # optional, this is the default
./capture-gui.sh light
./capture-gui.sh dark
python3 capture-cgstudio.py
python3 capture-python.py
```

Then copy them in, light and dark becoming the filename suffix the pages
expect:

```sh
cd "$SHOT_WORK/shots"
for t in light dark; do
    for f in $t/*.png; do
        cp "$f" "../../public/images/screenshots/$(basename "$f" .png)-$t.png"
    done
done
cp cgstudio/*.png python/*.png ../../public/images/screenshots/
```

## Things worth knowing before editing these

- **The GUI window is pinned to 1600x760 by seeded preferences, and every
  coordinate in `capture-gui.sh` is a fixed point inside it.** Seeding is not a
  convenience: `windowMaximised` defaults to true, an unseeded launch fills the
  screen, and openbox then refuses the resize. The preferences root is private
  (`-Djava.util.prefs.userRoot`) so a capture run never touches the operator's
  own theme, geometry or working directory, and so `stepssFirstTime` can be
  left out to make the licence dialog appear on demand.
- **Panels the application lays out itself move when the window resizes.** The
  observable picker is shot at 1600x830 for that reason, and the second `Add`
  in the curve picker is at a different y than the first because the Selected
  list grew under it. If a click starts landing on the wrong control, re-probe
  rather than nudging the number.
- **A few values are wall clock and differ between the light and dark runs of
  the same case**: the elapsed time in the status bar and the Dynamic
  Simulation pane, the timestamp in the one-line diagram title, and the
  `RT RT` panel of the Python monitor figure. Do not write those numbers into
  alt text; a pair has one alt text and it must be true of both. Everything
  else here is reproducible, and the eight non-monitor `py-*` figures come out
  byte-identical run to run.
- **CG Studio is dark-only** (SPS-L/stepss-cg-studio#1), so its figures are
  single and carry `class="shot-single"`. Every other figure on the site is a
  light/dark pair using Starlight's `light:sl-hidden` and `dark:sl-hidden`.
- **The hero collage is not made here.** It is a composed figure of four real
  results rather than a screenshot of a tool.
