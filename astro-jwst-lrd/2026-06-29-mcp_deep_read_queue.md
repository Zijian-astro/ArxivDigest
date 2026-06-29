# MCP Deep Read Queue - 2026-06-29

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2606.27468` - JWST Reveals Compact Nuclear Starbursts Masquerading as AGNs in Metal-Poor Dwarfs: Where Are the Accreting Intermediate-Mass Black Holes?
- `2606.27427` - SEEDZ: Rapid Galaxy Assembly as a Pathway to Supermassive Stars, Dense Stellar Environments and Massive Black Hole Seeds
- `2606.28296` - Memoirs of the curvaton: non-perturbative non-Gaussianity and supermassive primordial black holes
- `2606.28311` - Kinematic detection of dusty outflows from AGN: PAH kinematics of type 2 quasars with JWST/MIRI spectroscopy
- `2606.27426` - Too shy to spin? Cosmic wallflowers as proto-globular clusters