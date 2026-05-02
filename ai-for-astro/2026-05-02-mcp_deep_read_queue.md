# MCP Deep Read Queue - 2026-05-02

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2604.27092` - End-to-end autonomous scientific discovery on a real optical platform
- `2604.27221` - Web2BigTable: A Bi-Level Multi-Agent LLM System for Internet-Scale Information Search and Extraction
- `2604.27616` - RoadMapper: A Multi-Agent System for Roadmap Generation of Solving Complex Research Problems
- `2604.27996` - Exploring Interaction Paradigms for LLM Agents in Scientific Visualization
- `2604.28039` - SpecVQA: A Benchmark for Spectral Understanding and Visual Question Answering in Scientific Images