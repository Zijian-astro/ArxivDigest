# MCP Deep Read Queue - 2026-05-22

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2605.21574` - (LRDs)$^2$: The Low-ReDshift Little Red Dots Survey. II. DESI DR1 Sample
- `2605.21589` - A Magnetized Black Hole Envelope Model for Little Red Dots
- `2605.21599` - JWST Advanced Deep Extragalactic Survey (JADES) Data Release 5: stellar population catalogue for galaxies in GOODS-N and GOODS-S
- `2605.22161` - Blue-tilted Runnings and the JWST Early Galaxy Tension
- `2605.22162` - Spectra as Language: Large Language Models for Scalable Stellar Parameter and Abundance Inference