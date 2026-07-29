# MCP Deep Read Queue - 2026-07-29

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2607.24799` - Multimodal Hybrid Retrieval-Augmented Generation for Scientific Document Understanding using Open-Source SLMs
- `2607.24861` - HVM-GraphRAG: Holistic-View Multimodal Graph Retrieval-Augmented Generation on Complex Document
- `2607.25151` - HiEviDR-Bench: A Benchmark for Hierarchical Evidence Aggregation in Deep Research
- `2607.25818` - SepPrune:A Separator-based Pruning Framework for Efficient Multimodal Large Language Models
- `2607.24791` - From Naive RAG to Deep Agentic Retrieval: An Evolving Context Engineering Pipeline for Regulatory Compliance