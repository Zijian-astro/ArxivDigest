# MCP Deep Read Queue - 2026-05-08

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2605.05673` - Detection of an Extended Ly$α$ Halo around a $\textit{z}=6.64$ Broad Absorption Line Quasar with the Keck Cosmic Web Imager
- `2605.05298` - Kinematic Stratification in Extremely Red Quasars Revealed by JWST
- `2605.05327` - Shape of Direct-Method Mass-Metallicity Relation with JWST: Fast-Track Nitrogen and Helium Enrichment
- `2605.05573` - AstroAlertBench: Evaluating the Accuracy, Reasoning, and Honesty of Multimodal LLMs in Astronomical Classification
- `2605.05318` - HOLISMOKES XXI: Detecting strongly lensed type Ia supernovae from time series of multi-band LSST-like imaging data -- Part II