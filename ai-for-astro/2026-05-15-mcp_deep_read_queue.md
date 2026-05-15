# MCP Deep Read Queue - 2026-05-15

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2605.14306` - Towards Self-Evolving Agentic Literature Retrieval
- `2605.13874` - GEAR: Genetic AutoResearch for Agentic Code Evolution
- `2605.13950` - Collider-Bench: Benchmarking AI Agents with Particle Physics Analysis Reproduction
- `2605.14040` - Physics-R1: An Audited Olympiad Corpus and Recipe for Visual Physics Reasoning
- `2605.14212` - MetaAgent-X : Breaking the Ceiling of Automatic Multi-Agent Systems via End-to-End Reinforcement Learning