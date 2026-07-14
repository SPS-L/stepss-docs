# STEPSS Documentation

**Static and Transient Electric Power Systems Simulation** — Official documentation site.

Built with [Astro Starlight](https://starlight.astro.build/) and deployed to GitHub Pages.

🔗 **Live site**: [https://stepss.sps-lab.org/](https://stepss.sps-lab.org/)

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
| [stepss-java-ui](https://github.com/SPS-L/stepss-java-ui) | Java GUI |
| [stepss-pyramses](https://github.com/SPS-L/stepss-pyramses) | Python API |
| [stepss-userguide](https://github.com/SPS-L/stepss-userguide) | LaTeX source docs |
| [stepss-uramses](https://github.com/SPS-L/stepss-uramses) | User-defined models |
| [stepss-eigenanalysis](https://github.com/SPS-L/stepss-eigenanalysis) | Eigenvalue analysis |

## Authors

- [Dr. Petros Aristidou](https://sps-lab.org) — Cyprus University of Technology
- Dr. Thierry Van Cutsem — University of Liège

## License

- **Documentation content** (`src/content/docs/`, `public/images/`) — [CC BY 4.0](LICENSE). Share and adapt freely, including commercially, with appropriate credit.
- **Website code** (Astro config, components, styles) — [MIT](LICENSE-CODE).
- **`public/stepss_userguide.pdf`** — the compiled user guide, redistributed from [stepss-userguide](https://github.com/SPS-L/stepss-userguide) under that repository's licence.

The STEPSS **software** documented here is not covered by either licence — several components are proprietary or non-commercial. See [NOTICE](NOTICE) and the [licence page](https://stepss.sps-lab.org/getting-started/license/).
