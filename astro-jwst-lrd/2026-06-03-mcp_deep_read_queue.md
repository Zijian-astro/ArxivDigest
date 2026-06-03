# MCP Deep Read Queue - 2026-06-03

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2606.02773` - Why Little Red Dots Disappear at z < 3: Evolution of Number Density and Halo Mass
- `2606.03037` - A $z \sim$ 6.2 Quasar on the Local M$_{\rm BH}$-$σ_{\rm \ast}$ Relation Quenching Its Host Galaxy from the Aether Survey
- `2606.03375` - Little Red Dot progenitors from Compact Starbursts: A Natural Path to Early AGN Formation
- `2606.03522` - The UV Side of Little Red Dots: Red, Compact, and Iron-Enhanced Rest-UV Emission with a Strong Downturn around Ly$α$
- `2606.03934` - Spectral Handling and Estimation of AGN Parameters (SHEAP), The first AGN fitting GPU-based code