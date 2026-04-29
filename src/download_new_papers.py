# encoding: utf-8
import os
import tqdm
from bs4 import BeautifulSoup as bs
import urllib.request
import json
import datetime
import pytz
import re
import urllib.parse
import xml.etree.ElementTree as ET


ARXIV_API_URL = "https://export.arxiv.org/api/query"
ATOM_NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "arxiv": "http://arxiv.org/schemas/atom",
}

CATEGORY_CODES_BY_FIELD = {
    "astro-ph": [
        "astro-ph.GA",
        "astro-ph.CO",
        "astro-ph.EP",
        "astro-ph.HE",
        "astro-ph.IM",
        "astro-ph.SR",
    ],
    "cs": [
        "cs.AI",
        "cs.CL",
        "cs.CC",
        "cs.CE",
        "cs.CG",
        "cs.GT",
        "cs.CV",
        "cs.CY",
        "cs.CR",
        "cs.DS",
        "cs.DB",
        "cs.DL",
        "cs.DM",
        "cs.DC",
        "cs.ET",
        "cs.FL",
        "cs.GL",
        "cs.GR",
        "cs.AR",
        "cs.HC",
        "cs.IR",
        "cs.IT",
        "cs.LO",
        "cs.LG",
        "cs.MS",
        "cs.MA",
        "cs.MM",
        "cs.NI",
        "cs.NE",
        "cs.NA",
        "cs.OS",
        "cs.OH",
        "cs.PF",
        "cs.PL",
        "cs.RO",
        "cs.SI",
        "cs.SE",
        "cs.SD",
        "cs.SC",
        "cs.SY",
    ],
}

CODE_TO_SUBJECT = {
    "astro-ph.GA": "Astrophysics of Galaxies",
    "astro-ph.CO": "Cosmology and Nongalactic Astrophysics",
    "astro-ph.EP": "Earth and Planetary Astrophysics",
    "astro-ph.HE": "High Energy Astrophysical Phenomena",
    "astro-ph.IM": "Instrumentation and Methods for Astrophysics",
    "astro-ph.SR": "Solar and Stellar Astrophysics",
    "cs.AI": "Artificial Intelligence",
    "cs.CL": "Computation and Language",
    "cs.CC": "Computational Complexity",
    "cs.CE": "Computational Engineering, Finance, and Science",
    "cs.CG": "Computational Geometry",
    "cs.GT": "Computer Science and Game Theory",
    "cs.CV": "Computer Vision and Pattern Recognition",
    "cs.CY": "Computers and Society",
    "cs.CR": "Cryptography and Security",
    "cs.DS": "Data Structures and Algorithms",
    "cs.DB": "Databases",
    "cs.DL": "Digital Libraries",
    "cs.DM": "Discrete Mathematics",
    "cs.DC": "Distributed, Parallel, and Cluster Computing",
    "cs.ET": "Emerging Technologies",
    "cs.FL": "Formal Languages and Automata Theory",
    "cs.GL": "General Literature",
    "cs.GR": "Graphics",
    "cs.AR": "Hardware Architecture",
    "cs.HC": "Human-Computer Interaction",
    "cs.IR": "Information Retrieval",
    "cs.IT": "Information Theory",
    "cs.LO": "Logic in Computer Science",
    "cs.LG": "Machine Learning",
    "cs.MS": "Mathematical Software",
    "cs.MA": "Multiagent Systems",
    "cs.MM": "Multimedia",
    "cs.NI": "Networking and Internet Architecture",
    "cs.NE": "Neural and Evolutionary Computing",
    "cs.NA": "Numerical Analysis",
    "cs.OS": "Operating Systems",
    "cs.OH": "Other Computer Science",
    "cs.PF": "Performance",
    "cs.PL": "Programming Languages",
    "cs.RO": "Robotics",
    "cs.SI": "Social and Information Networks",
    "cs.SE": "Software Engineering",
    "cs.SD": "Sound",
    "cs.SC": "Symbolic Computation",
    "cs.SY": "Systems and Control",
}


def _clean_labeled_text(element, label):
    text = element.get_text(" ", strip=True)
    return re.sub(rf"^{label}:\s*", "", text).strip()


def _paper_number_from_dt(dt):
    abs_link = dt.find("a", href=re.compile(r"^/abs/"))
    if abs_link and abs_link.get("href"):
        return abs_link["href"].split("/abs/", 1)[1].strip()
    text_match = re.search(r"arXiv:([^\s]+)", dt.get_text(" ", strip=True))
    if text_match:
        return text_match.group(1)
    raise RuntimeError(f"Could not parse arXiv id from: {dt.get_text(' ', strip=True)}")


def _download_new_papers(field_abbr):
    NEW_SUB_URL = f'https://arxiv.org/list/{field_abbr}/new'  # https://arxiv.org/list/cs/new
    page = urllib.request.urlopen(NEW_SUB_URL)
    soup = bs(page, features="html.parser")
    content = soup.body.find("div", {'id': 'content'})

    # find the first h3 element in content
    h3 = content.find("h3").text   # e.g: New submissions for Wed, 10 May 23
    date = h3.replace("New submissions for", "").strip()

    dt_list = content.dl.find_all("dt")
    dd_list = content.dl.find_all("dd")
    arxiv_base = "https://arxiv.org/abs/"

    assert len(dt_list) == len(dd_list)
    new_paper_list = []
    for i in tqdm.tqdm(range(len(dt_list))):
        paper = {}
        paper_number = _paper_number_from_dt(dt_list[i])
        paper['main_page'] = arxiv_base + paper_number
        paper['pdf'] = arxiv_base.replace('abs', 'pdf') + paper_number

        paper['title'] = _clean_labeled_text(
            dd_list[i].find("div", {"class": "list-title mathjax"}),
            "Title",
        )
        paper['authors'] = _clean_labeled_text(
            dd_list[i].find("div", {"class": "list-authors"}),
            "Authors",
        )
        paper['subjects'] = _clean_labeled_text(
            dd_list[i].find("div", {"class": "list-subjects"}),
            "Subjects",
        )
        paper['abstract'] = dd_list[i].find("p", {"class": "mathjax"}).get_text(" ", strip=True)
        new_paper_list.append(paper)


    #  check if ./data exist, if not, create it
    if not os.path.exists("./data"):
        os.makedirs("./data")

    # save new_paper_list to a jsonl file, with each line as the element of a dictionary
    date = datetime.date.fromtimestamp(datetime.datetime.now(tz=pytz.timezone("America/New_York")).timestamp())
    date = date.strftime("%a, %d %b %y")
    with open(f"./data/{field_abbr}_{date}.jsonl", "w") as f:
        for paper in new_paper_list:
            f.write(json.dumps(paper) + "\n")


def _download_papers_for_date(field_abbr, target_date, max_results=500):
    query_date = datetime.datetime.strptime(target_date, "%Y-%m-%d")
    start = query_date.strftime("%Y%m%d0000")
    end = query_date.strftime("%Y%m%d2359")
    category_codes = CATEGORY_CODES_BY_FIELD.get(field_abbr, [field_abbr])
    category_query = " OR ".join(f"cat:{code}" for code in category_codes)
    search_query = f"({category_query}) AND submittedDate:[{start}+TO+{end}]"
    params = {
        "search_query": search_query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = ARXIV_API_URL + "?" + urllib.parse.urlencode(params, safe=":+()[]")
    with urllib.request.urlopen(url) as response:
        xml_text = response.read()

    root = ET.fromstring(xml_text)
    papers = []
    for entry in root.findall("atom:entry", ATOM_NS):
        id_text = entry.findtext("atom:id", default="", namespaces=ATOM_NS)
        paper_id = id_text.split("/abs/")[-1].strip()
        title = entry.findtext("atom:title", default="", namespaces=ATOM_NS)
        summary = entry.findtext("atom:summary", default="", namespaces=ATOM_NS)
        authors = [
            author.findtext("atom:name", default="", namespaces=ATOM_NS)
            for author in entry.findall("atom:author", ATOM_NS)
        ]
        codes = []
        for category in entry.findall("atom:category", ATOM_NS):
            term = category.get("term")
            if term and term not in codes:
                codes.append(term)
        subjects = "; ".join(
            f"{CODE_TO_SUBJECT.get(code, code)} ({code})" for code in codes
        )
        papers.append(
            {
                "main_page": f"https://arxiv.org/abs/{paper_id}",
                "pdf": f"https://arxiv.org/pdf/{paper_id}",
                "title": " ".join(title.split()),
                "authors": ", ".join(author for author in authors if author),
                "subjects": subjects,
                "abstract": " ".join(summary.split()),
            }
        )

    if not os.path.exists("./data"):
        os.makedirs("./data")
    with open(f"./data/{field_abbr}_{target_date}.jsonl", "w") as f:
        for paper in papers:
            f.write(json.dumps(paper) + "\n")


def _default_date_label():
    current_date = datetime.date.fromtimestamp(
        datetime.datetime.now(tz=pytz.timezone("America/New_York")).timestamp()
    )
    return current_date.strftime("%a, %d %b %y")


def get_papers(field_abbr, limit=None, target_date=None):
    date = target_date or _default_date_label()
    data_path = f"./data/{field_abbr}_{date}.jsonl"
    if not os.path.exists(data_path):
        if target_date:
            _download_papers_for_date(field_abbr, target_date)
        else:
            _download_new_papers(field_abbr)
    results = []
    with open(data_path, "r") as f:
        for i, line in enumerate(f.readlines()):
            if limit and i == limit:
                return results
            results.append(json.loads(line))
    if any(paper.get("main_page", "").rstrip("/") == "https://arxiv.org/abs" for paper in results):
        if target_date:
            _download_papers_for_date(field_abbr, target_date)
        else:
            _download_new_papers(field_abbr)
        results = []
        with open(data_path, "r") as f:
            for i, line in enumerate(f.readlines()):
                if limit and i == limit:
                    return results
                results.append(json.loads(line))
    return results
