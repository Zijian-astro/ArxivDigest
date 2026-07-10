# MCP Deep Read Queue - 2026-07-10

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2607.07946` - DeepSWE: Measuring Frontier Coding Agents on Original, Long-Horizon Engineering Tasks
- `2607.07984` - Agentic Neural Architecture Search
- `2607.08233` - Playing ZendoWorld: Challenging AI Agents on Active Visual Concept Induction
- `2607.07962` - Beyond Thermal Imaging: Inferring Thermophysical Properties from Time-Resolved Thermal Observations
- `2607.07993` - Hallucination Self-Play: Bootstrapping Reinforced Detector via Evolved Generator