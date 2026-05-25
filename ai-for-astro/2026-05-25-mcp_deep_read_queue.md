# MCP Deep Read Queue - 2026-05-25

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2605.22834` - Query-Adaptive Semantic Chunking for Retrieval-Augmented Generation: A Dynamic Strategy with Contextual Window Expansion
- `2605.22866` - BOHM: Zero-Cost Hierarchical Attribution for Compound AI Systems
- `2605.23070` - Flow Mismatching: Unsupervised Anomaly Detection via Velocity Discrepancies in Flow Matching Models
- `2605.23504` - VACE: Learning Geometrically Structured Representations for Time Series Anomaly Detection
- `2605.23754` - LLM-driven design of physics-constrained constitutive models: two agents are better than one