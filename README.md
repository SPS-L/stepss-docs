# STEPSS Documentation

**Static and Transient Electric Power Systems Simulation** — Official documentation site.

Built with [Astro Starlight](https://starlight.astro.build/) and deployed to GitHub Pages.

🔗 **Live site**: [https://sps-l.github.io/stepss-docs/](https://sps-l.github.io/stepss-docs/)

## Local Development

```bash
# Install dependencies
npm install

# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/content/docs/
├── index.mdx                    # Landing page
├── getting-started/             # Installation, overview, quick start, license
├── user-guide/                  # Network, PFC, disturbances, solver, models
├── pyramses/                    # PyRAMSES overview, install, API, examples
├── developer/                   # CODEGEN, user models, URAMSES
└── resources/                   # References, repositories
```

## Editing Documentation

All documentation lives in `src/content/docs/` as Markdown (`.md`) or MDX (`.mdx`) files. Each file has frontmatter with `title` and `description`.

### Adding a New Page

1. Create a `.md` file in the appropriate directory
2. Add frontmatter:
   ```yaml
   ---
   title: Your Page Title
   description: Brief description
   ---
   ```
3. Add the page to the sidebar in `astro.config.mjs`
4. Commit and push — GitHub Actions will deploy automatically

### Math Support

KaTeX is enabled for LaTeX math rendering. Use `$...$` for inline math and `$$...$$` for display math.

### Tabbed Content

Use Starlight's built-in components for tabbed content (GUI/Python/CLI):

```mdx
import { Tabs, TabItem } from '@astrojs/starlight/components';

<Tabs>
<TabItem label="Python">
Content for Python tab
</TabItem>
<TabItem label="GUI">
Content for GUI tab
</TabItem>
</Tabs>
```

## Deployment

The site deploys automatically via GitHub Actions when pushing to `main`. The workflow:

1. Checks out the code
2. Installs Node.js 22 and dependencies
3. Builds the static site with `astro build`
4. Deploys to GitHub Pages

### Manual Deployment

Trigger a manual deployment from the GitHub Actions tab → "Deploy to GitHub Pages" → "Run workflow".

## Related Repositories

| Repository | Description |
|------------|-------------|
| [STEPSS](https://github.com/SPS-L/STEPSS) | Java GUI |
| [stepss-PyRAMSES](https://github.com/SPS-L/stepss-PyRAMSES) | Python API |
| [STEPSS-Userguide](https://github.com/SPS-L/STEPSS-Userguide) | LaTeX source docs |
| [stepss-URAMSES](https://github.com/SPS-L/stepss-URAMSES) | User-defined models |
| [RAMSES-Eigenanalysis](https://github.com/SPS-L/RAMSES-Eigenanalysis) | Eigenvalue analysis |

## Authors

- [Dr. Petros Aristidou](https://sps-lab.org) — Cyprus University of Technology
- Dr. Thierry Van Cutsem — University of Liège
