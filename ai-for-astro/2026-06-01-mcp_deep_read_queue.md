# MCP Deep Read Queue - 2026-06-01

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2605.30434` - LongDS-Bench: On the Failure of Long-Horizon Agentic Data Analysis
- `2605.30961` - EvoGens: A Population-Based Heuristic Search Framework for Scientific Idea Generation
- `2605.31584` - LongTraceRL: Learning Long-Context Reasoning from Search Agent Trajectories with Rubric Rewards
- `2605.30407` - Exploring Autonomous Agentic Data Engineering for Model Specialization
- `2605.30790` - On the impact of retrieved content representations in RAG Pipelines