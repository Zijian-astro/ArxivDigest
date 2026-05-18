# MCP Deep Read Queue - 2026-05-18

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2605.15263` - On the quenching of LRD X-ray emission by both Compton-thick gas and high accretion rates
- `2605.15555` - A VLBA-resolved Jet Associated with Super-Eddington Accretion in a Radio-loud Quasar at $z=3.4$
- `2605.15712` - Early Emergence of Environmental Effects: Accelerated Galaxy Assembly in a z=2.96 Protocluster in the COSMOS Field
- `2605.15310` - Introducing the Lumina project: large-volume radiation-hydrodynamic simulations of the epochs of hydrogen and helium reionization
- `2605.15361` - Clumps in spiral galaxies at $z \lesssim 3$: Disentangling two spatial modes of star formation