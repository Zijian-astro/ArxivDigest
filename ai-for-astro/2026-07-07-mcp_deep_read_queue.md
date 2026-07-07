# MCP Deep Read Queue - 2026-07-07

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2607.02927` - VideoSearcher: Empowering Video Deep Research with Multi-Tool Agentic Reasoning via Reinforcement Learning
- `2607.04108` - Dictionaries, Not Darwin: Set-Level Selection Beats LLM Evolution in Scientific Equation Discovery
- `2607.02574` - From Tensor Buffer to Distributed Memory Hierarchy: A Survey of KV Cache Management for LLM Serving
- `2607.02771` - Automated Data Readiness for Scientific AI
- `2607.02909` - Learning Taxonomic Trees with Hierarchical Representation Regularization for Large Multimodal Models