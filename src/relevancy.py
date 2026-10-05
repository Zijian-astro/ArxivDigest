"""
run:
python -m relevancy run_all_day_paper \
  --output_dir ./data \
  --model_name="gpt-3.5-turbo-16k" \
"""
import time
import json
import os
import random
import re
import string
from datetime import datetime
from pathlib import Path

import numpy as np
import tqdm
import utils


def encode_prompt(query, prompt_papers):
    """Encode multiple prompt instructions into a single string."""
    prompt = Path(__file__).with_name("relevancy_prompt.txt").read_text() + "\n"
    prompt += query['interest']
    if query.get("digest_guidance"):
        prompt += "\n\nAdditional digest guidance:\n"
        prompt += query["digest_guidance"]
    if query.get("selection_guidance"):
        prompt += "\n\nUser feedback selection guidance:\n"
        prompt += query["selection_guidance"]

    for idx, task_dict in enumerate(prompt_papers):
        (title, authors, abstract) = task_dict["title"], task_dict["authors"], task_dict["abstract"]
        if not title:
            raise
        prompt += f"###\n"
        prompt += f"{idx + 1}. Paper ID: {_paper_id(task_dict)}\n"
        prompt += f"{idx + 1}. Title: {title}\n"
        prompt += f"{idx + 1}. Authors: {authors}\n"
        prompt += f"{idx + 1}. Abstract: {abstract}\n"
    prompt += f"\n Generate response:\n1."
    print(prompt)
    return prompt


def _paper_id(paper):
    return paper["main_page"].rstrip("/").rsplit("/abs/", 1)[-1]


class RelevanceResponseError(ValueError):
    """The model did not return one identifiable score for every input paper."""


def post_process_chat_gpt_response(paper_data, response, threshold_score=8):
    selected_data = []
    if response is None:
        raise RelevanceResponseError("No model response")
    content = response['message']['content']
    import pprint
    try:
        score_items = extract_json_items(content)
    except Exception:
        pprint.pprint(content)
        raise RelevanceResponseError("No valid relevance JSON")
    pprint.pprint(score_items)
    if not all(isinstance(item, dict) for item in score_items):
        raise RelevanceResponseError("Scores must be JSON objects")
    if len(score_items) != len(paper_data):
        raise RelevanceResponseError(
            f"Expected {len(paper_data)} scores, received {len(score_items)}"
        )
    # A single-paper retry is unambiguous even if the model omits its ID.
    if len(paper_data) == 1 and not score_items[0].get("Paper ID"):
        score_items[0]["Paper ID"] = _paper_id(paper_data[0])
    items_by_id = {str(item.get("Paper ID", "")): item for item in score_items}
    expected_ids = {_paper_id(paper) for paper in paper_data}
    if len(items_by_id) != len(score_items) or set(items_by_id) != expected_ids:
        raise RelevanceResponseError("Missing, duplicate, or unexpected Paper ID")

    for paper in paper_data:
        inst = dict(items_by_id[_paper_id(paper)])
        try:
            score = int(str(inst["Relevancy score"]).split("/")[0])
        except (KeyError, ValueError, TypeError) as error:
            raise RelevanceResponseError("Invalid relevance score") from error
        if not 0 <= score <= 10:
            raise RelevanceResponseError("Relevance score outside 0-10")
        if score < threshold_score:
            continue
        inst["Relevancy score"] = score
        scored_paper = dict(paper)
        output_str = "Title: " + paper["title"] + "\n"
        output_str += "Authors: " + paper["authors"] + "\n"
        output_str += "Link: " + paper["main_page"] + "\n"
        for key, value in inst.items():
            scored_paper[key] = value
            output_str += str(key) + ": " + str(value) + "\n"
        scored_paper['summarized_text'] = output_str
        selected_data.append(scored_paper)
    return selected_data, False


def extract_json_items(content):
    cleaned = content.strip()
    cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        parsed = json.loads(cleaned)
        return parsed if isinstance(parsed, list) else [parsed]
    except json.JSONDecodeError:
        pass

    decoder = json.JSONDecoder()
    items = []
    index = 0
    while index < len(cleaned):
        match = re.search(r"\{", cleaned[index:])
        if not match:
            break
        start = index + match.start()
        try:
            item, end = decoder.raw_decode(cleaned[start:])
        except json.JSONDecodeError:
            index = start + 1
            continue
        if isinstance(item, dict) and any(
            key.lower() == "relevancy score" for key in item.keys()
        ):
            items.append(item)
        index = start + end

    if items:
        return items

    raise RuntimeError("No JSON objects with Relevancy score found")


def find_word_in_string(w, s):
    return re.compile(r"\b({0})\b".format(w), flags=re.IGNORECASE).search(s)


def process_subject_fields(subjects):
    all_subjects = subjects.split(";")
    all_subjects = [
        s.replace("Subjects:", "").strip().split(" (")[0].strip()
        for s in all_subjects
    ]
    return all_subjects

def generate_relevance_score(
    all_papers,
    query,
    model_name="gpt-3.5-turbo-16k",
    threshold_score=8,
    num_paper_in_prompt=4,
    temperature=0.4,
    top_p=1.0,
    sorting=True,
    min_results=0,
    max_results=None,
    max_tokens_per_paper=320,
    audit_data=None,
    positive_ids=None,
):
    ans_data = []
    request_idx = 1
    hallucination = False
    for id in tqdm.tqdm(range(0, len(all_papers), num_paper_in_prompt)):
        prompt_papers = all_papers[id:id+num_paper_in_prompt]
        # only sampling from the seed tasks
        prompt = encode_prompt(query, prompt_papers)

        decoding_args = utils.OpenAIDecodingArguments(
            temperature=temperature,
            n=1,
            max_tokens=max_tokens_per_paper*num_paper_in_prompt,
            top_p=top_p,
        )
        request_start = time.time()
        response = utils.openai_completion(
            prompts=prompt,
            model_name=model_name,
            batch_size=1,
            decoding_args=decoding_args,
            logit_bias={"100257": -100},  # prevent the <|endoftext|> from being generated
        )
        print ("response", response['message']['content'])
        request_duration = time.time() - request_start

        process_start = time.time()
        try:
            batch_data, hallu = post_process_chat_gpt_response(
                prompt_papers, response, threshold_score=0
            )
        except RelevanceResponseError as error:
            if len(prompt_papers) == 1:
                raise
            print(f"Incomplete batch ({error}); retrying each paper individually.")
            batch_data, _ = generate_relevance_score(
                prompt_papers, query, model_name=model_name, threshold_score=0,
                num_paper_in_prompt=1, temperature=temperature, top_p=top_p,
                sorting=False, max_tokens_per_paper=max_tokens_per_paper,
            )
            hallu = True
        hallucination = hallucination or hallu
        ans_data.extend(batch_data)

        print(f"Request {request_idx+1} took {request_duration:.2f}s")
        print(f"Post-processing took {time.time() - process_start:.2f}s")

    if sorting:
        ans_data = sorted(ans_data, key=lambda x: int(x["Relevancy score"]), reverse=True)

    all_scored = ans_data
    positive_ids = set(positive_ids or [])
    ans_data = [
        paper for index, paper in enumerate(all_scored)
        if paper["Relevancy score"] >= threshold_score or index < min_results
    ]
    if max_results:
        ans_data = ans_data[:max_results]
    selected_ids = {_paper_id(paper) for paper in ans_data}
    for paper in all_scored:
        base_id = re.sub(r"v\d+$", "", _paper_id(paper))
        if base_id in positive_ids:
            paper["feedback_priority"] = True
            if _paper_id(paper) not in selected_ids:
                ans_data.append(paper)
                selected_ids.add(_paper_id(paper))
        if audit_data is not None:
            row = dict(paper)
            row["selected"] = _paper_id(paper) in selected_ids
            row["selection_reason"] = (
                "user_positive_feedback" if base_id in positive_ids else
                "threshold" if paper["Relevancy score"] >= threshold_score and row["selected"] else
                "minimum_results" if row["selected"] else
                "result_limit" if paper["Relevancy score"] >= threshold_score else
                "below_threshold"
            )
            audit_data.append(row)
    if sorting:
        ans_data.sort(key=lambda paper: paper["Relevancy score"], reverse=True)
    
    return ans_data, hallucination

def run_all_day_paper(
    query={"interest":"", "subjects":["Computation and Language", "Artificial Intelligence"]},
    date=None,
    data_dir="../data",
    model_name="gpt-3.5-turbo-16k",
    threshold_score=8,
    num_paper_in_prompt=8,
    temperature=0.4,
    top_p=1.0
):
    if date is None:
        date = datetime.today().strftime('%a, %d %b %y')
        # string format such as Wed, 10 May 23
    print ("the date for the arxiv data is: ", date)

    all_papers = [json.loads(l) for l in open(f"{data_dir}/{date}.jsonl", "r")]
    print (f"We found {len(all_papers)}.")

    all_papers_in_subjects = [
        t for t in all_papers
        if bool(set(process_subject_fields(t['subjects'])) & set(query['subjects']))
    ]
    print(f"After filtering subjects, we have {len(all_papers_in_subjects)} papers left.")
    ans_data = generate_relevance_score(all_papers_in_subjects, query, model_name, threshold_score, num_paper_in_prompt, temperature, top_p)
    utils.write_ans_to_file(ans_data, date, output_dir="../outputs")
    return ans_data


if __name__ == "__main__":
    query = {"interest":"""
    1. Large language model pretraining and finetunings
    2. Multimodal machine learning
    3. Do not care about specific application, for example, information extraction, summarization, etc.
    4. Not interested in paper focus on specific languages, e.g., Arabic, Chinese, etc.\n""",
    "subjects":["Computation and Language"]}
    ans_data = run_all_day_paper(query)
