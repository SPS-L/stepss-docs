# Responding to the August 2026 site review

**Date:** 2026-08-17
**Scope:** `stepss-docs` only
**Input:** `STEPSS Website Review.md` (17 Aug 2026), reviewing https://stepss.sps-lab.org at release v3.74.15

## 1. What the review got right, and what it missed

The review's factual claims check out. `/about/` and `/team/` do 404, the site
carries no screenshot of either application, and the homepage pitch is weaker
than the definition sitting one click deeper on Overview.

It under-diagnoses its own top finding. The absence of screenshots is a symptom;
the cause is that **this site has no GUI documentation at all**. Two Quick Start
tabs (`quickstart.mdx:110` and `:223`) end with "For detailed GUI usage, visit
the STEPSS website" and link to https://sps-lab.org/project/stepss/. That page
carries no GUI guide. It is a project blurb, and it additionally restates three
things this repo's rules forbid: that eigenanalysis is a MATLAB-based tool, the
retired "STEPSS for Java" and "STEPSS for Python" edition names, and the retired
PyRAMSES distribution name.

So the site's only pointer to GUI usage is a dead end that also contradicts the
documentation pointing at it. Screenshots have nowhere to live because the page
they belong on does not exist.

A second thing the review missed: STEPSS GUI ships an **Open Examples** dialog
offering Kundur two-area, IEEE Nordic and a 5-bus tutorial, each of which copies
a complete working case into the user's examples directory in one click. It is
the fastest first-run path in the product and it appears nowhere on this site.

The sidebar has a six-page **Python API** section documenting one edition and
nothing at all for the other. That asymmetry is the shape of the problem.

## 2. Verdict on each of the review's seven prioritized fixes

| # | Review's fix | Verdict | Reason |
|---|---|---|---|
| 1 | Add 3 to 5 screenshots | **Accept, enlarged** | Needs a GUI section to host them; see 3.1 |
| 2 | Rewrite the homepage hero | **Accept** | See 3.3 |
| 3 | Add an About/Team page | **Modify** | A Team page duplicates sps-lab.org and goes stale. Consolidate onto Overview instead; see 3.4 |
| 4 | Add a GUI vs Python table | **Reject** | `overview.md:33-58` already carries it, with a capability difference the review's version lacks. A third copy breaks the repo's one-owner-per-topic rule |
| 5 | Add an in-site changelog | **Modify** | See 3.5 |
| 6 | Clarify the commercial licence process | **Accept, partially** | See 3.6 |
| 7 | Add a top nav bar | **Reject as specified** | See 2.1 |

### 2.1 Why no top nav

Starlight has no top-nav slot. Adding one means overriding the `Header`
component, which is a maintenance burden across Starlight upgrades and brings
its own mobile behaviour to get wrong.

It also solves the wrong problem. Every destination the review lists (Docs,
Download, Publications, About) is already one click away in a sidebar that is
permanently visible on desktop. The genuine friction is narrower and provable:
the homepage uses `template: splash`, which is **the one page on the site with
no sidebar**. Confirmed by comparing the built output:

```
dist/index.html                          -> no .sidebar element
dist/getting-started/overview/index.html -> .sidebar present
```

A cold visitor landing on the homepage therefore sees no navigation at all. The
fix belongs in the homepage's own content (section 3.3), not in site chrome.

### 2.2 Not doing, and why

- **Hardware requirements** (review's missing-element 6). No authoritative RAM
  or core-count figures exist in any repo. Measuring one machine's usage is not
  a system requirement. Flag to the authors rather than invent.
- **Pricing and turnaround** for commercial licences. Same reason; see 3.6.
- **Fixing sps-lab.org.** Out of this repo. Report it; stop citing it as
  documentation.

## 3. The work

### 3.1 New "STEPSS GUI" sidebar section, three pages

Placed **immediately after Getting Started**, before Simulation Guide. Reading
order rationale: a new user installs, opens the application, and clicks Run. They
should not have to pass through File Formats first. Python API stays where it is;
scripting users are further along.

| Page | Slug | Content |
|---|---|---|
| First Run | `gui/first-run` | Licence acceptance, the toolchain check, working and examples directories, and the Open Examples dialog with its three bundled cases |
| The Interface | `gui/interface` | The six tabs (System Data, Observables, Initialization, Dynamic Simulation, Analysis, Codegen), the status bar, the dark-theme toggle |
| Running a Simulation | `gui/running` | End to end on Kundur two-area, from Open Examples through initialization and the run to a DYNGRAPH plot of the inter-area mode |

Three pages, so no section index page is needed (the repo rule sets that
threshold at about four) and no single-page group is created.

**Boundary.** These pages document *driving the application*. They link to
Simulation Guide for what the data means, and to CODEGEN Studio and
User-Defined Models for model building. They do not restate either. Any
parameter table or record syntax appearing on a GUI page is a defect.

Register all three in `astro.config.mjs` under a new `STEPSS GUI` group.

### 3.2 Screenshots

**Capture method.** Reproducible rather than ad hoc. Before each launch, write
the Java preferences node `my.stepss.StepssUI` with `windowMaximised=false` and
fixed `windowX/Y/Width/Height`, plus `darkTheme` for the dark pass. Every shot
is then identically framed and the light and dark pairs align pixel for pixel.

The preferences file does not currently exist on this machine, so it is created
for the session and **removed afterwards**, leaving the user's settings as they
were. Capture with `import -window <id>` under XWayland; verified working.

**Inventory.** Six GUI shots, each a light and dark pair:

1. Open Examples dialog (branding plus the three cases)
2. System Data tab with Kundur loaded
3. Initialization tab
4. Dynamic Simulation tab mid-run
5. Analysis tab
6. DYNGRAPH plot of the Kundur inter-area mode

**CODEGEN Studio ships light only.** It has no dark theme; its colour themes are
per model type (EXC blue, TOR green, INJ orange, TWOP purple), not light and
dark. Its two shots (full editor with a model loaded, and the Run Codegen
result) are single images framed on a neutral background so they do not glare on
the dark site theme. Do not fake a dark variant.

**Storage and markup.** `public/images/screenshots/`, absolute paths per the repo
image convention. Theme swapping uses Starlight's own utility classes, confirmed
present in `node_modules/@astrojs/starlight/style/util.css`:

```html
<img src="/images/screenshots/x-light.png" alt="..." class="dark:sl-hidden" />
<img src="/images/screenshots/x-dark.png"  alt="..." class="light:sl-hidden" />
```

No custom CSS. Every image carries real alt text describing what is shown, not
"screenshot of STEPSS".

### 3.3 Homepage

- Hero tagline becomes the sharper Overview definition, plus one line naming who
  it is for.
- The logo stays in the hero. A product screenshot goes directly beneath it.
  This is the one page with no sidebar and currently the one page offering a cold
  visitor no visual proof that the software exists.
- Two Editions and Core Modules stay. The edition cards link into the Overview
  comparison rather than growing a third copy of it.
- Quick Links carries the wayfinding load that the missing sidebar would
  otherwise provide.

### 3.4 Overview: the people, not the institutions

Replace the single author line at `overview.md:8` with a block about the two
people. Institutions appear as affiliation, not as the subject.

Sourced from https://sps-lab.org/author/petros-aristidou/ and
https://thierryvancutsem.github.io/home/, supplied by the project owner:

- **Petros Aristidou.** Diploma, National Technical University of Athens, 2010.
  PhD, University of Liège, 2015, on domain decomposition methods for real-time
  dynamic security assessment. Postdoc at the Power Systems Laboratory, ETH
  Zurich. Lecturer at the University of Leeds, 2016 to 2019, leading the Smart
  Grids Lab. Assistant Professor in Sustainable Power Systems at the Cyprus
  University of Technology since January 2020. The PhD is the direct origin of
  the Schur-complement decomposition in RAMSES, which is the connective fact the
  block turns on. Helios is his property (`license.md:52`).
- **Thierry Van Cutsem.** 42 years in power system dynamics: modelling,
  stability, security and control. Formerly Research Director at the Fund for
  Scientific Research (FNRS) and Adjunct Professor at the Montefiore Institute,
  University of Liège; **currently a consultant to transmission system operators
  and an adviser on research projects**. CODEGEN is his property
  (`license.md:60`).

**Correction to make.** The site currently says "Dr. Thierry Van Cutsem
(University of Liège)". His own page lists ULiège and FNRS as former posts. Say
what is true now. RAMSES remains the property of the University of Liège
regardless, and that statement on `license.md` stays as it is.

Each claim in the block must trace to one of: those two pages, the papers on
`resources/references.md`, or `license.md`. No career detail beyond what those
sources state.

### 3.5 New `resources/releases`

Not a mirrored changelog. Releases are frequent and automated (v3.74.15 shipped
about eight hours before the review), so a hand-maintained copy drifts within a
week, and fetching the GitHub Releases API at build time puts a network
dependency and a rate limit into CI that fails to an empty page.

The real gap is smaller: **the site never says which version it documents.** The
page covers what the version numbers mean, the four delivery channels
(installers, APT, Scoop, PyPI), how to check an installed version, and links out
to GitHub Releases.

### 3.6 License: requesting a commercial licence

A short section on `license.md` covering what to include in an enquiry: intended
use, organisation, system size, core count, timeframe. Routed to
stepss@sps-lab.org, consistent with the existing contact line.

States **no turnaround and no pricing.** Those facts are not in any repo and are
a commercial commitment that is not this document's to make.

### 3.7 Quick Start repairs

- Replace both "For detailed GUI usage, visit the STEPSS website" dead ends with
  links into the new GUI section.
- Correct the GUI steps. They currently describe a `File -> Open` flow; the
  application presents per-row **Load file** buttons across six tabs, and the
  fastest path is Open Examples, which the steps never mention.

## 4. Constraints carried from the repo rules

- **No em-dashes** (U+2014) anywhere. Verify with
  `grep -rnP '\x{2014}' src CLAUDE.md README.md astro.config.mjs`, which must
  return nothing. En-dashes in numeric ranges and compound names are fine.
- **One owner per topic.** No new page may restate record syntax, model
  parameters, or the edition comparison.
- **New pages must be registered** in the `sidebar` array in `astro.config.mjs`
  or they do not appear.
- **Sidebar stays two levels deep at most**, and no group holds a single page.
- **Never reintroduce**: the MATLAB eigenanalysis tool, PFC as a live
  alternative, or the retired PyRAMSES name.
- **Factual claims about the GUI** are checked against `stepss-java-ui` source,
  in the same way model pages are checked against `stepss-ramses`.

## 5. Validation

- `npm run build` after each stage. It is the repo's only validation step and it
  catches dead links, bad frontmatter and MDX syntax errors.
- The em-dash grep above.
- Every new internal link resolved, including the two Quick Start replacements.
- The rendered site screenshotted and shown to the project owner, rather than
  asserted to work.
- The Java preferences node removed after capture, and its absence confirmed.

## 6. Reported back, not fixed here

1. **https://sps-lab.org/project/stepss/ contradicts this documentation** on
   three points the repo rules name explicitly (MATLAB eigenanalysis, the
   "STEPSS for Java"/"for Python" edition names, the retired PyRAMSES name), and
   promises GUI usage detail it does not contain. It is a separate repository.
2. **Hardware requirements** are undocumented and need the authors' figures.
3. **Commercial licence turnaround and pricing** likewise.
