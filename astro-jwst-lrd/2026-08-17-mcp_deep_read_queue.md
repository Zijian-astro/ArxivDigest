# MCP Deep Read Queue - 2026-08-17

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2608.14023` - The galaxies' energy balance problem solved
- `2608.13640` - Laser Metrology for Precision Alignment of Transmission Gratings in the REDSoX Soft X-ray Polarimeter