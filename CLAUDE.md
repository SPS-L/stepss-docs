# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Documentation site for STEPSS (Static and Transient Electric Power Systems Simulation), built with **Astro 6 + Starlight 0.38**. Deployed to GitHub Pages at https://stepss.sps-lab.org/.

## Commands

| Command | Purpose |
|---------|---------|
| `npm run dev` | Start dev server |
| `npm run build` | Build static site to `dist/` |
| `npm run preview` | Preview production build locally |

There are no tests or linters configured.

## Architecture

- **Content**: All documentation lives in `src/content/docs/` as `.md` or `.mdx` files. URL slugs map directly from file paths (e.g., `user-guide/network.md` → `/user-guide/network/`).
- **Sidebar/Navigation**: Defined entirely in `astro.config.mjs` under the `sidebar` array. New pages must be registered there to appear in navigation.
- **Styling**: Custom theme overrides in `src/styles/custom.css` (blue accent color scheme, Inter/JetBrains Mono fonts).
- **Math**: KaTeX enabled via `remark-math` + `rehype-katex`. Use `$...$` for inline and `$$...$$` for display math.
- **Assets**: SVG logos/icons in `src/assets/`, static files (PDF, CNAME) in `public/`.

## Content Conventions

- Every doc page needs YAML frontmatter with `title` and `description`.
- MDX files use Starlight components: `<Tabs>`, `<TabItem>`, `<Steps>`, `<Card>`, `<CardGrid>`, `<Aside>`.
- Bare curly braces in MDX must be escaped (`{'{'}`) to avoid JSX parsing errors.
- The landing page (`src/content/docs/index.mdx`) uses `template: splash`.

## Deployment

GitHub Actions auto-deploys on push to `main` (`deploy.yml`). PRs get a build check (`pr-check.yml`). Both use Node 22.
