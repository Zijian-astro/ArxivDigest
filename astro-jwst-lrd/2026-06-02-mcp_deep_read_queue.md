# MCP Deep Read Queue - 2026-06-02

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2606.00258` - OCEANS of Absorption: High-resolution NIRSpec Spectroscopy Reveals Diverse Balmer-line Absorption in Little Red Dots
- `2606.00205` - Ultraviolet diversity of Little Red Dots as a probe for direct-collapse black hole ages
- `2606.01603` - Signatures of Accreting Black Holes in Line Intensity Mapping
- `2606.00219` - 21cmEMUv3: a hybrid diffusion-LSTM emulator of 21cmFAST summary observables
- `2606.01496` - The Information Content of Quasar Variability Light Curves: How Well Can we Infer Stochastic Model Parameters?