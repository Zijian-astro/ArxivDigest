from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content

from datetime import date

import argparse
import html
import json
import yaml
import os
import re
from pathlib import Path
from dotenv import load_dotenv
import openai
from relevancy import generate_relevance_score, process_subject_fields
from download_new_papers import get_papers
from smtp_mailer import load_smtp_settings, send_email


PLACEHOLDER_ENV_VALUES = {
    "",
    "your_api_key",
    "your_deepseek_api_key",
    "your_openai_api_key",
    "your_email",
}


def get_configured_env(name):
    value = os.environ.get(name, "").strip()
    if value in PLACEHOLDER_ENV_VALUES or value.startswith("your_"):
        return None
    return value


# Hackathon quality code. Don't judge too harshly.
# Feel free to submit pull requests to improve the code.

topics = {
    "Physics": "",
    "Mathematics": "math",
    "Computer Science": "cs",
    "Quantitative Biology": "q-bio",
    "Quantitative Finance": "q-fin",
    "Statistics": "stat",
    "Electrical Engineering and Systems Science": "eess",
    "Economics": "econ",
}

physics_topics = {
    "Astrophysics": "astro-ph",
    "Condensed Matter": "cond-mat",
    "General Relativity and Quantum Cosmology": "gr-qc",
    "High Energy Physics - Experiment": "hep-ex",
    "High Energy Physics - Lattice": "hep-lat",
    "High Energy Physics - Phenomenology": "hep-ph",
    "High Energy Physics - Theory": "hep-th",
    "Mathematical Physics": "math-ph",
    "Nonlinear Sciences": "nlin",
    "Nuclear Experiment": "nucl-ex",
    "Nuclear Theory": "nucl-th",
    "Physics": "physics",
    "Quantum Physics": "quant-ph",
}


# TODO: surely theres a better way
category_map = {
    "Astrophysics": [
        "Astrophysics of Galaxies",
        "Cosmology and Nongalactic Astrophysics",
        "Earth and Planetary Astrophysics",
        "High Energy Astrophysical Phenomena",
        "Instrumentation and Methods for Astrophysics",
        "Solar and Stellar Astrophysics",
    ],
    "Condensed Matter": [
        "Disordered Systems and Neural Networks",
        "Materials Science",
        "Mesoscale and Nanoscale Physics",
        "Other Condensed Matter",
        "Quantum Gases",
        "Soft Condensed Matter",
        "Statistical Mechanics",
        "Strongly Correlated Electrons",
        "Superconductivity",
    ],
    "General Relativity and Quantum Cosmology": ["None"],
    "High Energy Physics - Experiment": ["None"],
    "High Energy Physics - Lattice": ["None"],
    "High Energy Physics - Phenomenology": ["None"],
    "High Energy Physics - Theory": ["None"],
    "Mathematical Physics": ["None"],
    "Nonlinear Sciences": [
        "Adaptation and Self-Organizing Systems",
        "Cellular Automata and Lattice Gases",
        "Chaotic Dynamics",
        "Exactly Solvable and Integrable Systems",
        "Pattern Formation and Solitons",
    ],
    "Nuclear Experiment": ["None"],
    "Nuclear Theory": ["None"],
    "Physics": [
        "Accelerator Physics",
        "Applied Physics",
        "Atmospheric and Oceanic Physics",
        "Atomic and Molecular Clusters",
        "Atomic Physics",
        "Biological Physics",
        "Chemical Physics",
        "Classical Physics",
        "Computational Physics",
        "Data Analysis, Statistics and Probability",
        "Fluid Dynamics",
        "General Physics",
        "Geophysics",
        "History and Philosophy of Physics",
        "Instrumentation and Detectors",
        "Medical Physics",
        "Optics",
        "Physics and Society",
        "Physics Education",
        "Plasma Physics",
        "Popular Physics",
        "Space Physics",
    ],
    "Quantum Physics": ["None"],
    "Mathematics": [
        "Algebraic Geometry",
        "Algebraic Topology",
        "Analysis of PDEs",
        "Category Theory",
        "Classical Analysis and ODEs",
        "Combinatorics",
        "Commutative Algebra",
        "Complex Variables",
        "Differential Geometry",
        "Dynamical Systems",
        "Functional Analysis",
        "General Mathematics",
        "General Topology",
        "Geometric Topology",
        "Group Theory",
        "History and Overview",
        "Information Theory",
        "K-Theory and Homology",
        "Logic",
        "Mathematical Physics",
        "Metric Geometry",
        "Number Theory",
        "Numerical Analysis",
        "Operator Algebras",
        "Optimization and Control",
        "Probability",
        "Quantum Algebra",
        "Representation Theory",
        "Rings and Algebras",
        "Spectral Theory",
        "Statistics Theory",
        "Symplectic Geometry",
    ],
    "Computer Science": [
        "Artificial Intelligence",
        "Computation and Language",
        "Computational Complexity",
        "Computational Engineering, Finance, and Science",
        "Computational Geometry",
        "Computer Science and Game Theory",
        "Computer Vision and Pattern Recognition",
        "Computers and Society",
        "Cryptography and Security",
        "Data Structures and Algorithms",
        "Databases",
        "Digital Libraries",
        "Discrete Mathematics",
        "Distributed, Parallel, and Cluster Computing",
        "Emerging Technologies",
        "Formal Languages and Automata Theory",
        "General Literature",
        "Graphics",
        "Hardware Architecture",
        "Human-Computer Interaction",
        "Information Retrieval",
        "Information Theory",
        "Logic in Computer Science",
        "Machine Learning",
        "Mathematical Software",
        "Multiagent Systems",
        "Multimedia",
        "Networking and Internet Architecture",
        "Neural and Evolutionary Computing",
        "Numerical Analysis",
        "Operating Systems",
        "Other Computer Science",
        "Performance",
        "Programming Languages",
        "Robotics",
        "Social and Information Networks",
        "Software Engineering",
        "Sound",
        "Symbolic Computation",
        "Systems and Control",
    ],
    "Quantitative Biology": [
        "Biomolecules",
        "Cell Behavior",
        "Genomics",
        "Molecular Networks",
        "Neurons and Cognition",
        "Other Quantitative Biology",
        "Populations and Evolution",
        "Quantitative Methods",
        "Subcellular Processes",
        "Tissues and Organs",
    ],
    "Quantitative Finance": [
        "Computational Finance",
        "Economics",
        "General Finance",
        "Mathematical Finance",
        "Portfolio Management",
        "Pricing of Securities",
        "Risk Management",
        "Statistical Finance",
        "Trading and Market Microstructure",
    ],
    "Statistics": [
        "Applications",
        "Computation",
        "Machine Learning",
        "Methodology",
        "Other Statistics",
        "Statistics Theory",
    ],
    "Electrical Engineering and Systems Science": [
        "Audio and Speech Processing",
        "Image and Video Processing",
        "Signal Processing",
        "Systems and Control",
    ],
    "Economics": ["Econometrics", "General Economics", "Theoretical Economics"],
}


def _paper_id_from_url(url):
    match = re.search(r"arxiv\.org/abs/([^?#]+)", url or "")
    return match.group(1) if match else ""


def _normalize_paper(paper):
    normalized = dict(paper)
    normalized["arxiv_id"] = _paper_id_from_url(normalized.get("main_page", ""))
    return normalized


def _inspection_items(paper):
    return _as_list(
        paper.get("Full-text inspection checklist")
        or paper.get("Key figures to inspect")
    )


def generate_digest(
    topic,
    categories,
    interest,
    threshold,
    model_name="gpt-4o-mini",
    target_date=None,
    min_papers=0,
    max_papers=None,
    digest_guidance="",
    max_tokens_per_paper=320,
):
    if topic == "Physics":
        raise RuntimeError("You must choose a physics subtopic.")
    elif topic in physics_topics:
        abbr = physics_topics[topic]
    elif topic in topics:
        abbr = topics[topic]
    else:
        raise RuntimeError(f"Invalid topic {topic}")
    if categories:
        for category in categories:
            if category not in category_map[topic]:
                raise RuntimeError(f"{category} is not a category of {topic}")
        papers = get_papers(abbr, target_date=target_date)
        papers = [
            t
            for t in papers
            if bool(set(process_subject_fields(t["subjects"])) & set(categories))
        ]
    else:
        papers = get_papers(abbr, target_date=target_date)
    if interest:
        relevancy, hallucination = generate_relevance_score(
            papers,
            query={"interest": interest, "digest_guidance": digest_guidance},
            threshold_score=threshold,
            model_name=model_name,
            num_paper_in_prompt=16,
            min_results=min_papers,
            max_results=max_papers,
            max_tokens_per_paper=max_tokens_per_paper,
        )
        relevancy = [_normalize_paper(paper) for paper in relevancy]
        body = "<br><br>".join(
            [
                f'Title: <a href="{paper["main_page"]}">{paper["title"]}</a><br>Authors: {paper["authors"]}<br>arXiv ID: {paper["arxiv_id"]}<br>Score: {paper["Relevancy score"]}<br>Reason: {paper.get("Reasons for match", "")}<br>Short digest: {paper.get("Short digest", "")}<br>Full-text inspection checklist: {"; ".join(_inspection_items(paper))}'
                for paper in relevancy
            ]
        )
        if hallucination:
            body = (
                "Warning: the model hallucinated some papers. We have tried to remove them, but the scores may not be accurate.<br><br>"
                + body
            )
        selected_papers = relevancy
    else:
        papers = [_normalize_paper(paper) for paper in papers]
        body = "<br><br>".join(
            [
                f'Title: <a href="{paper["main_page"]}">{paper["title"]}</a><br>Authors: {paper["authors"]}<br>arXiv ID: {paper["arxiv_id"]}'
                for paper in papers
            ]
        )
        selected_papers = papers
        hallucination = False
    return body, selected_papers, hallucination


def generate_body(topic, categories, interest, threshold):
    body, _, _ = generate_digest(topic, categories, interest, threshold)
    return body


def configure_llm_provider(config):
    provider = config.get("provider", "openai").lower()
    if provider == "deepseek":
        api_key = get_configured_env("DEEPSEEK_API_KEY")
        if not api_key:
            raise RuntimeError("No DeepSeek API key found. Set DEEPSEEK_API_KEY.")
        openai.api_key = api_key
        openai.api_base = config.get(
            "api_base",
            os.environ.get("DEEPSEEK_API_BASE", "https://api.deepseek.com/v1"),
        )
        return config.get("model", config.get("openai_model", "deepseek-chat"))

    if provider == "openai":
        api_key = get_configured_env("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("No OpenAI API key found. Set OPENAI_API_KEY.")
        openai.api_key = api_key
        if os.environ.get("OPENAI_API_BASE"):
            openai.api_base = os.environ["OPENAI_API_BASE"]
        return config.get("model", config.get("openai_model", "gpt-4o-mini"))

    raise RuntimeError(f"Unsupported provider: {provider}")


def write_digest_outputs(body, papers, config, output_dir="outputs", digest_date=None):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    today = digest_date or date.today().isoformat()
    digest = {
        "generated_on": today,
        "topic": config["topic"],
        "categories": config["categories"],
        "threshold": config["threshold"],
        "interest": config.get("interest", ""),
        "papers": papers,
    }

    (output_path / "digest.html").write_text(body, encoding="utf-8")
    (output_path / "digest.json").write_text(
        json.dumps(digest, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    markdown_lines = [
        f"# Personalized arXiv Digest - {today}",
        "",
        f"Topic: {config['topic']}",
        f"Categories: {', '.join(config['categories']) if config['categories'] else 'All'}",
        f"Threshold: {config['threshold']}",
        "",
    ]
    for index, paper in enumerate(papers, start=1):
        score = paper.get("Relevancy score", "n/a")
        reason = paper.get("Reasons for match", "")
        markdown_lines.extend(
            [
                f"## {index}. {paper['title']}",
                "",
                f"- arXiv ID: `{paper.get('arxiv_id', '')}`",
                f"- Authors: {paper['authors']}",
                f"- Score: {score}",
                f"- Link: {paper['main_page']}",
                f"- PDF: {paper['pdf']}",
                f"- Subjects: {paper['subjects']}",
            ]
        )
        if reason:
            markdown_lines.append(f"- Reason: {reason}")
        short_digest = paper.get("Short digest", "")
        if short_digest:
            markdown_lines.extend(["", "Short digest:", short_digest])
        key_items = _inspection_items(paper)
        if key_items:
            markdown_lines.extend(["", "Full-text inspection checklist:"])
            markdown_lines.extend([f"- {item}" for item in key_items])
        markdown_lines.append("")
    (output_path / "digest.md").write_text("\n".join(markdown_lines), encoding="utf-8")
    rendered_page = render_digest_page(digest)
    (output_path / "index.html").write_text(rendered_page, encoding="utf-8")
    (output_path / f"{today}.html").write_text(rendered_page, encoding="utf-8")

    top_k = int(config.get("top_k_for_deep_read", 5))
    queue_lines = [
        f"# MCP Deep Read Queue - {today}",
        "",
        "Use this with arxiv-mcp-server. For each paper you care about, ask your MCP client to:",
        "",
        "1. call `download_paper` with the arXiv ID",
        "2. call `read_paper`",
        "3. summarize, compare, or build a literature review",
        "",
        "Suggested prompt:",
        "",
        "> Please deep-read the papers below with arxiv-mcp-server. Download missing papers, read their full text, then produce: problem, method, main contribution, implementation idea, and whether I should follow up.",
        "",
    ]
    for paper in papers[:top_k]:
        queue_lines.append(f"- `{paper.get('arxiv_id', '')}` - {paper['title']}")
    (output_path / "mcp_deep_read_queue.md").write_text(
        "\n".join(queue_lines), encoding="utf-8"
    )

    return {
        "html": output_path / "digest.html",
        "json": output_path / "digest.json",
        "markdown": output_path / "digest.md",
        "queue": output_path / "mcp_deep_read_queue.md",
        "web": output_path / "index.html",
        "dated_web": output_path / f"{today}.html",
    }


def _as_list(value):
    if not value:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [line.strip("- ").strip() for line in str(value).splitlines() if line.strip()]


def render_digest_page(digest):
    papers = digest["papers"]
    title = f"{digest['topic']} arXiv Digest - {digest['generated_on']}"
    cards = []
    for paper in papers:
        score = html.escape(str(paper.get("Relevancy score", "n/a")))
        reason = html.escape(str(paper.get("Reasons for match", "")))
        short_digest = html.escape(str(paper.get("Short digest", "")))
        key_items = _inspection_items(paper)
        key_html = "".join(f"<li>{html.escape(item)}</li>" for item in key_items)
        cards.append(
            f"""
            <article class="paper-card" data-score="{score}">
              <div class="paper-meta">
                <span class="score">{score}</span>
                <span>{html.escape(paper.get("arxiv_id", ""))}</span>
              </div>
              <h2>{html.escape(paper["title"])}</h2>
              <p class="authors">{html.escape(paper["authors"])}</p>
              <div class="links">
                <a href="{html.escape(paper["main_page"])}">arXiv</a>
                <a href="{html.escape(paper["pdf"])}">PDF</a>
              </div>
              <section>
                <h3>Short Digest</h3>
                <p>{short_digest}</p>
              </section>
              <section>
                <h3>Reason</h3>
                <p>{reason}</p>
              </section>
              <section>
                <h3>Full-Text Inspection Checklist</h3>
                <ul>{key_html}</ul>
              </section>
              <details>
                <summary>Abstract</summary>
                <p>{html.escape(paper.get("abstract", ""))}</p>
              </details>
            </article>
            """
        )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f7f7f4;
      --ink: #1e2528;
      --muted: #5f6b70;
      --line: #d9dedb;
      --accent: #096b72;
      --accent-2: #8a4b22;
      --card: #ffffff;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--bg);
      color: var(--ink);
      line-height: 1.5;
    }}
    header {{
      padding: 28px clamp(18px, 4vw, 48px) 18px;
      border-bottom: 1px solid var(--line);
      background: #fff;
      position: sticky;
      top: 0;
      z-index: 2;
    }}
    h1 {{ margin: 0 0 8px; font-size: clamp(24px, 3vw, 38px); }}
    .subtitle {{ color: var(--muted); margin: 0; }}
    main {{
      width: min(1120px, calc(100% - 32px));
      margin: 24px auto 56px;
      display: grid;
      gap: 16px;
    }}
    .toolbar {{
      display: flex;
      gap: 12px;
      align-items: center;
      flex-wrap: wrap;
      padding: 12px 0;
    }}
    input {{
      min-width: min(420px, 100%);
      flex: 1;
      padding: 10px 12px;
      border: 1px solid var(--line);
      border-radius: 6px;
      font: inherit;
      background: #fff;
    }}
    .paper-card {{
      background: var(--card);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 20px;
      box-shadow: 0 1px 2px rgba(0,0,0,.04);
    }}
    .paper-meta {{
      display: flex;
      gap: 10px;
      align-items: center;
      color: var(--muted);
      font-size: 14px;
    }}
    .score {{
      display: inline-grid;
      place-items: center;
      min-width: 34px;
      height: 28px;
      border-radius: 4px;
      background: var(--accent);
      color: #fff;
      font-weight: 700;
    }}
    h2 {{ margin: 12px 0 6px; font-size: 21px; line-height: 1.25; }}
    h3 {{ margin: 18px 0 6px; font-size: 13px; text-transform: uppercase; color: var(--accent-2); }}
    .authors {{ color: var(--muted); margin: 0 0 10px; }}
    .links {{ display: flex; gap: 14px; margin: 8px 0 4px; }}
    a {{ color: var(--accent); font-weight: 650; text-decoration-thickness: 1px; }}
    ul {{ margin: 6px 0 0 20px; padding: 0; }}
    details {{ margin-top: 16px; color: var(--muted); }}
    summary {{ cursor: pointer; color: var(--ink); }}
  </style>
</head>
<body>
  <header>
    <h1>{html.escape(title)}</h1>
    <p class="subtitle">{len(papers)} papers selected. Categories: {html.escape(", ".join(digest["categories"]))}</p>
  </header>
  <main>
    <div class="toolbar">
      <input id="search" type="search" placeholder="Filter by title, abstract, AGN, LRD, JWST, author...">
    </div>
    <section id="papers">
      {"".join(cards)}
    </section>
  </main>
  <script>
    const search = document.getElementById('search');
    const cards = [...document.querySelectorAll('.paper-card')];
    search.addEventListener('input', () => {{
      const q = search.value.toLowerCase();
      for (const card of cards) {{
        card.style.display = card.innerText.toLowerCase().includes(q) ? '' : 'none';
      }}
    }});
  </script>
</body>
</html>"""


if __name__ == "__main__":
    # Load the .env file.
    load_dotenv()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config", help="yaml config file to use", default="config.yaml"
    )
    parser.add_argument(
        "--date",
        help="arXiv submission date to digest in YYYY-MM-DD format. Defaults to today's arXiv /new page.",
        default=None,
    )
    args = parser.parse_args()
    with open(args.config, "r") as f:
        config = yaml.safe_load(f)

    topic = config["topic"]
    categories = config["categories"]
    from_email = get_configured_env("FROM_EMAIL")
    to_email = get_configured_env("TO_EMAIL")
    threshold = config["threshold"]
    interest = config["interest"]
    model_name = configure_llm_provider(config)
    body, papers, hallucination = generate_digest(
        topic,
        categories,
        interest,
        threshold,
        model_name=model_name,
        target_date=args.date,
        min_papers=int(config.get("min_papers", 0)),
        max_papers=config.get("max_papers"),
        digest_guidance=config.get("digest_guidance", ""),
        max_tokens_per_paper=int(config.get("max_tokens_per_paper", 320)),
    )
    with open("digest.html", "w") as f:
        f.write(body)
    output_files = write_digest_outputs(
        body,
        papers,
        config,
        output_dir=config.get("output_dir", "outputs"),
        digest_date=args.date,
    )
    if hallucination:
        print("Warning: model hallucination cleanup was triggered.")
    print("Wrote personalized outputs:")
    for name, path in output_files.items():
        print(f"- {name}: {path}")
    sendgrid_api_key = get_configured_env("SENDGRID_API_KEY")
    if sendgrid_api_key and from_email and to_email:
        sg = SendGridAPIClient(api_key=sendgrid_api_key)
        from_email = Email(from_email)  # Change to your verified sender
        to_email = To(to_email)
        subject = date.today().strftime("Personalized arXiv Digest, %d %b %Y")
        content = Content("text/html", body)
        mail = Mail(from_email, to_email, subject, content)
        mail_json = mail.get()

        # Send an HTTP POST request to /mail/send
        response = sg.client.mail.send.post(request_body=mail_json)
        if response.status_code >= 200 and response.status_code <= 300:
            print("Send test email: Success!")
        else:
            print("Send test email: Failure ({response.status_code}, {response.text})")
    else:
        smtp_settings = load_smtp_settings()
        if smtp_settings:
            send_email(
                subject=date.today().strftime("Personalized arXiv Digest, %d %b %Y"),
                html_body=body,
                text_body="Your personalized arXiv digest is attached as HTML.",
                settings=smtp_settings,
            )
            print(f"SMTP email sent to {smtp_settings.to_email}")
        else:
            print("Email settings incomplete. Skipping email")
