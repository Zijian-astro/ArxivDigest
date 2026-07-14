# MCP Deep Read Queue - 2026-07-14

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2607.09806` - An Autonomous Scientific Knowledge Generation Framework for AI-Driven Scientific Discovery
- `2607.10463` - GRASP: GRanularity-Aware Search Policy for Agentic RAG
- `2607.11084` - NVAITC AI Scientist: A Governed End-to-End Research System -- A Hypertension GWAS Case Study
- `2607.11683` - RAGU: A Multi-Step GraphRAG Engine with a Compact Domain-Adapted LLM
- `2607.10789` - Imaging-101: Benchmarking LLM Coding Agents on Scientific Computational Imaging