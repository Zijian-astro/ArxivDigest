# MCP Deep Read Queue - 2026-05-14

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2605.13472` - First Light And Reionization Epoch Simulations (FLARES) XXI: The UV Indices of Galaxies in the Early Universe
- `2605.13735` - A New PSF Deconvolution Algorithm: Simultaneous Spatial Resolution Enhancement and Point Source Removal for Morphological Analysis of AGN Host Galaxies
- `2605.13514` - COOL-LAMPS IX: A Rare Duo of Quasars Each Lensed by a Single Massive Galaxy Cluster
- `2605.13842` - From DES to KiDS: Domain adaptation for cross-survey detection of low-surface-brightness galaxies
- `2605.13843` - The Galaxy Luminosity Functions in ASTRID: Predictions for LSST