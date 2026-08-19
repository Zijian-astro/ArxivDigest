# MCP Deep Read Queue - 2026-08-19

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2608.17679` - Infrared Lines from Sterile-Neutrino Transition Magnetic Moments at JWST
- `2608.17570` - Dianoga simulations of galaxy clusters and groups: Properties of the baryonic components
- `2608.17526` - From Variability to SED Modeling: A Multiwavelength Study of the Neutrino Blazar TXS 0506+056
- `2608.17568` - NMMA-Astro-COLIBRI: An Automated Light-Curve Supernovae Classification Service in the Multi-Survey Era
- `2608.17680` - $R_{\rm e}$, or not $R_{\rm e}$: Developing $R_5\equiv R_{-2}$ as a scale radius for galaxy sizes, masses, and mass-to-light ratios