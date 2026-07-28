# MCP Deep Read Queue - 2026-07-28

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2607.22835` - Unsupervised selection and characterisation of Little Red Dots in JWST surveys with manifold learning
- `2607.22966` - A quasar hatching from a buried red phase at z = 3.7
- `2607.22834` - Reionization driven by the few: the ionizing budget of galaxies at z=5-10 from JWST/NIRSpec
- `2607.23020` - PhotoIFU: NIRCam as a Photometric Integral Field Unit for Mapping Feedback in Galaxies
- `2607.23062` - HETDEX: Star Formation Stochasticity Diagram of Lyman Alpha Emitting Galaxies at Cosmic Noon Confirms Three Archetypes