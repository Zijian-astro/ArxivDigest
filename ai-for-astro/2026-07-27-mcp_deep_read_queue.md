# MCP Deep Read Queue - 2026-07-27

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2607.21596` - FlowEvo: Self-Evolving Agents through the Co-Evolution of Workflows and Executable Skills
- `2607.21692` - Learning What Matters: Supervising Sparse Attention Routing with Causal Evidence Sets
- `2607.21673` - Self-Poisoning in Adaptive Out-of-Distribution Detection: A Sharp-Threshold Theory and Certified Label-Free Calibration
- `2607.22319` - Towards Trustworthy and Cost-Efficient Data Integration: From Naïve RAG to Agentic RAG
- `2607.22375` - IDEAgent: Agentic Quality-Diversity Search for Research Idea Generation