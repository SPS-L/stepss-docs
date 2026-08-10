# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Documentation site for STEPSS (Static and Transient Electric Power Systems Simulation), built with **Astro 7 + Starlight 0.41**. Deployed to GitHub Pages at https://stepss.sps-lab.org/. Repo: `SPS-L/stepss-docs`.

## Commands

| Command | Purpose |
|---------|---------|
| `npm install` | Install dependencies (required after clone or dependency changes) |
| `npm run dev` | Start dev server (http://localhost:4321) |
| `npm run build` | Build static site to `dist/` — **this is the only validation step** |
| `npm run preview` | Preview production build locally |

There are no tests or linters configured. **Always run `npm run build` after changes** — it catches broken links, bad frontmatter, MDX syntax errors, and missing imports.

## Architecture

- **Content**: All documentation lives in `src/content/docs/` as `.md` or `.mdx` files. URL slugs map directly from file paths (e.g., `user-guide/network.md` → `/user-guide/network/`).
- **Sidebar/Navigation**: Defined entirely in `astro.config.mjs` under the `sidebar` array. New pages **must** be registered there with their `slug` to appear in navigation. The sidebar supports nested `items` arrays for sub-sections.
- **Styling**: Custom theme overrides in `src/styles/custom.css` (blue accent, Inter/JetBrains Mono fonts).
- **Math**: KaTeX via `remark-math` + `rehype-katex` + `starlight-katex`. Use `$...$` inline and `$$...$$` display.
- **Images**: Diagrams (SVGs) go in `public/images/` and are referenced as absolute paths (`/images/foo.svg`). Use `<img src="/images/..." alt="..." style="width:60%" />` for sizing control. Logos/icons are in `src/assets/`.
- **Static files**: PDF user guide, CNAME, and favicon in `public/`. `public/stepss_docs.pdf` is a copy of the compiled `stepss_doc.pdf` from the `stepss-userguide` repo — refresh it whenever the user guide is rebuilt.

## Content Conventions

### Frontmatter
Every page requires YAML frontmatter with `title` and `description`. The landing page (`index.mdx`) additionally uses `template: splash` with a `hero` block.

### MD vs MDX
- Use `.md` for pages with only Markdown, math, and HTML `<img>` tags. Starlight's `:::note`, `:::tip`, `:::caution` directive syntax works in plain `.md` files.
- Use `.mdx` when you need Starlight components (`<Tabs>`, `<TabItem>`, `<Steps>`, `<Card>`, `<CardGrid>`, `<Aside>`). These **must** be imported at the top: `import { Tabs, TabItem } from '@astrojs/starlight/components';`
- Bare curly braces in `.mdx` must be escaped (`{'{'}`) to avoid JSX parsing errors. This is a common build failure cause.

### Domain content patterns
- Data format documentation follows a consistent structure: concept explanation → circuit/block diagram (SVG) → data format code block → parameter table with Field/Description/Unit columns.
- Model reference pages (exciters, governors, injectors) use `<Tabs>`/`<TabItem>` to group variants, with each tab containing a block diagram, parameter table, and initialization notes.

### Model pages follow the RAMSES code

This site documents an engine it does not contain. **`stepss-ramses` is the
authority for every factual claim on a model page** — never write one from a
paper, from another simulator's manual, or from an older revision of this site.
Check it against the source before publishing:

| Claim | Source of truth |
|---|---|
| Name valid in a `.dat` file | the `case(...)` labels in `src/devices/usr_<kind>_models.f90`, plus the built-in `select case` in `src/devices/<kind>_model.f90` |
| Parameter names and their **order** | the `parname(...)` assignments under `case (define_var_and_par)` in the model's `.f90` |
| Number of data vs additional parameters | `nbdata` / `nbaddpar` in the same block |
| Observables | `obsname(...)` under `case (define_obs)` |

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
  same block was missing `parname(1..6)` altogether — fixed in RAMSES rather
  than documented around.

State a version floor whenever a model is not in every release — the IEEE
governors do not exist before 3.50, and a user on an older build otherwise
reads a page describing models their binary cannot load. `git ls-tree <tag>`
and `git show <tag>:<file>` in `stepss-ramses` date a model precisely.

## Deployment

GitHub Actions auto-deploys on push to `main` (`.github/workflows/deploy.yml`). PRs get a build check (`.github/workflows/pr-check.yml`). Both use Node 22. Manual deploys via `workflow_dispatch`.
