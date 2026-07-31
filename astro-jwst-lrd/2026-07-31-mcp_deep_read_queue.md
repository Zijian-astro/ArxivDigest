# MCP Deep Read Queue - 2026-07-31

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2607.28278` - JWST's Constraints on the Substellar IMF in NGC 2024
- `2607.28501` - X-ray Absorption Variability in NGC 1142: Another Constraint on the Nature of the Torus/Broad-Line Region in Active Galactic Nuclei
- `2607.28510` - Uncertainty-Aware Tidal Disruption Event Classification : A Host-Agnostic Probabilistic Random Forest Approach
- `2607.27750` - PhySR: Physics-Informed Neural Network for Super-Resolution Reconstruction in Radio Synthesis Imaging
- `2607.28475` - DB-Bench: Benchmarking Deblenders for LSST DESC Using the Blending ToolKit