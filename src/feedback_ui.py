"""Shared static feedback form for daily pages and the digest homepage."""

import html
import json


def render_feedback_form(repository, digest_date="", revision=None):
    """Render a form that opens an owner-submitted GitHub feedback issue.

    Parameters
    ----------
    repository : str
        GitHub owner/repository receiving feedback.
    digest_date : str, optional
        Date of the digest being inspected.
    revision : int, optional
        Strategy revision used when generating this page.

    Returns
    -------
    str
        Standalone HTML fragment with scoped styles and JavaScript.
    """
    if not repository:
        return ""
    config = json.dumps({"repository": repository, "digest_date": digest_date}).replace("<", "\\u003c")
    version = f"本页筛选策略：v{revision}。" if revision is not None else ""
    history_url = f"https://github.com/{repository}/issues?q=is%3Aissue+%5Bdigest-feedback%5D"
    return r"""
<section class="feedback-panel" aria-labelledby="feedback-heading">
  <style>
    .feedback-panel { padding: 20px; margin: 18px 0; border: 1px solid #d9dedb; border-radius: 8px; background: #fff; }
    .feedback-panel h2 { margin: 0 0 10px; font-size: 21px; }
    .feedback-panel label { display: block; margin: 10px 0 5px; font-weight: 650; }
    .feedback-panel input, .feedback-panel textarea { box-sizing: border-box; display: block; width: 100%; min-width: 0; padding: 10px; border: 1px solid #b9c5c2; border-radius: 6px; font: inherit; }
    .feedback-panel button { margin-top: 12px; padding: 10px 14px; border: 0; border-radius: 6px; background: #096b72; color: #fff; font: inherit; cursor: pointer; }
    .feedback-panel p { color: #5f6b70; }
    #feedback-error { color: #a12828; }
  </style>
  <h2 id="feedback-heading">标记漏选论文</h2>
  <p>输入论文链接，并说明你为什么想看它。点击按钮后，在 GitHub 点击 Create 完成提交；AI 随后学习补充筛选规则，并在 Issue 回复结果，下一次筛选使用新策略。</p>
  <p>VERSION <a href="HISTORY_URL">查看反馈和学习结果</a></p>
  <form id="feedback-form">
    <label for="feedback-paper">arXiv 链接或 ID</label>
    <input id="feedback-paper" required placeholder="https://arxiv.org/abs/2608.25021v1" autocomplete="off">
    <label for="feedback-note">为什么这篇论文值得选入？（选填）</label>
    <textarea id="feedback-note" rows="3" maxlength="1500" placeholder="例如：高红移 compact blue broad-line emitters 与 LRD 的物理联系也是我的研究重点。"></textarea>
    <label for="feedback-date">漏选的 digest 日期（选填）</label>
    <input id="feedback-date" type="date" value="DIGEST_DATE">
    <button type="submit">在 GitHub 提交漏选反馈</button>
    <p id="feedback-error" role="status" aria-live="polite"></p>
  </form>
</section>
<script>
(() => {
  const config = FEEDBACK_CONFIG;
  const form = document.getElementById('feedback-form');
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const error = document.getElementById('feedback-error');
    error.textContent = '';
    let id = document.getElementById('feedback-paper').value.trim();
    if (id.includes('://')) {
      try {
        const url = new URL(id);
        if (!['https:', 'http:'].includes(url.protocol) || url.host !== 'arxiv.org' || !/^\/(abs|pdf)\//.test(url.pathname)) throw new Error();
        id = url.pathname.replace(/^\/(abs|pdf)\//, '').replace(/\/$/, '');
      } catch (_) {
        error.textContent = '请输入 arxiv.org 的 abs/PDF 链接，或 arXiv ID。';
        return;
      }
    }
    id = id.replace(/^arxiv:\s*/i, '').replace(/\.pdf$/, '').replace(/v\d+$/, '');
    if (!/^(\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?\/\d{7})$/.test(id)) {
      error.textContent = 'arXiv ID 格式不正确，例如 2608.25021。';
      return;
    }
    const payload = {
      arxiv_id: id,
      note: document.getElementById('feedback-note').value.trim(),
      digest_date: document.getElementById('feedback-date').value,
    };
    const body = '<!-- arxiv-digest-feedback -->\n```json\n' + JSON.stringify(payload, null, 2) + '\n```\n\n由个人 arXiv digest 网站提交。';
    const issue = new URL('https://github.com/' + config.repository + '/issues/new');
    issue.searchParams.set('title', '[digest-feedback] 漏选 ' + id);
    issue.searchParams.set('body', body);
    window.location.assign(issue.href);
  });
})();
</script>
""".replace("FEEDBACK_CONFIG", config).replace("VERSION", html.escape(version)).replace(
        "HISTORY_URL", html.escape(history_url, quote=True)
    ).replace("DIGEST_DATE", html.escape(digest_date, quote=True))
