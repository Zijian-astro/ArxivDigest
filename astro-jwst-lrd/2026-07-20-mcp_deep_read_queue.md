# MCP Deep Read Queue - 2026-07-20

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2607.15357` - Non-Thermal Physics Drives Compact, Self-Regulated Galaxy Morphologies at Cosmic Dawn
- `2607.15344` - The Azahar Project: Non-Thermal Physics Drives Star Formation Burstiness and the Evolution of the UV Luminosity Density at Cosmic Dawn
- `2607.15515` - Gas-Phase Metallicity and Nitrogen Abundances in Low-Mass Galaxies Down to $M_\star\simeq10^{5.7}\,M_\odot$ at $z\simeq4.5$--$10.1$ from JWST Lensing Cluster Surveys
- `2607.15341` - Forest without Trees is still Fruitful: Constraints on the thermal state of the neutral IGM at $z\approx5.6$ with the 21-cm forest power spectrum
- `2607.15359` - Observations of X-ray quasi-periodic eruptions