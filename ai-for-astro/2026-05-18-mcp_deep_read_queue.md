# MCP Deep Read Queue - 2026-05-18

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2605.15334` - From I/O to Code with Discovery Agent
- `2605.15470` - Njord: A Probabilistic Graph Neural Network for Ensemble Ocean Forecasting
- `2605.15913` - Towards Generalization of Block Attention via Automatic Segmentation and Block Distillation
- `2605.15959` - When and Why Adversarial Training Improves PINNs: A Neural Tangent Kernel Perspective
- `2605.15961` - Sparse Autoencoders enable Robust and Interpretable Fine-tuning of CLIP models