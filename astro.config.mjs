// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// https://astro.build/config
export default defineConfig({
	site: 'https://stepss.sps-lab.org',
	base: '/',
	markdown: {
		remarkPlugins: [remarkMath],
		rehypePlugins: [rehypeKatex],
	},
	integrations: [
		starlight({
			title: 'STEPSS',
			description: 'Static and Transient Electric Power Systems Simulation — Documentation',
			logo: {
				light: './src/assets/logo-light.png',
				dark: './src/assets/logo-dark.png',
				replacesTitle: false,
			},
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/SPS-L/STEPSS-GUI' },
			],
			editLink: {
				baseUrl: 'https://github.com/SPS-L/stepss-docs/edit/main/',
			},
			customCss: [
				'./src/styles/custom.css',
				'katex/dist/katex.min.css',
			],
			head: [
				{
					tag: 'meta',
					attrs: {
						name: 'keywords',
						content: 'power systems, simulation, RAMSES, PyRAMSES, dynamic simulation, STEPSS',
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
					],
				},
				{
					label: 'Simulation Guide',
					items: [
						{
							label: 'Data Formats',
							items: [
								{ label: 'File Formats',    slug: 'user-guide/file-formats' },
								{ label: 'Network Modeling', slug: 'user-guide/network' },
							],
						},
						{
							label: 'Power Flow (PFC)',
							items: [
								{ label: 'Power Flow Data & Settings', slug: 'user-guide/pfc' },
							],
						},
						{
							label: 'Dynamic Simulation',
							items: [
								{ label: 'Reference Frames & Initialization', slug: 'user-guide/reference-frames' },
								{ label: 'Dynamic Models',                    slug: 'user-guide/dynamic-models' },
								{ label: 'Disturbances',                      slug: 'user-guide/disturbances' },
								{ label: 'Solver Settings',                   slug: 'user-guide/solver-settings' },
							],
						},
					],
				},
				{
					label: 'PyRAMSES',
					items: [
						{ label: 'Overview',      slug: 'pyramses/overview' },
						{ label: 'Installation',  slug: 'pyramses/installation' },
						{ label: 'API Reference', slug: 'pyramses/api-reference' },
						{ label: 'Examples',      slug: 'pyramses/examples' },
					],
				},
				{
					label: 'Model Reference',
					items: [
						{ label: 'Synchronous Machine', slug: 'models/synchronous-machine' },
						{
							label: 'Exciters',
							items: [
								{ label: 'IEEE Exciters',    slug: 'models/ieee-exciters' },
								{ label: 'Custom Exciters',  slug: 'models/custom-exciters' },
							],
						},
						{
							label: 'Governors',
							items: [
								{ label: 'IEEE Governors',   slug: 'models/ieee-governors' },
								{ label: 'Custom Governors', slug: 'models/custom-governors' },
							],
						},
						{ label: 'Injectors',            slug: 'models/custom-injectors' },
						{ label: 'Two-Port Models',      slug: 'models/two-port-models' },
						{ label: 'Discrete Controllers', slug: 'models/discrete-controllers' },
					],
				},
				{
					label: 'Extending STEPSS',
					items: [
						{ label: 'User-Defined Models',    slug: 'developer/user-models' },
						{ label: 'CODEGEN Blocks Library', slug: 'developer/codegen-library' },
						{ label: 'CODEGEN Model Examples', slug: 'developer/codegen-examples' },
						{ label: 'URAMSES',                slug: 'developer/uramses' },
					],
				},
				{
					label: 'Analysis',
					items: [
						{ label: 'Eigenanalysis', slug: 'user-guide/eigenanalysis' },
					],
				},
				{
					label: 'Test Systems',
					items: [
						{ label: 'Nordic Test System', slug: 'test-systems/nordic' },
						{ label: '5-Bus Test System',  slug: 'test-systems/5bus' },
					],
				},
				{
					label: 'Reference',
					items: [
						{ label: 'Repositories', slug: 'resources/repositories' },
						{ label: 'References',   slug: 'resources/references' },
						{ label: 'License',      slug: 'getting-started/license' },
					],
				},
			],
		}),
	],
});
