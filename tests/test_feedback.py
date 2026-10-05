import io
import hashlib
import json
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import action
import download_new_papers
import feedback
import relevancy
from feedback_ui import render_feedback_form


def paper(paper_id, subjects="Astrophysics of Galaxies (astro-ph.GA)"):
    return {"title": "JWST source " + paper_id, "authors": "Test Author",
            "abstract": "High-redshift compact source spectroscopy.", "subjects": subjects,
            "main_page": "https://arxiv.org/abs/" + paper_id,
            "pdf": "https://arxiv.org/pdf/" + paper_id}


def response(*items):
    return {"message": {"content": json.dumps(list(items))}}


def score(paper_id, value):
    return {"Paper ID": paper_id, "Relevancy score": value, "Reasons for match": "Test reason"}


class ScoringTests(unittest.TestCase):
    def test_reordered_response_is_matched_by_id(self):
        papers = [paper("2608.25021v1"), paper("2608.25022v1")]
        result, _ = relevancy.post_process_chat_gpt_response(
            papers, response(score("2608.25022v1", "4/10"), score("2608.25021v1", 9)), 0
        )
        self.assertEqual([item["Relevancy score"] for item in result], [9, 4])
        self.assertNotIn("Relevancy score", papers[0])

    def test_missing_and_duplicate_response_ids_fail(self):
        papers = [paper("2608.25021"), paper("2608.25022")]
        for result in [response(score("2608.25021", 9)),
                       response(score("2608.25021", 9), score("2608.25021", 8))]:
            with self.subTest(result=result), self.assertRaises(relevancy.RelevanceResponseError):
                relevancy.post_process_chat_gpt_response(papers, result, 0)

    def test_incomplete_batch_retries_all_inputs_and_records_rejections(self):
        papers = [paper("2608.25021"), paper("2608.25022")]
        audit = []
        with patch("relevancy.utils.openai_completion", side_effect=[
            response(score("2608.25021", 9)), response(score("2608.25021", 9)),
            response(score("2608.25022", 3)),
        ]) as llm:
            selected, recovered = relevancy.generate_relevance_score(
                papers, {"interest": "JWST"}, audit_data=audit,
            )
        self.assertTrue(recovered)
        self.assertEqual(llm.call_count, 3)
        self.assertEqual(len(selected), 1)
        self.assertEqual(len(audit), 2)
        self.assertEqual(audit[1]["selection_reason"], "below_threshold")

    def test_failed_single_retry_stops_instead_of_dropping_paper(self):
        with patch("relevancy.utils.openai_completion", return_value=response()):
            with self.assertRaises(relevancy.RelevanceResponseError):
                relevancy.generate_relevance_score([paper("2608.25021")], {"interest": "JWST"})

    def test_known_positive_survives_threshold_and_cap_without_changing_score(self):
        papers = [paper("2608.25021v1"), paper("2608.25022")]
        audit = []
        with patch("relevancy.utils.openai_completion", return_value=response(
            score("2608.25021v1", 5), score("2608.25022", 9)
        )):
            selected, _ = relevancy.generate_relevance_score(
                papers, {"interest": "JWST"}, positive_ids={"2608.25021"},
                max_results=1, audit_data=audit,
            )
        self.assertEqual(len(selected), 2)
        self.assertEqual(selected[1]["Relevancy score"], 5)
        self.assertEqual(audit[1]["selection_reason"], "user_positive_feedback")

    def test_category_exclusions_are_audited(self):
        papers = [paper("2608.25021"), paper("2608.25022", "Solar and Stellar Astrophysics (astro-ph.SR)")]
        audit = []
        with patch("action.get_papers", return_value=papers), patch(
            "relevancy.utils.openai_completion", return_value=response(score("2608.25021", 9))
        ):
            action.generate_digest("Astrophysics", ["Astrophysics of Galaxies"],
                                   "JWST", 7, audit_data=audit)
        self.assertEqual({row["selection_reason"] for row in audit}, {"category_excluded", "threshold"})


class FeedbackTests(unittest.TestCase):
    def setUp(self):
        self.example = dict(paper("2608.25021"), arxiv_id="2608.25021", user_note="Include BLEs")
        self.state = {"schema_version": 1, "revision": 1, "rules": ["Prioritize JWST"],
                      "examples": [self.example]}

    def test_normalizes_versions_urls_and_legacy_ids(self):
        for value in ["2608.25021v1", "https://arxiv.org/abs/2608.25021v2?x=1",
                      "https://arxiv.org/pdf/2608.25021v1.pdf", "arXiv:2608.25021"]:
            self.assertEqual(feedback.normalize_arxiv_id(value), "2608.25021")
        self.assertEqual(feedback.normalize_arxiv_id("astro-ph/0601001v2"), "astro-ph/0601001")
        for value in ["https://evil.example/abs/2608.25021", "https://arxiv.org.evil/abs/2608.25021",
                      "https://arxiv.org/list/astro-ph/new", "../etc/passwd"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                feedback.normalize_arxiv_id(value)

    def test_parses_unicode_and_backticks_in_reason(self):
        payload = {"arxiv_id": "2608.25021v1", "note": "蓝色 BLE ``` 也相关", "digest_date": "2026-10-04"}
        issue = {"title": "[digest-feedback] 漏选", "body": feedback.FEEDBACK_MARKER
                 + "\n```json\n" + json.dumps(payload) + "\n```"}
        result = feedback.parse_feedback_issue(issue)
        self.assertEqual(result["note"], payload["note"])
        self.assertEqual(result["arxiv_id"], "2608.25021")

    def test_failed_learning_retains_original_strategy(self):
        original = json.dumps(self.state, sort_keys=True)
        with patch("feedback.utils.openai_completion", return_value={"message": {
            "content": json.dumps({"rules": ["Include blue broad-line sources"]})
        }}), patch("relevancy.generate_relevance_score", return_value=([
            dict(self.example, **{"Relevancy score": 4})
        ], False)):
            with self.assertRaises(RuntimeError):
                feedback.learn_strategy(self.state, self.example, {"interest": "JWST", "threshold": 7}, "deepseek-chat")
        self.assertEqual(json.dumps(self.state, sort_keys=True), original)

    def test_successful_learning_records_validation_and_replaces_same_example(self):
        with patch("feedback.utils.openai_completion", return_value={"message": {
            "content": json.dumps({"rules": ["Include blue broad-line sources"]})
        }}), patch("relevancy.generate_relevance_score", return_value=([
            dict(self.example, **{"Relevancy score": 9})
        ], False)):
            state = feedback.learn_strategy(self.state, dict(self.example, user_note="Updated"),
                                            {"interest": "JWST", "threshold": 7}, "deepseek-chat")
        self.assertEqual(state["revision"], 2)
        self.assertEqual(len(state["examples"]), 1)
        self.assertEqual(state["validation"]["positive_scores"], {"2608.25021": 9})

    def test_missing_remote_file_on_existing_branch_does_not_reset_strategy(self):
        missing = urllib.error.HTTPError("url", 404, "not found", {}, None)
        with patch("feedback._github_api", side_effect=[missing, {"ref": "refs/heads/digest-feedback"}]):
            with self.assertRaises(RuntimeError):
                feedback._remote_state("owner/repo")

    def test_backlog_includes_other_owner_feedback_but_skips_duplicates_and_strangers(self):
        def issue(number, owner="owner"):
            return {"number": number, "user": {"login": owner}, "title": "[digest-feedback] paper",
                    "body": feedback.FEEDBACK_MARKER + '\n```json\n{"arxiv_id":"2608.25021","note":"wanted"}\n```'}
        with patch("feedback._github_api", return_value=[issue(1), issue(2), issue(3, "stranger")]):
            pending = list(feedback._pending_feedback("owner/repo", self.state, issue(2)))
        self.assertEqual([row[0]["number"] for row in pending], [1])

    def test_old_feedback_for_same_paper_is_not_relearned_after_newer_feedback(self):
        old_payload = {"arxiv_id": "2608.25021", "note": "Old reason", "digest_date": ""}
        fingerprint = hashlib.sha256(json.dumps(old_payload, sort_keys=True).encode()).hexdigest()
        self.state["processed_feedback"] = {"1": fingerprint}
        old_issue = {"number": 1, "user": {"login": "owner"}, "title": "[digest-feedback] paper",
                     "body": feedback.FEEDBACK_MARKER + '\n```json\n' + json.dumps(old_payload) + '\n```'}
        with patch("feedback._github_api", return_value=[old_issue]):
            pending = list(feedback._pending_feedback("owner/repo", self.state, old_issue))
        self.assertEqual(pending, [])

    def test_full_outputs_include_audit_and_strategy_revision(self):
        with tempfile.TemporaryDirectory() as directory:
            files = action.write_digest_outputs("body", [self.example],
                {"topic": "Astrophysics", "categories": [], "threshold": 7,
                 "feedback_repository": "owner/repo"}, directory, "2026-10-05", self.state,
                [dict(self.example, selected=True, selection_reason="user_positive_feedback")])
            audit = json.loads(files["audit"].read_text())
            self.assertEqual(audit["strategy_revision"], 1)
            self.assertIn("feedback-form", files["web"].read_text())
            self.assertIn("本页筛选策略：v1", files["web"].read_text())


class DownloadTests(unittest.TestCase):
    def test_new_listing_includes_crosslists_but_not_replacements(self):
        def listing(paper_id):
            return f'''<dl><dt><a href="/abs/{paper_id}">arXiv:{paper_id}</a></dt><dd>
              <div class="list-title mathjax">Title: JWST</div>
              <div class="list-authors">Authors: A</div>
              <div class="list-subjects">Subjects: Astrophysics of Galaxies (astro-ph.GA)</div>
              <p class="mathjax">Abstract</p></dd></dl>'''
        page = '<body><div id="content"><h3>Showing new listings for Monday, 5 October 2026</h3>'
        page += listing("2608.25021").replace('<dl>', '<dl><h3>New submissions</h3>')
        page += listing("2608.25022").replace('<dl>', '<dl><h3>Cross submissions</h3>')
        page += listing("2608.25023").replace('<dl>', '<dl><h3>Replacement submissions</h3>') + '</div></body>'
        with tempfile.TemporaryDirectory() as directory, patch(
            "download_new_papers._urlopen_with_retry", return_value=io.BytesIO(page.encode())
        ), patch("download_new_papers.os.makedirs"), patch("download_new_papers.os.path.exists", return_value=True), patch(
            "download_new_papers.open", unittest.mock.mock_open(), create=True
        ) as output:
            download_new_papers._download_new_papers("astro-ph")
        written = ''.join(call.args[0] for call in output().write.call_args_list)
        self.assertIn("2608.25021", written)
        self.assertIn("2608.25022", written)
        self.assertNotIn("2608.25023", written)


if __name__ == "__main__":
    unittest.main()
