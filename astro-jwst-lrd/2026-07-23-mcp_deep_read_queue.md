# MCP Deep Read Queue - 2026-07-23

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2607.19491` - Rapid growth in a dual AGN during a gas-rich merger at z~4.5
- `2607.19471` - The first dusty galaxies across $6 \lesssim z \lesssim 14$: Blue monsters, red monsters, and the bimodality of dust content in early galaxies
- `2607.19640` - AGNFormer I: Reconstruction of AGN spectra using a probabilistic transformer model
- `2607.19970` - Nebular continuum in high-redshift galaxies with JWST
- `2607.19603` - AGN Feedback Models and AGN Demographics II: Comparing Predictions of Radiative and Total Feedback to Observations