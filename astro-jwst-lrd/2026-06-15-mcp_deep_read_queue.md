# MCP Deep Read Queue - 2026-06-15

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2606.13819` - GA-NIFS: The interplay between feedback and star formation at 3 < z < 9 probed by JWST/NIRSpec IFU
- `2606.14643` - A new CIGALE module for modeling AGN emission lines
- `2606.13784` - The host halo masses of AGNs and quasars at $z \sim 3-7$ with TNG-Cluster, FLAMINGO and other cosmological galaxy simulations
- `2606.14477` - GATOS N: Extended circumnuclear dust emission in nearby Seyfert galaxies surveyed by JWST/MIRI
- `2606.13781` - CANUCS/Technicolor Data Release 2: A Catalogue of Galaxy Structural Parameters in up to 29 HST+JWST bands and a Multi-Wavelength Exploration of the Galaxy Size-Mass Relation at $0.6 < z \leq 4$