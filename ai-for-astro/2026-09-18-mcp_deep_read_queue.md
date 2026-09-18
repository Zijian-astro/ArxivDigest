# MCP Deep Read Queue - 2026-09-18

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2609.19644` - ScientistTwo: Pioneering the Human Knowledge Frontier with Autonomous AI
- `2609.19417` - Less Is More: Graph-free Multimodal RAG via Multi-signal Late Fusion
- `2609.19437` - Bayesian Optimization with Rich Auxiliary Information via LLMs
- `2609.19601` - FootprintRAG: Visual Analytics for Evidence Context Refinement in RAG-based Scientific Literature Exploration
- `2609.19634` - Scientific Image Quality Assessment via Multi-modal Retrieval-Augmented Generation