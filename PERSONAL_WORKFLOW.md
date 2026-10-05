# Personal arXiv Workflow

This fork is set up as the discovery half of a two-repo research workflow:

- `ArxivDigest` finds and ranks new arXiv papers.
- `arxiv-mcp-server` downloads and reads the full text of papers you choose to inspect.

## Daily Discovery

Edit these config files as your interests evolve:

- `personal_config.yaml`: main astronomy digest for JWST high-redshift galaxies, AGN, and little red dots.
- `personal_config_ai_astro.yaml`: supplemental computer-science digest for AI/LLM/LMM methods that may transfer to astronomy. Its daily schedule is currently paused; the config and historical pages remain available.

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

Run a historical arXiv submission date with:

```bash
python src/action.py --config personal_config.yaml --date 2026-04-28
```

The astronomy config keeps at least 7 papers by score, even if fewer than 7 pass the preferred relevance threshold. The AI supplement keeps 5–8 papers.

## Missed-Paper Feedback

On the Pages homepage or a newly generated astronomy digest, use **标记漏选论文**:

1. Paste an arXiv abstract/PDF URL or ID and optionally explain why you want it included.
2. Optionally enter the date of the digest that missed it.
3. The website opens a prefilled GitHub Issue. Sign in as the repository owner and click **Create** to submit it.
4. `Learn astro paper feedback` fetches the paper's title and abstract, asks the configured LLM to distill supplementary selection rules, and scores all stored positive examples against the existing threshold. It permits one rule-repair attempt; a failed check retains the previous strategy.
5. The Action replies in the Issue with the new rules and strategy revision. The next digest run loads them automatically. Learning starts on submission and takes an Action run; it does not instantly rewrite an already generated digest.

The repository owner's feedback alone can update this personal strategy. The learning workflow sends the existing research interests, feedback notes, and public paper metadata to the configured provider (currently DeepSeek), using the existing API secret. Each update uses one rule-generation request plus scoring requests for the stored positive examples; a repair can repeat this work. Repeating unchanged feedback does not call the LLM again.

`feedback/astro.json` on the default branch is the initial strategy. It includes the owner-reported positive `2608.25021`, with explicit initial guidance about compact blue broad-line emitters and their connection to LRDs. These initial rules were derived from the reported paper's abstract and have not been validated by a live model run. Learned revisions live on the separate `digest-feedback` branch, preserving the hand-written interests in `personal_config.yaml`. After a learned revision exists, changing the default-branch seed does not overwrite the saved strategy.

For local runs, sync the latest learned state first if desired:

```bash
GITHUB_REPOSITORY=Zijian-astro/ArxivDigest GITHUB_TOKEN=your_token python src/feedback.py sync
python src/action.py --config personal_config.yaml
```

The website stores no API keys or GitHub tokens. Feedback is stored in repository Issues and strategy history, so it has the repository's visibility. Editing a submitted Issue updates that paper's feedback; closing an Issue does not retract the saved positive example.

Learned rules are appended to the original scoring prompt. Categories, thresholds, and quotas are unchanged for ordinary papers. Explicitly marked positives are retained when they occur in the fetched list, even if their category or score would normally exclude them; the original score and override reason remain visible in the audit. With a configured result cap, this override can increase the selected count beyond the cap. Similar unseen papers are judged by the updated LLM prompt: passing known-positive checks does not establish future recall or prevent every omission.

Batch scoring now requires identifiable results for every candidate. Missing, duplicated, or mismatched replies trigger individual retries; an unsuccessful retry fails the run rather than silently dropping a paper. Daily discovery includes new submissions and cross-lists, but still excludes replacements. This can increase the number of candidates and selected papers.

Each run writes `selection_audit.json` containing fetched candidates, scores and reasons, selection decisions, category exclusions, configuration, and strategy revision. It is included in the Action artifact and published as `<date>-selection_audit.json` alongside each daily page. This distinguishes a paper absent from the fetched list from one rejected by categories, score, or the result cap. Historical runs created before this change do not have this audit.

Run the offline regression checks with:

```bash
python -m unittest discover -s tests
```

## Outputs

Each run writes:

- `digest.html`: email/browser version.
- `outputs/astro-jwst-lrd/`: main astronomy digest output.
- `outputs/ai-for-astro/`: supplemental AI-for-astronomy digest output.
- `selection_audit.json`: full selection decisions inside each digest output folder.

The GitHub Action runs only the astronomy config Monday-Friday at 12:00 Beijing time. To temporarily run the AI supplement too, use **Run workflow → include_ai**; its default is false. Local AI runs remain available.

It also deploys the generated HTML dashboards to GitHub Pages and preserves historical daily pages on the `gh-pages` branch. In your GitHub fork, enable:

```text
Settings -> Pages -> Build and deployment -> Source: Deploy from a branch
Branch: gh-pages
Folder: / (root)
```

After a successful run, your public page will be available at the repository's GitHub Pages URL.

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
