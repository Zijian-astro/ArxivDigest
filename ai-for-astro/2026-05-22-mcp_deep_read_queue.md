# MCP Deep Read Queue - 2026-05-22

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2605.21825` - Toward AI VIS Co-Scientists: A General and End-to-End Agent Harness for Solving Complex Data Visualization Tasks
- `2605.22054` - LABO: LLM-Accelerated Bayesian Optimization through Broad Exploration and Selective Experimentation
- `2605.22343` - Sibyl-AutoResearch: Autonomous Research Needs Self-Evolving Trial-and-Error Harnesses, Not Paper Generators
- `2605.21491` - Teaching Language Models to Forecast Research Success Through Comparative Idea Evaluation
- `2605.21820` - Beyond Scalar Objectives: Expert-Feedback-Driven Autonomous Experimentation for Scientific Discovery at the Nanoscale