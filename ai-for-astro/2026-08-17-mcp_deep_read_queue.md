# MCP Deep Read Queue - 2026-08-17

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2608.13940` - AI Research Preference Models
- `2608.14372` - Catching the Imposter: Self-Supervised Learning of Physical Coherence with Cross-Entity Feature Permutations
- `2608.14407` - The Past and Future of AI Scientists
- `2608.13608` - Evaluating Agentic Learning Harness Capabilities Without Labels via the Scaling Hypothesis
- `2608.13889` - Consensus-gated Multi-Agent Neural Architecture Search for Seismic Fault Segmentation