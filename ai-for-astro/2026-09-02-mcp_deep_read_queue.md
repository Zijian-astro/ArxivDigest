# MCP Deep Read Queue - 2026-09-02

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2609.00065` - Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents
- `2609.01294` - Explore Before Committing: Hypothesis-Guided Search for Deep Research Agents
- `2609.00231` - Beyond Language Priors: Diagnosing and Fixing Visual-Origin Hallucinations in Multimodal LLM
- `2609.00689` - SCoNE: Selective Context-aware Neuron Editing for Robust Retrieval-Augmented Generation
- `2609.01289` - Agentic Multimodal Models for Environmental Hyperspectral Unmixing