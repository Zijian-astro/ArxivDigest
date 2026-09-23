# MCP Deep Read Queue - 2026-09-23

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2609.25349` - Calcium Triplet Absorption is Common around Little Red Dots
- `2609.26553` - Constraining Inflation with Little Red Dots
- `2609.25886` - Rest-Frame UV and Optical Structural Evolution of Narrowband-Selected Lyman-alpha Emitters at z = 2-7 with JWST/NIRCam
- `2609.25224` - Gone with the wind? Potential gas inflow in the broad-line region of a QSO at $z=0.287$ traced by time-varying Balmer absorption
- `2609.26483` - Exploring the influence of reionisation-era galaxies on their local intergalactic medium using the Sherwood-Relics simulations