# MCP Deep Read Queue - 2026-05-20

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2605.19661` - COSMOS-Web: Star formation along the early Hubble sequence and the evolution of dust over the redshift range 0<z<12
- `2605.18959` - Hyrax: An Extensible Framework for Rapid ML Experimentation and Unsupervised Discovery in the Era of Rubin, Roman, and Euclid
- `2605.20121` - Galaxy Proximate Damped Lyman-Alpha Systems and HI Reionization Topology in TECHNICOLOR DAWN
- `2605.18992` - Summary of Discussion Sessions from "The Dusty Universe 2025: The Fifth Pandust Conference"
- `2605.19241` - Active Galactic Nucleus Tori: Potential Birthplace to Millions of Planets