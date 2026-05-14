# MCP Deep Read Queue - 2026-05-14

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2605.13034` - ViDR: Grounding Multimodal Deep Research Reports in Source Visual Evidence
- `2605.13245` - It's not the Language Model, it's the Tool: Deterministic Mediation for Scientific Workflows
- `2605.13277` - Utility-Oriented Visual Evidence Selection for Multimodal Retrieval-Augmented Generation
- `2605.13551` - Mixed neural posterior estimation for simulators with discrete and continuous parameters
- `2605.13764` - VectorSmuggle: Steganographic Exfiltration in Embedding Stores and a Cryptographic Provenance Defense