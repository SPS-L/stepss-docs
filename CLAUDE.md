# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Documentation site for STEPSS (Static and Transient Electric Power Systems Simulation), built with **Astro 6 + Starlight 0.38**. Deployed to GitHub Pages at https://stepss.sps-lab.org/. Repo: `SPS-L/stepss-docs`.

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
- **Static files**: PDF user guide, CNAME, and favicon in `public/`.

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

## Deployment

GitHub Actions auto-deploys on push to `main` (`.github/workflows/deploy.yml`). PRs get a build check (`.github/workflows/pr-check.yml`). Both use Node 22. Manual deploys via `workflow_dispatch`.
