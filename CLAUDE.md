# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Documentation site for STEPSS (Static and Transient Electric Power Systems Simulation), built with **Astro 7 + Starlight 0.41**. Deployed to GitHub Pages at https://stepss.sps-lab.org/. Repo: `SPS-L/stepss-docs`.

## Commands

| Command | Purpose |
|---------|---------|
| `npm install` | Install dependencies (required after clone or dependency changes) |
| `npm run dev` | Start dev server (http://localhost:4321) |
| `npm run build` | Build static site to `dist/`, **the only validation step** |
| `npm run preview` | Preview production build locally |

There are no tests or linters configured. **Always run `npm run build` after changes**: it catches broken links, bad frontmatter, MDX syntax errors, and missing imports.

## Architecture

- **Content**: All documentation lives in `src/content/docs/` as `.md` or `.mdx` files. URL slugs map directly from file paths (e.g., `user-guide/network.md` → `/user-guide/network/`).
- **Sidebar/Navigation**: Defined entirely in `astro.config.mjs` under the `sidebar` array. New pages **must** be registered there with their `slug` to appear in navigation. The sidebar supports nested `items` arrays for sub-sections.
  - Keep the tree **two levels deep at most**, and never create a group holding a
    single page. `CODEGEN Blocks` is the one nested group, because it is a nine-page
    reference.
  - A sidebar `label` that differs from the page's own `title` shows up as two
    names for one page (sidebar vs breadcrumb). Only diverge deliberately, as with
    the deliberately-shortened model page labels.
  - Each section with more than about four pages gets an index page at the section
    root (`models/index.md`, `test-systems/index.md`). Link to **that**, never to an
    arbitrary member page standing in for the section.
- **Styling**: Custom theme overrides in `src/styles/custom.css` (blue accent, Inter/JetBrains Mono fonts).
- **Math**: KaTeX via `remark-math` + `rehype-katex` + `starlight-katex`. Use `$...$` inline and `$$...$$` display.
- **Images**: Diagrams (SVGs) go in `public/images/` and are referenced as absolute paths (`/images/foo.svg`). Use `<img src="/images/..." alt="..." style="width:60%" />` for sizing control. Logos/icons are in `src/assets/`.
- **Static files**: PDF user guide, CNAME, and favicon in `public/`. `public/stepss_docs.pdf` is a copy of the compiled `stepss_doc.pdf` from the `stepss-userguide` repo; refresh it whenever the user guide is rebuilt.

## Content Conventions

### No em-dashes

Use ordinary punctuation (comma, colon, semicolon, parentheses, or a new
sentence) instead of an em-dash (U+2014). This is house style across every
`stepss-*` repo. Check with:

```sh
grep -rnP '\x{2014}' src CLAUDE.md README.md astro.config.mjs
```

It must come back empty. En-dashes (U+2013) are fine
where they belong: numeric ranges (`g1–g20`), and compound names such as
Newton–Raphson and lead–lag.

### Helios is the power flow, and the Python package is `stepss`

The power-flow engine is **Helios**. The Python distribution is **`stepss`**.

**Two names are banned outright from this site: PFC and PyRAMSES.** Not as a live
alternative, not as a deprecated one, not as a `pfc` executable, not as a
migration note, not as a historical aside, and not as a redirect. Write as though
neither ever existed. This is a hard rule from the project owner, and it is
stricter than what this file said before: a "Historical Note: PFC" section on
`user-guide/power-flow.md`, a succession paragraph on
`getting-started/overview.md`, and a `/user-guide/pfc` redirect were all removed
to satisfy it.

A reader arriving with a case built for the old power flow is served by the
current [Power Flow](/user-guide/power-flow/) reference, which documents the
format that is read today. A reader arriving with old Python code is served by
the retired distribution's own PyPI page, not by this site.

Check with:

```sh
grep -rniE 'pfc|pyramses' src astro.config.mjs README.md
```

It must come back empty. When removing a URL that other repos link to, repoint
the links in those repos first: dropping the `/user-guide/pfc` redirect required
fixing three references in stepss-helios (`README.md` twice,
`docs/architecture.md` once) so they would not 404.

### Eigenanalysis is in the engine, and MATLAB is not part of STEPSS

Small-signal analysis is performed by RAMSES itself, triggered by the `EIG`
disturbance or the `run_ssa` C entry, and documented on
`user-guide/eigenanalysis.md`. In STEPSS GUI it is the **Small-signal stability
analysis** half of the Analysis tab.

**MATLAB support for small-signal analysis was removed, and no reference to it is
to be kept.** No `ssa(...)` call, no `matlab` code fence, no MATLAB version
prerequisite, no QZ/ARPACK/JDQR method menu, and no note explaining that such a
tool used to exist. `stepss-eigenanalysis` holds reference data and a validation
suite; it is not a tool a reader installs, and its tests need neither MATLAB nor a
RAMSES licence.

The ban is on **that tool**, not on the word. MATLAB mentions unrelated to it are
fine and two are load-bearing: Helios exports a `.m` file
(`python/helios.md`, `user-guide/power-flow.md`), which is an output format rather
than a dependency and needs no section or caveat of its own; and
`developer/user-models.md` notes that the exponent operator is `**` and not `^` as
in MATLAB, which is a genuine syntax warning for readers arriving from there.
`models/synchronous-machine-param-conversion.md` linking `Sync_mach_Octave`, a
parameter-conversion reference implementation, is likewise unrelated.

The `JAC` disturbance stays documented. It exports the raw matrices and is a
different feature from `EIG`, which analyses them.

**`EIG` takes a basename and nothing else, and its two former parameters are
not to be documented as options.** From RAMSES 3.79 the engine writes every
mode into all three results files: `real_limit` became a live control in the
results window (`user-guide/eigenanalysis.md`, "Filtering and zooming"), and
`pf_threshold` became the `$PF_THRES` solver setting, owned by
`user-guide/solver-settings.md`. The Analysis tab has no threshold fields, so
do not describe any on `gui/interface.mdx`. Both parameters appear on this site
only as migration notes saying where they went, because a `.dst` still carrying
either is refused rather than ignored and a reader hitting that needs to be
told what to do.

Check with:

```sh
grep -rniE '\bssa\(|requires matlab|R20[0-9][0-9][ab]|QZ|ARPACK|JDQR' src
```

It must come back empty. A bare `grep -rni matlab src` is **not** the test: it has
legitimate hits.

### The Python package is `stepss`, and has no other name here

The Python API lives under `/python/` and the PyPI distribution is `stepss`,
starting at version 3.59. The package's former name is deliberately absent from
this site: no page mentions it, and no redirect serves its old URLs. Do not
reintroduce either when writing about installation, version pinning or
migration. A reader arriving with older code is served by the PyPI page of the
retired distribution, not by this site.

### Frontmatter
Every page requires YAML frontmatter with `title` and `description`. The landing page (`index.mdx`) additionally uses `template: splash` with a `hero` block.

### MD vs MDX
- Use `.md` for pages with only Markdown, math, and HTML `<img>` tags. Starlight's `:::note`, `:::tip`, `:::caution` directive syntax works in plain `.md` files.
- Use `.mdx` when you need Starlight components (`<Tabs>`, `<TabItem>`, `<Steps>`, `<Card>`, `<CardGrid>`, `<Aside>`). These **must** be imported at the top: `import { Tabs, TabItem } from '@astrojs/starlight/components';`
- Bare curly braces in `.mdx` must be escaped (`{'{'}`) to avoid JSX parsing errors. This is a common build failure cause.

### Domain content patterns
- Data format documentation follows a consistent structure: concept explanation → circuit/block diagram (SVG) → data format code block → parameter table with Field/Description/Unit columns.
- Model reference pages carry one section per model, in this order: scientific
  description (with a block-diagram SVG where one exists), parameter table, then
  a usage example showing a RAMSES data-file excerpt. `models/ieee-governors.mdx`
  is the reference implementation; match it when adding a model.
- `<Tabs>`/`<TabItem>` are used **within** a usage example (data file vs notes),
  not to group model variants. Pages that need no components are `.md`.

### One owner per topic

Every fact has exactly one page that states it; every other page links to that
page. The site previously carried the model-name rosters in eight places and
documented THEVEQ, IMPLOAD, LTC, RT and SIM_MINMAX* twice each, and the copies
drifted into contradicting one another on version floors, units and file counts.

The division that holds today:

| Topic | Owner |
|---|---|
| Record **syntax** (`SYNC_MACH`, `INJEC`, `IMPLOAD`, `TWOP`, `DCTL`) | `user-guide/dynamic-models.md` |
| Which model names exist and their state | `models/index.md` |
| A model's parameters, equations, examples | its family page under `models/` |
| Power-flow records, settings, menu, exit status | `user-guide/power-flow.md` |
| The Python API for any of the above | the matching `python/` page |

Before adding a table or explanation, check whether its owner already has one. If
you find the same fact in two places, delete one and link instead. A tutorial page
(`quickstart`, `examples`) shows one path and links out; it does not carry
reference tables.

### Model pages follow the RAMSES code

This site documents an engine it does not contain. **`stepss-ramses` is the
authority for every factual claim on a model page**. Never write one from a
paper, from another simulator's manual, or from an older revision of this site.
Check it against the source before publishing:

| Claim | Source of truth |
|---|---|
| Name valid in a `.dat` file | the `case(...)` labels in `src/devices/usr_<kind>_models.f90`, plus the built-in `select case` in `src/devices/<kind>_model.f90` |
| Parameter names and their **order** | the `parname(...)` assignments under `case (define_var_and_par)` in the model's `.f90` |
| Number of data vs additional parameters | `nbdata` / `nbaddpar` in the same block |
| Observables | `obsname(...)` under `case (define_obs)` |
| Whether a model is compiled at all | `MODEL_DIRS` in `build/Makefile.gfortran`. `models/*/hq/` is excluded, so the Hydro-Québec families are neither built nor shipped: never tell a reader they can enable one through URAMSES |

Three traps this has produced before:

- **A model's subroutine name is not necessarily a valid data-file name.** They
  are two separate strings and they do diverge: `TGOV1` is implemented by
  `tor_TGOV1D`, and writing `TGOV1D` in a data file fails. Head each section
  `## NAME (\`tor_impl\`)` so both are visible and the difference is obvious.
- **Compiled ≠ reachable.** A model can be in the library yet registered under
  no name (`tor_gasturbm`, `tor_govclasm`, `tor_govhydr`, `tor_govnuc`). Those
  need an explicit caution, not a silent listing beside working models.
- **The `.txt` model description can disagree with the generated `.f90`.** The
  `.f90` is what runs, so document that; but a disagreement is usually a bug in
  the `.f90`, so report it rather than just writing it down. `tor_ENTSOE_simp`
  reported its additional parameter as `Tm0` where the `.txt` said `C`, and the
  same block was missing `parname(1..6)` altogether, fixed in RAMSES rather
  than documented around.

State a version floor whenever a model is not in every release: the IEEE
governors do not exist before 3.50, and a user on an older build otherwise
reads a page describing models their binary cannot load. `git ls-tree <tag>`
and `git show <tag>:<file>` in `stepss-ramses` date a model precisely.

## Deployment

GitHub Actions auto-deploys on push to `main` (`.github/workflows/deploy.yml`). PRs get a build check (`.github/workflows/pr-check.yml`). Both use Node 22. Manual deploys via `workflow_dispatch`.
