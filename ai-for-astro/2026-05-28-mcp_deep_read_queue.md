# MCP Deep Read Queue - 2026-05-28

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2605.27499` - GenSBI: Generative Methods for Simulation-Based Inference in JAX
- `2605.27610` - Eliot: Interactively $\underline{E}$xploring Fast-Changing Scientific $\underline{Li}$terature Trends with $\underline{O}$nline Da$\underline{t}$a and Learning
- `2605.27760` - SkillGrad: Optimizing Agent Skills Like Gradient Descent
- `2605.28282` - ResearchLoop: An Evidence-Gated Control Plane for AI-Assisted Research
- `2605.28371` - From paper to benchmark: agentic, framework-based reproduction of under-specified methods in machine health intelligence