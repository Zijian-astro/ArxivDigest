# MCP Deep Read Queue - 2026-05-15

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2605.13966` - Massive Galaxies Form Early and Gray: Stellar Assembly and Dust Attenuation at $\mathbf{z>3.5}$ from CAPERS
- `2605.14233` - A new sample of Little Red Dots at $z<0.45$ in DESI DR1: Broad Balmer lines, low ionization spectrum and no variability
- `2605.14922` - DREAMS. JWST Spectroscopy of a $z=8.3$ Galaxy with an ALMA Dust Continuum Detection: Early Dust, Very High $T_{\rm dust}$, and a Multi-wavelength [OIII] Ratio Discrepancy
- `2605.14313` - An Updated Characterization of Luminous Lyα emitters at the End of Reionization
- `2605.13967` - When galaxies burst: enhanced shot-noise for line-intensity mapping in the JWST era