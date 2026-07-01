# MCP Deep Read Queue - 2026-07-01

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2606.30711` - Little Red Dots as Intermediate Mass, Super-Eddington Engines: Insights from Type IIn Supernovae and The 1837-1856 Great Eruption of $η$ Carinae
- `2606.30757` - Unveil the nature of JWST-AGN and Little Red Dots with SKAO continuum surveys
- `2606.30787` - JWST spectroscopy of galaxies at $z>10$: Damped Ly$α$ absorbers reveal efficient star formation and hidden redshift biases
- `2606.30802` - A Census of the 200 Most Massive Galaxies Spectroscopically Observed with JWST at zspec $\sim$3-15
- `2606.31312` - Dissecting the Obscured Core of GN20: an Active Galactic Nucleus Outshone by Young Stars