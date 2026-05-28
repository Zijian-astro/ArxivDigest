# MCP Deep Read Queue - 2026-05-28

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2605.27481` - Astronomy Open Science Competence Centre in Europe
- `2605.27629` - The Celestial Reference Frame at K Band: The CRF-K-2025 Catalog
- `2605.28644` - Exploring non-Poisson satellite occupation in HOD models and its impact on 2- and 3-point galaxy clustering