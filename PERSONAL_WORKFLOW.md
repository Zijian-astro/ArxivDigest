# Personal arXiv Workflow

This fork is set up as the discovery half of a two-repo research workflow:

- `ArxivDigest` finds and ranks new arXiv papers.
- `arxiv-mcp-server` downloads and reads the full text of papers you choose to inspect.

## Daily Discovery

Edit these config files as your interests evolve:

- `personal_config.yaml`: main astronomy digest for JWST high-redshift galaxies, AGN, and little red dots.
- `personal_config_ai_astro.yaml`: supplemental computer-science digest for AI/LLM/LMM methods that may transfer to astronomy.

Run locally:

```bash
cd /Users/zijianzhang/Documents/Git/ArxivDigest
conda env create -f environment.yml
conda activate arxiv-digest
cp .env.template .env
python src/action.py --config personal_config.yaml
```

If the environment already exists, skip `conda env create -f environment.yml` and just activate it.

Set `DEEPSEEK_API_KEY` in `.env`. Add SendGrid or SMTP secrets only if you want email delivery.

The personal configs use:

```yaml
provider: "deepseek"
model: "deepseek-chat"
```

If you later want to switch a config back to OpenAI, set `provider: "openai"`, choose an OpenAI model, and provide `OPENAI_API_KEY`.

For Gmail SMTP delivery, set:

```bash
MAIL_USERNAME=your.email@gmail.com
MAIL_PASSWORD=your_google_app_password
TO_EMAIL=recipient@example.com
```

Then send a local test email:

```bash
python src/send_smtp_test.py
```

Run the AI-for-astronomy supplement with:

```bash
python src/action.py --config personal_config_ai_astro.yaml
```

## Outputs

Each run writes:

- `digest.html`: email/browser version.
- `outputs/astro-jwst-lrd/`: main astronomy digest output.
- `outputs/ai-for-astro/`: supplemental AI-for-astronomy digest output.

The GitHub Action now runs both configs every day at 12:00 Beijing time and uploads separate artifacts for each.

It also deploys the generated HTML dashboards to GitHub Pages. In your GitHub fork, enable:

```text
Settings -> Pages -> Build and deployment -> Source: GitHub Actions
```

After a successful run, the Pages URL is shown in the `deploy_pages` job summary.

## Deep Reading With MCP

Configure your MCP client using:

```text
/Users/zijianzhang/Documents/Git/arxiv-mcp-server/personal_mcp_config.json
```

Then paste the suggested prompt from one of the `mcp_deep_read_queue.md` files into Codex, Claude, or another MCP-capable client. The MCP server will cache downloaded papers in:

```text
/Users/zijianzhang/Documents/Git/arxiv-papers
```

That gives you a durable local paper library for later `read_paper`, `list_papers`, and semantic search workflows.
