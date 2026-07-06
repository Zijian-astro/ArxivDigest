# MCP Deep Read Queue - 2026-07-06

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2607.02329` - Grounded autonomous research: a fault-tolerant LLM pipeline from corpus to manuscript in frontier computational physics
- `2607.01431` - IsoSci: A Benchmark of Isomorphic Cross-Domain Science Problems for Evaluating Reasoning versus Knowledge Retrieval in LLMs
- `2607.02020` - Hidden Forgetting in Continual Multimodal Learning: When Accuracy Survives but Grounding Fails
- `2607.02262` - CheckRLM: Effective Knowledge-Thought Coherence Checking in Retrieval-Augmented Reasoning
- `2607.02301` - InvSplat: Inverse Feed-Forward Scene Splatting