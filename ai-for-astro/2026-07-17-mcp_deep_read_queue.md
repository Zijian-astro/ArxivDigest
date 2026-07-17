# MCP Deep Read Queue - 2026-07-17

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2607.14095` - HG-RAG: Hierarchy-Guided Retrieval-Augmented Generation for Structured Knowledge Graphs
- `2607.14327` - PReM: Learning What to Preserve and When to Refresh for Context Compression
- `2607.14561` - MARS: Multi-hop Adaptive Retrieval and SPARQL Generation for KGQA
- `2607.14777` - SEED: Self-Evolving On-Policy Distillation for Agentic Reinforcement Learning
- `2607.15079` - BrainPilot: Automating Brain Discovery with Agentic Research