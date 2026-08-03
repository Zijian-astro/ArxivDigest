# MCP Deep Read Queue - 2026-08-03

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2607.29589` - A Massive Galaxy at the Edge of Feedback-Free Efficiency
- `2607.28875` - Determining Total Infrared Luminosities from Submm Measurements of High Redshift Galaxies
- `2607.29075` - Reincarnations of massive stars in active galactic nucleus discs
- `2607.28704` - Understanding constraints on primordial mass black holes made of dark matter using fast radio bursts
- `2607.29335` - Maximising the mid-infrared high-contrast performance of ELT/METIS despite water vapour seeing