# STEPSS Site Review Response Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the gaps the August 2026 site review found, chiefly by giving STEPSS GUI the documentation section it has never had, illustrated with real screenshots of the running application.

**Architecture:** A new three-page `STEPSS GUI` sidebar section sits between Getting Started and Simulation Guide, documenting how to drive the application without restating any reference material the Simulation Guide already owns. Screenshots are captured reproducibly by writing the application's own Java preferences node before launch, so light and dark pairs align pixel for pixel and swap with Starlight's built-in theme utility classes. Six smaller edits fix the homepage pitch, the two off-site dead ends in Quick Start, the author credit, version discoverability and the commercial-licence path.

**Tech Stack:** Astro 7, Starlight 0.41, MDX, Node 22. Screenshot capture with `xdotool` and ImageMagick `import` under XWayland. No test framework exists in this repo; `npm run build` is the only validation step.

**Spec:** `docs/superpowers/specs/2026-08-17-site-review-response-design.md`

## Global Constraints

- **No em-dashes** (U+2014) anywhere in the repo. En-dashes (U+2013) are fine in numeric ranges (`g1–g20`) and compound names (Newton–Raphson, lead–lag). Verify with the grep in the validation step of every task.
- **`npm run build` must pass** after every task. It is the only validation step and it catches dead links, bad frontmatter, MDX syntax errors and missing imports.
- **New pages must be registered** in the `sidebar` array in `astro.config.mjs`, or they do not appear in navigation.
- **Sidebar stays two levels deep at most.** No group may hold a single page.
- **One owner per topic.** No new page may restate record syntax, model parameters, or the GUI-versus-Python edition comparison. Those are owned by `user-guide/dynamic-models.md`, the family pages under `models/`, and `getting-started/overview.md:33-58` respectively.
- **Never reintroduce:** the retired MATLAB eigenanalysis tool, PFC as a live alternative, or the retired PyRAMSES distribution name.
- **Factual claims about the GUI are checked against `stepss-java-ui` source**, in the same way model pages are checked against `stepss-ramses`. Citations for every fact used in this plan are given inline in the task that needs them.
- **Bare curly braces in `.mdx` must be escaped** (`{'{'}`) or the build fails.
- **Images** live in `public/images/` and are referenced by absolute path (`/images/...`).
- **Work on a branch.** The repo is currently on `main`; see Task 0.
- **Commit only when the project owner asks.** Each task below ends with a commit step. Prepare the commit, then confirm before running it.

---

### Task 0: Branch and baseline

**Files:**
- Modify: none

- [ ] **Step 1: Confirm the working tree is clean**

Run: `cd /home/apetros/Code/stepss/stepss-docs`, then `git status --short`
Expected: no output, apart from the untracked `docs/superpowers/` spec and plan.

- [ ] **Step 2: Create the working branch**

Run: `git checkout -b site-review-response`
Expected: `Switched to a new branch 'site-review-response'`

- [ ] **Step 3: Establish the build baseline**

Run: `npm run build`
Expected: PASS. Record the page count it reports, so a later drop is noticed.

- [ ] **Step 4: Establish the em-dash baseline**

Run: `grep -rnP '\x{2014}' src CLAUDE.md README.md astro.config.mjs`
Expected: no output, exit status 1.

---

### Task 1: Screenshot capture harness

**Files:**
- Create: `$TMPDIR/shots/capture.sh` (throwaway, not committed)
- Create: `public/images/screenshots/` (directory)

**Interfaces:**
- Produces: twelve PNG files in `public/images/screenshots/`, named `gui-<shot>-light.png` and `gui-<shot>-dark.png` for each of the six shots listed in Step 5. Tasks 2, 3, 4 and 6 reference these exact filenames.

**Background the implementer needs:**

The application persists its window geometry and theme in the Java preferences node `my.stepss.StepssUI`. Writing those keys before launch makes every capture identically framed, which is what lets the light and dark images swap without the page reflowing. The relevant keys, from `stepss-java-ui/src/my/stepss/StepssUI.java:6458-6466`:

| Key | Purpose |
|---|---|
| `windowMaximised` | `false` is required, or the geometry keys are ignored |
| `windowX`, `windowY`, `windowWidth`, `windowHeight` | Frame bounds |
| `darkTheme` | `true` for the dark pass |
| `workingDirectory` | Where the file choosers open |

`rememberSession()` (`StepssUI.java:598`) writes these on exit; `startMaximised()` (`:661`) reads `windowMaximised`, defaulting to `true`, which is why a first run is maximised and unusable for capture.

**Two environment traps, both already hit:**

1. The sandbox mounts `/tmp` read-only, and Java's ImageIO writes its cache there. Without an override the application starts with every image missing and logs `Can't create cache file!`. Export `_JAVA_OPTIONS="-Djava.io.tmpdir=$TMPDIR/jtmp"` before launching.
2. This machine's `xdotool` predates `windowstate`, so a maximised window cannot be un-maximised from the command line. That is why the geometry goes through preferences rather than `xdotool windowsize`.

- [x] **Step 1: Find the preferences node, and back it up**

**Corrected during execution.** The node is **not** at the nested
`~/.java/.userPrefs/my/stepss/StepssUI/` path this step originally checked.
`preferences()` (`StepssUI.java:6506-6520`) resolves it through
`PreferenceMigration.node(root, LEGACY_NODE, PREFERENCES_NODE)` off
`Preferences.userRoot()`, and the node name contains dots and capitals, so Java
stores it as a **single flat alt-Base64-encoded directory** at the `.userPrefs`
root rather than a directory per package component. Looking for `my/stepss/`
finds nothing and wrongly concludes there are no settings to protect.

Enumerate and identify it by content instead:

```sh
cd ~/.java/.userPrefs && for d in _*; do echo "=== $d"; cat "$d/prefs.xml"; done
```

The STEPSS node is the one carrying `stepssFirstTime` and `windowMaximised`.

On this machine it **did** exist, holding real settings
(`examplesDirectory=/home/apetros/Code`, `showExamplesAtStartup=true`,
`stepssFirstTime=false`, `windowMaximised=true`,
`workingDirectory=/home/apetros/Code/kundur-two-area`), dated the day before the
run. Back it up before writing anything, and take the restore branch in Step 8:

```sh
mkdir -p "$TMPDIR/prefs-backup"
cd ~/.java/.userPrefs
for d in _*; do
  k=$(echo "$d" | md5sum | cut -c1-8)
  cp "$d/prefs.xml" "$TMPDIR/prefs-backup/$k.xml"
  echo "$d" > "$TMPDIR/prefs-backup/$k.dirname"
done
```

**Two sandbox notes.** Writing `~/.java` and launching the GUI both need the
sandbox off: in-sandbox, `~/.java` is read-only, and the example install into
`examplesDirectory` fails silently, leaving no directory and no error.

- [ ] **Step 2: Write the capture script**

```bash
#!/usr/bin/env bash
# Throwaway capture harness. Not committed.
set -euo pipefail

PREFS_DIR="$HOME/.java/.userPrefs/my/stepss/StepssUI"
OUT="/home/apetros/Code/stepss/stepss-docs/public/images/screenshots"
export _JAVA_OPTIONS="-Djava.io.tmpdir=$TMPDIR/jtmp"
mkdir -p "$TMPDIR/jtmp" "$OUT" "$PREFS_DIR"

# $1 = "true" for the dark pass, "false" for light
write_prefs() {
  cat > "$PREFS_DIR/prefs.xml" <<XML
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE map SYSTEM "http://java.sun.com/dtd/preferences.dtd">
<map MAP_XML_VERSION="1.0">
  <entry key="windowMaximised" value="false"/>
  <entry key="windowX" value="80"/>
  <entry key="windowY" value="60"/>
  <entry key="windowWidth" value="1760"/>
  <entry key="windowHeight" value="1100"/>
  <entry key="darkTheme" value="$1"/>
  <entry key="stepssFirstTime" value="false"/>
</map>
XML
}

# $1 = window id, $2 = output basename
shoot() {
  import -window "$1" "$OUT/$2.png"
  echo "captured $2 -> $(identify -format '%wx%h' "$OUT/$2.png")"
}

find_window() {  # $1 = title substring
  for _ in $(seq 1 20); do
    for w in $(xdotool search --name "$1" 2>/dev/null); do
      echo "$w"; return 0
    done
    read -t 1 </dev/null 2>/dev/null || true
  done
  echo "window '$1' never appeared" >&2; return 1
}
```

- [ ] **Step 3: Verify the light pass frames correctly**

Run the script's light pass, launch `stepss`, and capture the Open Examples dialog.
Expected: a PNG whose geometry is the dialog's own size, not `3006x1696`. A `3006x1696` result means the geometry preference was ignored; re-check `windowMaximised=false`.

- [ ] **Step 4: Load the Kundur example**

In the Open Examples dialog, select **Kundur two-area** and click **Open example**. Per `stepss-java-ui/src/my/stepss/examples/ExampleInstaller.java:16-30`, this unpacks the case into the user's examples directory and fills the file slots from generated configuration, so the case is runnable immediately.

Expected: the dialog closes and the window title becomes `STEPSS - kundur-two-area`.

- [x] **Step 5: Capture the seven light shots**

**Inventory revised during execution**, to seven rather than six:

| Basename | Size | What it shows |
|---|---|---|
| `gui-open-examples` | 760x620 | The Open Examples dialog, branding and all three cases |
| `gui-system-data` | 1600x760 | System Data tab with the Kundur files loaded |
| `gui-observables` | 1600x760 | Observables tab, runtime observables set for live plotting |
| `gui-initialization` | 1600x760 | Initialization tab after the power flow, with the Helios output and power balance |
| `gui-dynamic-simulation` | 1600x760 | Dynamic Simulation tab with the solver report |
| `gui-select-observables` | 520x560 | The curve picker, two machines queued |
| `gui-plot` | 1000x600 | The extracted curves: the inter-area oscillation |

Three changes from the original six, all forced by what the application actually does:

- **`gui-analysis` dropped.** The Analysis tab is a bare row of buttons with no
  content of its own; an empty panel is not worth a figure. Its two halves
  (time-domain extraction, and the in-engine small-signal analysis) are described
  in prose on `gui/interface`, and the extraction path is shown by
  `gui-select-observables` instead.
- **`gui-observables` and `gui-select-observables` added.** The first carries the
  live-plotting feature, which is the review's "live plot during a run" ask and is
  otherwise invisible. The second is a step the walkthrough cannot skip.
- **`gui-dyngraph` became `gui-plot`, and is a rendered figure rather than a
  window screenshot.** See Step 5a.

The window is **1600x760**, not the 1760x1100 first configured: at 1100 the
System Data tab was 40% empty. Set the geometry through preferences for the first
launch, then `xdotool windowsize` works for the rest, because the window is no
longer maximised.

The Kundur disturbance steps load L9 by +0.5 pu at t = 1 s over a 60 s horizon (`examples.properties`, `kundur.summary`), which is confirmed by `disturb.dst` itself: `1.000 CHGPRM INJ L9 Po +0.5 0` and `60.000 STOP`. Run the power flow before capturing `gui-initialization`, and the simulation before `gui-dynamic-simulation`, so both panels carry real output rather than being blank.

- [x] **Step 5a: Render the curve figure, because no plot window is capturable here**

The GUI plots through gnuplot, and **all three of gnuplot's interactive terminals
fail in this Wayland session**: `qt` opens a 10x10 stub and logs
`QObject::startTimer: Timers can only be used with threads started with QThread`,
while `x11` and `wxt` exit silently with no window. Do not keep trying them.

Instead render the figure from the artefacts the GUI itself produced. Clicking
**Plot** writes `tempGnupOut.cur` (the extracted columns) and `tempGnupOut.plt`
(the gnuplot script) into the working directory. Re-render that data with the
`pngcairo` terminal.

This is a better outcome than a window screenshot, not a worse one: a gnuplot
window is white in both themes, whereas `pngcairo` gives a genuine **dark
variant**. Colours come from the validated categorical palette, slots 1 and 2,
and both modes pass all six checks of the data-viz validator (worst CVD ΔE 24.7
light, 26.8 dark, against a target of 8):

| Role | Light | Dark |
|---|---|---|
| Surface | `#fcfcfb` | `#1a1a19` |
| Text, primary / secondary | `#0b0b0b` / `#52514e` | `#ffffff` / `#c3c2b7` |
| G1 (series 1) | `#2a78d6` | `#3987e5` |
| G3 (series 2) | `#eb6834` | `#d95926` |

Plot `rotor`-adjacent quantities on **one axis only**: G1 and G3 active power are
both MW, so a single y-axis is correct and a second would be the commonest chart
error. Window the x-axis to 0 to 12.6 s: the mode is a ~0.7 Hz anti-phase swing
that damps out by about 6 s, and the full 60 s horizon compresses it to nothing.
Carry direct labels adjacent to each curve as well as the legend, so identity is
never colour-alone, and keep label text in ink colours rather than the series
colour.

- [x] **Step 6: Repeat for dark, using the live toggle**

**Corrected during execution.** Do **not** edit `darkTheme` in the XML and
restart. Java Preferences caches the node in memory, so the exiting process
flushes its cached value straight over the edit.

Use the application's own **Tools, Dark theme** toggle instead
(`addThemeToggle()`, `StepssUI.java:743`). It calls `installTheme` plus
`FlatLaf.updateUI()`, so it re-themes **live**, which means the loaded case, the
completed power flow and the finished simulation output are all preserved and the
whole run does not have to be repeated. Only the two dialogs need reopening.

Every dark capture must be the same pixel dimensions as its light twin. Check:

Run: `cd public/images/screenshots && for f in *-light.png; do d="${f%-light.png}-dark.png"; echo "$f $(identify -format '%wx%h' "$f") vs $(identify -format '%wx%h' "$d")"; done`
Expected: each pair reports identical dimensions.

- [ ] **Step 7: Check the file sizes are reasonable**

Run: `du -sh public/images/screenshots/; ls -la public/images/screenshots/`
Expected: no single PNG over about 500 KB. If any is larger, run it through `convert <f> -strip -quality 90 <f>` and re-check.

- [x] **Step 8: Restore the preferences file**

The restore branch applies, because Step 1 found real settings. Close the
application **gracefully first** and only then restore, or the exiting process
writes its own session state over the restored file.

Graceful close is the title-bar close button, which raises an **Exit
Confirmation** ("Are you sure you want to exit? All simulation data will be
lost!") offering Yes, Yes (clear all open windows), and Cancel. Take **Yes (clear
all open windows)**, which also disposes any lingering gnuplot instance. Note that
`Ctrl+Q` and the File, Exit item both failed to close it by synthetic click in
this session; the title-bar button worked.

```sh
NODE_DIR="$HOME/.java/.userPrefs/$(cat "$TMPDIR/prefs-backup/de79af73.dirname")"
cp "$TMPDIR/prefs-backup/de79af73.xml" "$NODE_DIR/prefs.xml"
cat "$NODE_DIR/prefs.xml"
```

Expected: byte-for-byte the Step 1 contents, with **no `darkTheme` key** and
`windowMaximised` back to `true`.

- [x] **Step 8a: Remove the stray `.claude` directory from `public/`**

Creating `public/images/screenshots/` also created
`public/images/screenshots/.claude/.cc-writes` as harness bookkeeping. It is
empty and `.gitignore:25` ignores it, so it cannot be committed, but **`public/`
is copied verbatim into `dist/`**, so anything left there is published. Remove it:

```sh
rm -rf public/images/screenshots/.claude
ls -a public/images/screenshots/
```

- [x] **Step 9: Commit**

```bash
git add public/images/screenshots
git commit -m "Add STEPSS GUI screenshots, light and dark"
```

---

### Task 2: The STEPSS GUI section, and its First Run page

**Files:**
- Create: `src/content/docs/gui/first-run.mdx`
- Modify: `astro.config.mjs:61-155` (the `sidebar` array)

**Interfaces:**
- Consumes: `gui-open-examples-{light,dark}.png` from Task 1.
- Produces: the slugs `gui/first-run`, `gui/interface` and `gui/running`. Tasks 3, 4, 6 and 8 link to these.

**Sourced facts.** Every claim below traces to `stepss-java-ui`:

| Fact | Source |
|---|---|
| A first run must accept the licence before anything else, and it is **RAMSES's** licence rather than the interface's | `LicenseDialog.java:26-38` |
| The licence terms are deliberately not summarised in the dialog; `getting-started/license.md` owns the bus and core caps | `LicenseDialog.java:34-38` |
| Open Examples is reached from **File, Open Examples** | `examples/examples.properties:1-2` |
| The three bundled cases and their scale | `examples.properties`, `.name` and `.scale` keys |
| Opening an example copies it into the examples directory and fills the case | `ExampleInstaller.java:16-30` |
| The examples directory is separate from the working directory, so a second example lands beside the first rather than inside it | `StepssUI.java:6468-6475` |
| The dark theme toggle is at the end of the **Tools** menu | `StepssUI.java:735-744` |

- [ ] **Step 1: Register the section in the sidebar**

Insert this group into `astro.config.mjs` immediately after the `Getting Started` group and before `Simulation Guide`:

```js
		{
			// The GUI is the edition an installer delivers, and the first thing
			// a new reader opens. It sits before the Simulation Guide because
			// nobody should have to read File Formats to press Run.
			label: 'STEPSS GUI',
			items: [
				{ label: 'First Run',            slug: 'gui/first-run' },
				{ label: 'The Interface',        slug: 'gui/interface' },
				{ label: 'Running a Simulation', slug: 'gui/running' },
			],
		},
```

- [ ] **Step 2: Verify the build fails**

Run: `npm run build`
Expected: FAIL, because the three slugs have no pages yet. This confirms the sidebar entry is live rather than silently ignored.

- [ ] **Step 3: Write the First Run page**

Create `src/content/docs/gui/first-run.mdx` with this frontmatter and structure:

```mdx
---
title: First Run
description: What happens the first time you open STEPSS GUI, and the fastest way to a working case
---

import { Steps, Card, CardGrid } from '@astrojs/starlight/components';
```

Sections, in order:

1. **Accepting the licence.** The first launch shows the RAMSES licence and will not continue until it is accepted. Say plainly that this is the engine's licence, not the interface's, and link to `/getting-started/license/` for the terms, the 1000-bus and 2-core caps and the per-component breakdown. Do **not** restate the caps here; `LicenseDialog.java:34-38` records that duplicating them is the mistake to avoid.
2. **Start from a bundled example.** The recommended path. Use `<Steps>`: File, then Open Examples, then pick a case, then Open example. State that this copies the case into your examples directory and fills in every file slot, so **Run** works immediately.
3. **The three bundled cases.** A `<CardGrid>` or table, with the scale and one-line purpose of each, taken verbatim in substance from `examples.properties`:
   - **5-bus tutorial**, 5 buses, 1 machine. The teaching case from EEN452 at the Cyprus University of Technology, and the right one to open first: small enough to read end to end.
   - **Kundur two-area**, 11 buses, 4 machines, 60 Hz. The standard inter-area oscillation benchmark. Ships `dyn_noPSS.dat` beside `dyn.dat` so the same run can be repeated with the stabiliser out and the damping compared.
   - **IEEE Nordic**, 74 buses, 20 machines, 400/220/130 kV. The long-term voltage stability reference from IEEE PES technical report PES-TR19, opening on operating point A with a branch tripped.
   Link each to its Test Systems page under `/test-systems/`, not to its GitHub repo, since that section owns the per-system detail.
4. **The screenshot**, placed in section 2, using the pair from Task 1:

```html
<img src="/images/screenshots/gui-open-examples-light.png"
     alt="The Open Examples dialog listing Kundur two-area, IEEE Nordic and the 5-bus tutorial, with the Kundur description shown"
     class="dark:sl-hidden" />
<img src="/images/screenshots/gui-open-examples-dark.png"
     alt="The Open Examples dialog listing Kundur two-area, IEEE Nordic and the 5-bus tutorial, with the Kundur description shown"
     class="light:sl-hidden" />
```

5. **Where files land.** The examples directory is remembered separately from the working directory, so opening a second example puts it beside the first rather than inside it.
6. **Setting the theme.** Tools, then Dark theme. The choice is remembered between sessions.
7. **Next steps.** Link to `/gui/interface/` and `/gui/running/`.

**Boundary check before writing:** this page must not describe record syntax, model parameters, or the difference between the two editions. Link out for all three.

- [ ] **Step 4: Verify the build still fails, for the right reason**

Run: `npm run build`
Expected: FAIL, now naming only `gui/interface` and `gui/running` as missing. `gui/first-run` must no longer appear in the error.

- [ ] **Step 5: Commit**

```bash
git add astro.config.mjs src/content/docs/gui/first-run.mdx
git commit -m "Add the STEPSS GUI section, starting with First Run"
```

---

### Task 3: The Interface page

**Files:**
- Create: `src/content/docs/gui/interface.mdx`

**Interfaces:**
- Consumes: `gui-system-data-{light,dark}.png` and `gui-observables-{light,dark}.png` from Task 1; the sidebar group from Task 2.

**Sourced facts.** The six tabs, in the order the application creates them (`addTab` calls in `stepss-java-ui/src/my/stepss/StepssUI.java`). **This table was corrected during execution**: the original was assembled from `setText` greps and mis-attributed several controls to the wrong tab. What follows is what each tab actually shows, read off the running application with the Kundur case loaded.

| Tab | Line | Controls, as they appear |
|---|---|---|
| System Data | 1562 | **System data files (required)**: rows 1 to 9 each with a **Load file** button and an edit pencil, plus an unnumbered row 10. **Disturbance file (required)** on its own row below. **Clear files** |
| Observables | 2104 | **Runtime observables**: three type-plus-name rows and **Plot refresh interval (sec)**. **Recording to file**: Save continuous trace, Save discrete trace, Save output trajectory, Save settings comments and initialization data. **Observables file (required when a trajectory is saved)**, Show observable dialog, **Clear files** |
| Initialization | 2226 | Output pane, then **Run power flow**, Add Helios results to data, Bus overview, Generators & SVCs, Adjustable transformers, Global power balance, **Clear all**. The last five enable only after a successful run |
| Dynamic Simulation | 2387 | Output pane, then **Run dynamic simulation**, Stop simulation, Load output, Load continuous trace, Load discrete trace, Load initialization, Save current output, Search..., **Clear all** |
| Analysis | 2636 | **Time-domain analysis**: Extract curves, Preview curve, Save extracted curve, Save current trajectory, Load trajectory, Clear all gnuplot instances. **Small-signal stability analysis**: Select results directory, Results basename (`ssa`), Analysis time t [s] (`0.001`), Real part limit (`-1.0`), PF threshold (`0.05`), Run small-signal stability analysis, View results..., Save dynamic Jacobian..., Load dynamic Jacobian... |
| Codegen | 2739 | Load files for Codegen, Display loaded files, Save converted files, Save executable |

The **Tools** menu, which the page should also cover: Save command file, Save observables file, Open in editor (Ctrl+N), Select external simulator (Ctrl+R), Select working directory, Open working folder (Ctrl+E), Open terminal in working folder (Ctrl+T), Clear all gnuplot instances (Ctrl+G), then Dark theme and Check for updates at startup. The **File** menu is Save configuration (Ctrl+S), Load configuration (Ctrl+L), Open Examples, Exit (Ctrl+Q).

The status bar carries the working directory on the left, and on the right the engine version (`RAMSES 3.74`) plus a state that goes `Idle`, `Solving power flow`, `Power flow finished 3.0 s`, `Simulation finished 2.0 s`.

**The Analysis tab is where small-signal stability analysis lives**, which is consistent with the repo rule that eigenanalysis moved into the engine. Link to `/user-guide/eigenanalysis/` and do not describe a separate MATLAB tool.

Re-read the labels against the source before writing; a label that has changed upstream must be corrected rather than copied from this plan.

**Two upstream typos to report, not to reproduce.** The runtime observable type list (`StepssUI.java:1964`) contains `Center of Intertia` (for Inertia) and `Branch Rective Power Origin`/`Extremity` (for Reactive). Following the repo's practice of reporting a defect rather than documenting around it, spell them correctly in prose and raise them against `stepss-java-ui`.

- [ ] **Step 1: Write the page**

```mdx
---
title: The Interface
description: What each tab of STEPSS GUI is for, and the order you use them in
---
```

Structure: a short paragraph saying the window is six tabs used roughly left to right, then one section per tab, in application order. Each section says what the tab is for and what its controls do. The System Data section carries the screenshot pair:

```html
<img src="/images/screenshots/gui-system-data-light.png"
     alt="The System Data tab with the Kundur two-area case loaded, showing the numbered system data file rows and the disturbance file row below them"
     class="dark:sl-hidden" />
<img src="/images/screenshots/gui-system-data-dark.png"
     alt="The System Data tab with the Kundur two-area case loaded, showing the numbered system data file rows and the disturbance file row below them"
     class="light:sl-hidden" />
```

Close with a short section on the status bar and the Tools menu theme toggle.

**Boundary check:** say *which* files go in which slot and link to `/user-guide/file-formats/` for what those files contain. Do not describe the formats here.

- [ ] **Step 2: Verify the build fails only on `gui/running`**

Run: `npm run build`
Expected: FAIL naming only `gui/running`.

- [ ] **Step 3: Commit**

```bash
git add src/content/docs/gui/interface.mdx
git commit -m "Document the six tabs of STEPSS GUI"
```

---

### Task 4: The Running a Simulation page

**Files:**
- Create: `src/content/docs/gui/running.mdx`

**Interfaces:**
- Consumes: `gui-initialization-*`, `gui-dynamic-simulation-*`, `gui-select-observables-*` and `gui-plot-*` from Task 1.

**Sourced facts.** The Kundur case, from `examples.properties`:

| Slot | Files |
|---|---|
| System data | `lf.dat`, `dyn.dat`, `solveroptions.dat` |
| Disturbance | `disturb.dst` |
| Observables | `obs.dat` |
| Also shipped | `dyn_noPSS.dat`, `README.md`, `LICENSE` |

The disturbance steps load L9 by +0.5 pu at t = 1 s over a 60 s horizon. `dyn_noPSS.dat` is the same case with the stabiliser gain set to zero.

- [ ] **Step 1: Write the page**

```mdx
---
title: Running a Simulation
description: A complete run in STEPSS GUI, from opening the Kundur two-area example to plotting the inter-area mode
---

import { Steps } from '@astrojs/starlight/components';
```

A single `<Steps>` walkthrough: open the example, check the loaded files on System Data, initialize, run, then plot. Each stage gets its screenshot pair, with alt text describing what the reader should be seeing rather than naming the tab.

End with a **Try it with the stabiliser out** section: swap `dyn.dat` for `dyn_noPSS.dat` on the System Data tab, re-run, and compare the damping of the inter-area mode. This is what the example ships two dynamic files for, and it turns a walkthrough into an experiment.

- [ ] **Step 2: Verify the build now passes**

Run: `npm run build`
Expected: PASS. This is the first green build since Task 2.

- [ ] **Step 3: Verify the new section renders**

Run: `npm run dev`, then open `http://localhost:4321/gui/first-run/`
Expected: the STEPSS GUI group appears in the sidebar between Getting Started and Simulation Guide, all three pages load, and every screenshot resolves. Toggle the site theme and confirm each image swaps rather than disappearing or doubling.

- [ ] **Step 4: Commit**

```bash
git add src/content/docs/gui/running.mdx
git commit -m "Add an end-to-end GUI walkthrough on the Kundur case"
```

---

### Task 5: CODEGEN Studio screenshots

**Files:**
- Modify: `src/content/docs/developer/cg-studio.mdx:34-46` (the Interface Overview table)
- Create: `public/images/screenshots/cg-studio-editor.png`, `public/images/screenshots/cg-studio-codegen-result.png`

**CODEGEN Studio ships light only.** It has no dark theme: `src/cg_studio/frontend/css/style.css` has no `prefers-color-scheme` block and no `data-theme` hook, and the colour themes in `js/main.js:41` are per model type (EXC blue, TOR green, INJ orange, TWOP purple). Do **not** fabricate a dark variant. This is tracked upstream as SPS-L/stepss-cg-studio#1; when it lands, recapture as a pair and switch to the `light:sl-hidden` / `dark:sl-hidden` markup used everywhere else.

- [ ] **Step 1: Launch CODEGEN Studio**

Run: `cg-studio --no-browser`
Then open `http://127.0.0.1:8765` in a browser sized to 1600x1000.

- [ ] **Step 2: Build the model from the page's own walkthrough**

Follow `cg-studio.mdx:319-369`: type EXC, name `simple_avr`, add `KA`, `TA` and `VREF` to `%data`, drag `algeq` and `tf1p` onto the canvas, connect them, set the `algeq` expression to `{VREF}-[v]-avr1`, rename the `tf1p` output to `vf`, and add the `avr1` state. Using the documented example rather than an invented one means the screenshot and the surrounding prose cannot drift apart.

- [ ] **Step 3: Capture the editor**

Capture the full window showing all four regions the page's table describes: palette, canvas, block inspector and DSL preview.
Expected: `cg-studio-editor.png`, no wider than 1600 px.

- [ ] **Step 4: Capture the Run Codegen result**

Click **Run Codegen** and capture the modal showing the generated `exc_simple_avr.f90`.
Expected: `cg-studio-codegen-result.png`.

- [ ] **Step 5: Place the images**

Put the editor screenshot directly beneath the **Interface Overview** heading at `cg-studio.mdx:34`, so the three-column layout is shown before it is described in a table. Put the result screenshot in the **Running CODEGEN** section at `:255`.

Because these have no dark twin, give each a neutral frame so it does not glare on the dark site theme. Add to `src/styles/custom.css`:

```css
/* Screenshots with no dark variant: a neutral mat keeps a light-only
   image from glaring against the dark theme. CODEGEN Studio has no dark
   theme yet (SPS-L/stepss-cg-studio#1); remove this when it does. */
.shot-light-only {
	background: var(--sl-color-gray-6);
	padding: 0.75rem;
	border-radius: 0.5rem;
	display: block;
	max-width: 100%;
	height: auto;
}
```

- [ ] **Step 6: Verify**

Run: `npm run build`
Expected: PASS.

Then in `npm run dev`, view `/developer/cg-studio/` in both themes and confirm the images are legible in each.

- [ ] **Step 7: Commit**

```bash
git add public/images/screenshots src/content/docs/developer/cg-studio.mdx src/styles/custom.css
git commit -m "Show the CODEGEN Studio editor rather than only describing it"
```

---

### Task 6: Homepage

**Files:**
- Modify: `src/content/docs/index.mdx:1-38`

**Why this page matters more than its length suggests:** it uses `template: splash`, which is the one page on the site rendered **without a sidebar**. Confirmed against the built output: `dist/index.html` contains no `.sidebar` element while `dist/getting-started/overview/index.html` does. A cold visitor landing here sees no navigation at all, so the page's own content carries the entire wayfinding load.

- [ ] **Step 1: Replace the hero tagline**

The current tagline (`index.mdx:6`) is "A comprehensive power system simulation suite for static and dynamic analysis of electrical grids." Replace it with the sharper definition currently buried at `getting-started/overview.md:6`, plus a line naming who it is for:

```yaml
  tagline: |
    Static and Transient Electric Power Systems Simulation. Compute the power
    flow of a network and simulate its dynamic response to disturbances under
    the phasor approximation. Built for power system researchers, teaching, and
    grid studies.
```

Keep the logo image and the three existing actions unchanged.

- [ ] **Step 2: Add the product screenshot below the hero**

Insert immediately after the frontmatter's closing `---` and the component import, before `## Two Editions`. Use the `gui-initialization` pair from Task 1: it is a real screenshot of the application holding a solved case, and its colour-coded engine output, generator table and power balance read unmistakably as power system software. The `gui-plot` figure is the better *result* image but is a chart rather than the product, so it belongs on `gui/running`, not in the hero position.

```html
<img src="/images/screenshots/gui-initialization-light.png"
     alt="STEPSS GUI showing the solved power flow of the Kundur two-area system: bus voltages, the four generators with their P, Q and voltage setpoints, and the system power balance"
     class="dark:sl-hidden" />
<img src="/images/screenshots/gui-initialization-dark.png"
     alt="STEPSS GUI showing the solved power flow of the Kundur two-area system: bus voltages, the four generators with their P, Q and voltage setpoints, and the system power balance"
     class="light:sl-hidden" />
```

- [ ] **Step 3: Link the edition cards to the comparison**

The two cards at `index.mdx:31-38` currently link only to install anchors. Add a link from the section's intro paragraph to `/getting-started/overview/#two-editions`, which owns the full comparison. Do **not** add a comparison table here; that would be the third copy and breaks the one-owner rule.

- [ ] **Step 4: Add the GUI section to Quick Links**

The `## Quick Links` grid at `:60-81` is the homepage's substitute for the missing sidebar. Add a card pointing at `/gui/first-run/`, placed first, since it is now the shortest path from landing to a running simulation.

- [ ] **Step 5: Verify**

Run: `npm run build`
Expected: PASS.

Run: `grep -rnP '\x{2014}' src/content/docs/index.mdx`
Expected: no output.

- [ ] **Step 6: Commit**

```bash
git add src/content/docs/index.mdx
git commit -m "Lead the homepage with what STEPSS does and show it running"
```

---

### Task 7: The people behind STEPSS

**Files:**
- Modify: `src/content/docs/getting-started/overview.md:8-10`

**Sources**, both supplied by the project owner:
- https://sps-lab.org/author/petros-aristidou/
- https://thierryvancutsem.github.io/home/

**Facts available, and their bounds.** Use these and nothing beyond them. No invented dates, posts or honours.

**Petros Aristidou:** Diploma, Electrical and Computer Engineering, National Technical University of Athens, 2010. PhD, University of Liège, 2015, on domain decomposition methods for real-time dynamic security assessment of transmission systems. Postdoctoral researcher, Power Systems Laboratory, ETH Zurich, one year, on control algorithms for low-inertia systems. Lecturer, University of Leeds, 2016 to 2019, leading the Smart Grids Lab. Assistant Professor in Sustainable Power Systems, Cyprus University of Technology, since January 2020. Helios is his property (`getting-started/license.md:52`).

**Thierry Van Cutsem:** 42 years of research in electric power system engineering, on the dynamics of large power systems: modelling, stability, security and control. Formerly Research Director at the Fund for Scientific Research (FNRS) and Adjunct Professor at the Montefiore Institute, University of Liège. Currently a consultant to transmission system operators and an adviser on research projects. CODEGEN is his property (`license.md:60`).

- [ ] **Step 1: Write the block**

Replace lines 8 to 10 with a section headed `## The people behind STEPSS`. Lead with the people; affiliations follow as attribution rather than opening the sentence.

The connective fact the block turns on: Aristidou's 2015 Liège PhD on **domain decomposition** is the direct origin of the parallel Schur-complement decomposition that RAMSES solves with, published as papers 1 and 2 on `/resources/references/`. Van Cutsem's contribution is the simulation core: the accelerated and localized Newton schemes (paper 3) and the angle-reference treatment that makes long-term runs well posed (paper 5).

Link each name to their own page, and close by pointing at `/resources/references/` so a reader can check the attribution against the papers.

- [ ] **Step 2: Correct the Van Cutsem affiliation**

Line 8 currently reads "Dr. Thierry Van Cutsem (University of Liège)". His own page lists ULiège and FNRS as **former** posts. State the current position instead.

Leave `license.md` untouched: RAMSES remains the property of the University of Liège regardless of where its author works now, and that statement is correct as written.

- [ ] **Step 3: Verify no fact outruns its source**

Re-read the block against the two URLs above. Any sentence that cannot be traced to them, to `/resources/references/`, or to `license.md` must be cut.

- [ ] **Step 4: Verify**

Run: `npm run build`
Expected: PASS.

Run: `grep -rnP '\x{2014}' src/content/docs/getting-started/overview.md`
Expected: no output.

- [ ] **Step 5: Commit**

```bash
git add src/content/docs/getting-started/overview.md
git commit -m "Say who wrote STEPSS, and what each of them contributed"
```

---

### Task 8: Quick Start repairs

**Files:**
- Modify: `src/content/docs/getting-started/quickstart.mdx:95-111` (the dynamic simulation GUI tab)
- Modify: `src/content/docs/getting-started/quickstart.mdx:211-225` (the power flow GUI tab)

**The defect.** Both tabs end with "For detailed GUI usage, visit the [STEPSS website](https://sps-lab.org/project/stepss/)". That page carries no GUI guide. It is also stale in three ways this repo's rules name explicitly: it calls eigenanalysis a MATLAB-based tool, it uses the retired "STEPSS for Java" and "STEPSS for Python" edition names, and it says the Python package was once published under the retired PyRAMSES name. It must stop being cited as documentation.

The steps themselves are also wrong. Both describe "Use File → Open to load your data files". The application has no such flow: system data files are loaded through nine numbered **Load file** rows on the **System Data** tab, with the disturbance file on its own row below them (`StepssUI.java:1181-1315`).

- [ ] **Step 1: Rewrite the dynamic simulation GUI tab**

Replace the six `<Steps>` items with a short pointer plus the correct outline: open a bundled example or load files on the System Data tab, set observables, initialize, run, then analyse. Keep it to a few lines and link to `/gui/running/` for the walkthrough. This page is a comparison of the three interfaces, so it shows one path and links out; it does not grow into a second GUI guide.

Replace the closing line with:

```mdx
For the full walkthrough, see [Running a Simulation](/gui/running/).
```

- [ ] **Step 2: Rewrite the power flow GUI tab**

Same treatment. Replace the closing line with a link to `/gui/interface/`.

- [ ] **Step 3: Confirm the off-site citation is gone from this page**

Run: `grep -n "sps-lab.org/project/stepss" src/content/docs/getting-started/quickstart.mdx`
Expected: no output.

The remaining three references elsewhere are legitimate and stay: `overview.md:10` and `references.md:22` cite it as a project page, which it is, and `nordic.mdx:181` cites the lab. Confirm they are untouched:

Run: `grep -rn "sps-lab.org/project/stepss" src/content/docs/`
Expected: exactly three hits, in `overview.md`, `references.md` and `nordic.mdx`.

- [ ] **Step 4: Verify**

Run: `npm run build`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add src/content/docs/getting-started/quickstart.mdx
git commit -m "Point Quick Start at the GUI guide instead of a page without one"
```

---

### Task 9: Releases and versions

**Files:**
- Create: `src/content/docs/resources/releases.md`
- Modify: `astro.config.mjs` (the `Resources` group, currently lines 148-154)

**Why not a mirrored changelog.** The review asked for an in-site changelog. Releases here are frequent and automated: v3.74.15 shipped roughly eight hours before the review was written. A hand-maintained copy drifts within a week, and fetching the GitHub Releases API at build time puts a network dependency and a rate limit into CI that fails to a silently empty page. The real gap is smaller and fixable: **the site never says which version it documents.**

- [ ] **Step 1: Write the page**

```md
---
title: Releases
description: How STEPSS is versioned, where releases are published, and how to check the version you have
---
```

Cover, in order:

1. **Where releases live.** GitHub Releases, linked out. Say plainly that this site does not mirror the changelog.
2. **The delivery channels**, which are four and are already documented individually on the installation page: the platform installers, the APT repository, the Scoop bucket, and PyPI. Link to `/getting-started/installation/` for each rather than restating the commands.
3. **Checking what you have.** Give the command for each edition: `ramses -v` for the engine (documented at `quickstart.mdx:36`), Help then About in the GUI, and the package version for `stepss`.
4. **What the numbers mean.** Components share a release train: `stepss-java-ui/versions.properties` pins ramses, helios, dyngraph, codegen and uramses, so a STEPSS version identifies a tested combination rather than any one component's own history.

Verify point 4 against `stepss-java-ui/versions.properties` before writing it, and state only what that file actually shows.

- [ ] **Step 2: Register it in the sidebar**

Add to the `Resources` group in `astro.config.mjs`, after `Repositories` and before `Publications`:

```js
						{ label: 'Releases',      slug: 'resources/releases' },
```

- [ ] **Step 3: Verify**

Run: `npm run build`
Expected: PASS, with a page count one higher than the previous task's.

- [ ] **Step 4: Commit**

```bash
git add src/content/docs/resources/releases.md astro.config.mjs
git commit -m "Say how STEPSS is versioned and where releases are published"
```

---

### Task 10: Requesting a commercial licence

**Files:**
- Modify: `src/content/docs/getting-started/license.md:62-68` (insert before the `## Authors` section)

**Hard constraint.** State **no turnaround and no pricing.** Neither fact exists in any repo, and both are commercial commitments that are not this document's to make. The spec records this as reported back to the project owner rather than written.

- [ ] **Step 1: Write the section**

Add `## Requesting a Commercial Licence` covering what to include in an enquiry, so a first message arrives complete:

- which components the use involves (RAMSES, Helios, CODEGEN each have separate owners, already tabulated at the top of this page)
- the intended use, and whether it is consulting, a product, or a funded project with a commercial partner
- the size of the systems involved, since the free tier caps at 1000 buses
- the core count needed, since the free tier caps at 2
- the timeframe

Route it to **stepss@sps-lab.org**, consistent with the existing contact line at `:68`.

Cross-reference the per-component table at the top of the page rather than restating which components are proprietary.

- [ ] **Step 2: Confirm nothing was invented**

Run: `grep -niE "turnaround|within [0-9]|business day|price|pricing|cost|fee|EUR|USD|€|\\$" src/content/docs/getting-started/license.md`
Expected: no hits introduced by this task. A pre-existing hit on "free of charge" is fine.

- [ ] **Step 3: Verify**

Run: `npm run build`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add src/content/docs/getting-started/license.md
git commit -m "Say what a commercial licence enquiry should contain"
```

---

### Task 11: Full-site validation

**Files:**
- Modify: whatever the checks below turn up

- [ ] **Step 1: Clean build from scratch**

Run: `rm -rf dist .astro && npm run build`
Expected: PASS. Compare the page count against Task 0's baseline: it must be exactly four higher (three GUI pages plus Releases).

- [ ] **Step 2: Em-dash sweep**

Run: `grep -rnP '\x{2014}' src CLAUDE.md README.md astro.config.mjs docs`
Expected: no output.

- [ ] **Step 3: Confirm no forbidden topic was reintroduced**

Run: `grep -rniE "pyramses|matlab" src/content/docs/`
Expected: only the three known-good MATLAB hits recorded in `CLAUDE.md:80-86`: the `**` versus `^` syntax warning in `developer/user-models.md`, and the Helios `.m` export in `python/helios.md` and `user-guide/power-flow.md`. Zero PyRAMSES hits.

- [ ] **Step 4: Confirm every screenshot is referenced**

Run: `for f in public/images/screenshots/*.png; do b=$(basename "$f"); grep -rq "$b" src/content/docs/ || echo "ORPHAN: $b"; done`
Expected: no output. An orphan is either a missing image on a page or a file that should not have been committed.

- [ ] **Step 5: Theme-swap check on every screenshot page**

Run `npm run dev` and visit `/`, `/gui/first-run/`, `/gui/interface/`, `/gui/running/` and `/developer/cg-studio/` in both site themes.
Expected: exactly one image visible per pair in each theme. Two visible means a missing utility class; none visible means both classes were applied to the same image.

- [ ] **Step 6: Mobile check**

In the browser's device emulation at 390x844, visit the same five pages.
Expected: no horizontal scroll, and every screenshot scaled to fit rather than overflowing.

- [ ] **Step 7: Confirm the Java preferences node is still gone**

Run: `ls ~/.java/.userPrefs/my/stepss 2>&1`
Expected: `No such file or directory`, unless Task 1 Step 1 found a pre-existing file, in which case confirm the backup was restored.

- [ ] **Step 8: Screenshot the finished site for review**

Capture the homepage and `/gui/running/` in both themes and show them to the project owner, rather than asserting the result.

- [ ] **Step 9: Report what was not done**

Restate the three items from the spec's section 6, which are deliberately unfixed and need the project owner:

1. https://sps-lab.org/project/stepss/ contradicts this documentation on three points and promises GUI detail it does not carry. Separate repository.
2. Hardware requirements are undocumented and need real figures.
3. Commercial licence turnaround and pricing likewise.

- [ ] **Step 10: Commit any fixes from this pass**

```bash
git add -A
git commit -m "Fix what the full-site validation pass turned up"
```

---

## Self-Review

**Spec coverage.** Every section of the spec maps to a task: 3.1 to Tasks 2, 3 and 4; 3.2 to Tasks 1 and 5; 3.3 to Task 6; 3.4 to Task 7; 3.5 to Task 9; 3.6 to Task 10; 3.7 to Task 8; section 4's constraints to Global Constraints and Task 11; section 5 to the validation steps ending each task and Task 11; section 6 to Task 11 Step 9. Spec section 2.2's three refusals are enforced by Task 10 Step 2 and Task 11 Step 9.

**Placeholder scan.** No "TBD", "TODO", "add appropriate error handling" or "similar to Task N". Each page task carries its sourced facts inline with file and line citations, so an implementer who reads only that task can write it.

**Consistency.** Screenshot basenames declared in Task 1 Step 5 (`gui-open-examples`, `gui-system-data`, `gui-observables`, `gui-initialization`, `gui-dynamic-simulation`, `gui-select-observables`, `gui-plot`) are the names used in Tasks 2, 3, 4 and 6. The original list named `gui-analysis` and `gui-dyngraph`; both were revised during execution and every downstream reference was updated with them. The `-light` and `-dark` suffixes and the `dark:sl-hidden` / `light:sl-hidden` pairing are identical everywhere. The three slugs registered in Task 2 Step 1 are the slugs created in Tasks 2, 3 and 4 and linked from Tasks 6 and 8. `.shot-light-only` is defined in Task 5 and used only there, which is correct: it exists for the one case with no dark twin.

**One gap found and closed:** Task 9's sidebar insertion originally omitted the indentation matching `astro.config.mjs`, which uses tabs. The snippet now matches the surrounding entries.
