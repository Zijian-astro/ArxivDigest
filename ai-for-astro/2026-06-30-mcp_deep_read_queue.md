# MCP Deep Read Queue - 2026-06-30

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2606.29315` - Hierarchical Experimentalist Agents
- `2606.29746` - DEEPMED Search: An Open-Source Agentic Platform for Medical Deep Research with Introspective Verification
- `2606.28392` - RADIANT-PET: Reasoning-Augmented PET/CT Lesion Segmentation with Large Language Models and Reinforcement Learning
- `2606.28780` - Multimodal Graph RAG for Long-range Visually Rich Document Understanding
- `2606.28920` - ExACT: Exemplar-Driven Calibrated Refinement for Training-Free Visual Grounding in Remote Sensing Images