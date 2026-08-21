// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';
import fortranFreeForm from '@shikijs/langs/fortran-free-form';

// https://astro.build/config
export default defineConfig({
	site: 'https://stepss.sps-lab.org',
	base: '/',
	// The block library used to be one 2300-line page at /developer/codegen-library/;
	// it is now one page per block category under /developer/codegen-blocks/.
	redirects: {
		'/developer/codegen-library': '/developer/codegen-blocks/',
	},
	markdown: {
		remarkPlugins: [remarkMath],
		rehypePlugins: [rehypeKatex],
	},
	integrations: [
		starlight({
			title: 'STEPSS',
			expressiveCode: {
				shiki: {
					langs: [fortranFreeForm],
				},
			},
			description: 'Static and Transient Electric Power Systems Simulation, Documentation',
			logo: {
				light: './src/assets/icon-light.svg',
				dark: './src/assets/icon-dark.svg',
				replacesTitle: false,
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/SPS-L/stepss-docs' },
				{ icon: 'email', label: 'Contact (stepss@sps-lab.org)', href: 'mailto:stepss@sps-lab.org' },
			],
			editLink: {
				baseUrl: 'https://github.com/SPS-L/stepss-docs/edit/main/',
			},
			// Only to hang the User Guide download off the header; the override
			// renders Starlight's own SocialIcons straight after its own button.
			components: {
				SocialIcons: './src/components/SocialIcons.astro',
			},
			customCss: [
				'@fontsource/inter/400.css',
				'@fontsource/inter/600.css',
				'@fontsource/jetbrains-mono/400.css',
				'./src/styles/custom.css',
				'katex/dist/katex.min.css',
			],
			head: [
				{
					tag: 'meta',
					attrs: {
						name: 'keywords',
						content: 'power systems, simulation, RAMSES, stepss, dynamic simulation, STEPSS',
					},
				},
			],
			sidebar: [
				{
					label: 'Getting Started',
					items: [
						{ label: 'Overview',     slug: 'getting-started/overview' },
						{ label: 'Installation', slug: 'getting-started/installation' },
						{ label: 'Quick Start',  slug: 'getting-started/quickstart' },
						{ label: 'License',      slug: 'getting-started/license' },
					],
				},
				{
					// The edition an installer delivers, and the first thing a new
					// reader opens. Ahead of the Simulation Guide because nobody
					// should have to read File Formats before pressing Run. The
					// Python API stays below the guide: scripting users are further
					// along.
					label: 'STEPSS GUI',
					items: [
						{ label: 'First Run',            slug: 'gui/first-run' },
						{ label: 'The Interface',        slug: 'gui/interface' },
						{ label: 'Running a Simulation', slug: 'gui/running' },
					],
				},
				{
					// Flat, in workflow order: describe the network, solve the power
					// flow, then set up and run the dynamic simulation, then analyse it.
					label: 'Simulation Guide',
					items: [
						{ label: 'File Formats',        slug: 'user-guide/file-formats' },
						{ label: 'Network Modeling',    slug: 'user-guide/network' },
						{ label: 'Power Flow',          slug: 'user-guide/power-flow' },
						{ label: 'Reference Frames & Initialization', slug: 'user-guide/reference-frames' },
						{ label: 'Dynamic Data Records', slug: 'user-guide/dynamic-models' },
						{ label: 'Disturbances',        slug: 'user-guide/disturbances' },
						{ label: 'Solver Settings',     slug: 'user-guide/solver-settings' },
						{ label: 'Eigenanalysis',       slug: 'user-guide/eigenanalysis' },
					],
				},
				{
					label: 'Python API',
					items: [
						{ label: 'Introduction', slug: 'python' },
						{ label: 'Overview',      slug: 'python/overview' },
						{ label: 'Installation',  slug: 'python/installation' },
						{ label: 'Examples',      slug: 'python/examples' },
						{ label: 'API Reference', slug: 'python/api-reference' },
						// Not "Power Flow (Helios)": that label belongs to the engine
						// reference under Simulation Guide. This page is the Python API.
						{ label: 'Helios Power-Flow API', slug: 'python/helios' },
					],
				},
				{
					label: 'Model Reference',
					items: [
						{ label: 'Model Index',             slug: 'models' },
						{ label: 'Synchronous Machine',     slug: 'models/synchronous-machine' },
						{ label: 'SM Parameter Conversion', slug: 'models/synchronous-machine-param-conversion' },
						{ label: 'IEEE Exciters',           slug: 'models/ieee-exciters' },
						{ label: 'Custom Exciters',         slug: 'models/custom-exciters' },
						{ label: 'IEEE Governors',          slug: 'models/ieee-governors' },
						{ label: 'Custom Governors',        slug: 'models/custom-governors' },
						{ label: 'Injectors',               slug: 'models/custom-injectors' },
						{ label: 'Two-Port Models',         slug: 'models/two-port-models' },
						{ label: 'Discrete Controllers',    slug: 'models/discrete-controllers' },
					],
				},
				{
					label: 'Extending STEPSS',
					items: [
						{ label: 'User-Defined Models', slug: 'developer/user-models' },
						{
							label: 'CODEGEN Blocks',
							items: [
								{ label: 'Block Index',          slug: 'developer/codegen-blocks' },
								{ label: 'Algebraic & Math',     slug: 'developer/codegen-blocks/algebraic' },
								{ label: 'Transfer Functions',   slug: 'developer/codegen-blocks/transfer-functions' },
								{ label: 'Integrators',          slug: 'developer/codegen-blocks/integrators' },
								{ label: 'Controllers',          slug: 'developer/codegen-blocks/controllers' },
								{ label: 'Limiters & Switching', slug: 'developer/codegen-blocks/limiters' },
								{ label: 'Frequency Estimation', slug: 'developer/codegen-blocks/frequency' },
								{ label: 'Automata & Timers',    slug: 'developer/codegen-blocks/automata' },
								{ label: 'Functions Reference',  slug: 'developer/codegen-blocks/functions' },
							],
						},
						{ label: 'CODEGEN Model Examples', slug: 'developer/codegen-examples' },
						{ label: 'CODEGEN Studio',         slug: 'developer/cg-studio' },
						{ label: 'URAMSES',                slug: 'developer/uramses' },
					],
				},
				{
					// Ordered smallest to largest, which is also easiest to hardest.
					label: 'Test Systems',
					items: [
						{ label: 'Overview',               slug: 'test-systems' },
						{ label: '5-Bus Test System',      slug: 'test-systems/5bus' },
						{ label: 'Kundur Two-Area System', slug: 'test-systems/kundur' },
						{ label: 'Nordic Test System',     slug: 'test-systems/nordic' },
						{ label: 'GB Network',             slug: 'test-systems/gb-network' },
					],
				},
				{
					label: 'Resources',
					items: [
						{ label: 'Repositories',  slug: 'resources/repositories' },
						{ label: 'Releases',      slug: 'resources/releases' },
						{ label: 'Publications',  slug: 'resources/references' },
						{ label: 'User Guide (PDF)', link: '/stepss_docs.pdf',
						  attrs: { download: true } },
					],
				},
			],
		}),
	],
});
