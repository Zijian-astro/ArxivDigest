# MCP Deep Read Queue - 2026-08-27

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2608.25341` - A systematic study of AGN feedback in a disk galaxy using MACER. III. High Gas Fractions in AGN Hosts
- `2608.25552` - Energy Partition in AGN-driven Bubbles of NGC 4438: From Nuclear Bubbles to a Galaxy-scale Outflow
- `2608.25571` - Energetics of AGN Feedback
- `2608.25111` - CCAT: The Prime-Cam Instrument for the Fred Young Submillimeter Telescope -- Overview and Status
- `2608.25364` - Recovering the effective impact parameters in integral-field absorption-line tomography