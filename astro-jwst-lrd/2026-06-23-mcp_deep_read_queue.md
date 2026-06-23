# MCP Deep Read Queue - 2026-06-23

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2606.21614` - Little Red and Blue Dots: AGN-excited narrow lines, Lyman-$α$ emission, and resemblance to standard quasars
- `2606.20800` - No hidden monsters: Probing recently-quenched galaxies for obscured AGN with JWST-PRIMER MIRI and NIRCam
- `2606.20845` - LEGGOS I: The JWST LEGGOS Survey -- LEnsing and Galaxy Growth: Observing Substructures -- Unpacks the Nature of Clumpy Star Formation and Quenching in Gravitationally Lensed Galaxies beyond Cosmic Noon
- `2606.20801` - LEGGOS III: Mapping Star Formation and Dust in Gravitationally Lensed Galaxies with $\textit{SUMAC}$, a UMAP and Clustering Framework
- `2606.22758` - Black Hole Occupation Fraction: Dependence on Black Hole Mass Threshold, Environment, Resolution and Redshift