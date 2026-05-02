# MCP Deep Read Queue - 2026-05-02

Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:

1. call `download_paper` with the arXiv ID
2. call `read_paper`
3. summarize, compare, or build a literature review

Suggested prompt:

> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.

- `2604.27071` - Chaotic Molecular Gas in Five Dusty Star-forming Galaxies in the Spiderweb Protocluster at $z = 2.16$
- `2604.27056` - The First Empirical Calibration of the MIR Abundance Diagnostic Ne$_{23}$ with JWST
- `2604.27065` - Dwarf Galaxies Hosting Extreme Star-Forming Regions and (Variable) AGNs at Radio Wavelengths
- `2604.27159` - Molecular Outflows in the Nucleus of the Nearby Compton-thick AGN NGC 3079
- `2604.27301` - Turbulence and Star Formation Suppression in Elliptical Galaxies: The Role of Active Galactic Nucleus Jet Wind Interaction