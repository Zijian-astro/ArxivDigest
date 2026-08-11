# MCP Deep Read Queue - 2026-08-11

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2608.09813` - An emerging baryon cycle in a galaxy 500 million years after the Big Bang
- `2608.08203` - A New Window on the Hα Luminosity Function and Star Formation Rate Density from 1.2 < z < 6.6 from JWST Medium-Band Photometry
- `2608.08015` - Breathing Fire: Hot Dust in the Big Three Dragons at z = 7.15
- `2608.08369` - GATOS: Distinct Feedback Modes in AGN Central Regions Revealed by Spatially Resolved JWST Spectroscopy
- `2608.08275` - The Quasar Feedback Survey: Ionised Outflows in type 2 QSOs with MUSE data