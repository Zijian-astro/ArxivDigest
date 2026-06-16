# MCP Deep Read Queue - 2026-06-16

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2606.14869` - COSMOS-Web: A Multi-wavelength Morphological Catalog of ~780,000 Galaxies
- `2606.14959` - Probing Direct Contributions of Galaxies and AGN to Cosmic Reionization in a Quasar Field J0226+0302 with JWST NIRCam and NIRSpec
- `2606.16853` - Optically Invisible Galaxies at Cosmic Noon and beyond with JWST/UNCOVER
- `2606.15365` - PEARLS: NuSTAR and XMM-Newton Extragalactic Survey of the JWST North Ecliptic Pole Time Domain Field VI: Multiwavelength SED Analysis
- `2606.16012` - HYPERION. The cold ISM of rapidly growing $z>6$ quasars: diverse gas reservoirs, dust enrichment, and feedback signatures