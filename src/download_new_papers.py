# encoding: utf-8
import os
import tqdm
from bs4 import BeautifulSoup as bs
import urllib.request
import json
import datetime
import pytz
import re


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


def get_papers(field_abbr, limit=None):
    date = datetime.date.fromtimestamp(datetime.datetime.now(tz=pytz.timezone("America/New_York")).timestamp())
    date = date.strftime("%a, %d %b %y")
    data_path = f"./data/{field_abbr}_{date}.jsonl"
    if not os.path.exists(data_path):
        _download_new_papers(field_abbr)
    results = []
    with open(data_path, "r") as f:
        for i, line in enumerate(f.readlines()):
            if limit and i == limit:
                return results
            results.append(json.loads(line))
    if any(paper.get("main_page", "").rstrip("/") == "https://arxiv.org/abs" for paper in results):
        _download_new_papers(field_abbr)
        results = []
        with open(data_path, "r") as f:
            for i, line in enumerate(f.readlines()):
                if limit and i == limit:
                    return results
                results.append(json.loads(line))
    return results
