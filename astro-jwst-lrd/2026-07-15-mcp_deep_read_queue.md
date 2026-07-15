# MCP Deep Read Queue - 2026-07-15

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2607.12016` - The onset of stellar bars at Cosmic Noon. Bar-driven quenching and AGN co-evolution in a mature disc galaxy
- `2607.12953` - Fast and accurate bandpass integration of complex SEDs with neural networks
- `2607.12018` - The JADES Transient Survey II: Volumetric Supernova Rates out to z~5
- `2607.12028` - The JADES Transient Survey III: Linking Core-Collapse Supernova Rates to Cosmic Star Formation
- `2607.12929` - The MAGPI survey: Stellar populations radial trends and mass assembly in star-forming galaxies at z~0.3