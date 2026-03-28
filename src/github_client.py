"""
github_client.py — All GitHub API interactions via PyGithub + httpx.

Responsibilities:
  • Verify HMAC-SHA256 webhook signatures
  • Fetch unified diff + full file sources for a PR
  • Post findings as a single batched inline PR review
"""

import hmac
import logging
from hashlib import sha256

import httpx
from github import Github, GithubException

from src.config import GITHUB_TOKEN, GITHUB_WEBHOOK_SECRET

log = logging.getLogger(__name__)


def verify_signature(payload: bytes, sig_header: str) -> bool:
    """
    Validate the GitHub webhook HMAC-SHA256 signature.
    Returns True (skip check) when GITHUB_WEBHOOK_SECRET is not configured —
    useful for local development but must be set in production.
    """
    if not GITHUB_WEBHOOK_SECRET:
        log.warning("Webhook secret not set — skipping signature verification")
        return True
    expected = "sha256=" + hmac.new(
        GITHUB_WEBHOOK_SECRET.encode(), payload, sha256
    ).hexdigest()
    return hmac.compare_digest(expected, sig_header or "")


def fetch_pr_data(repo_full_name: str, pr_number: int) -> tuple[str, dict[str, str]]:
    """
    Fetch the raw unified diff and full source of every changed .py file.

    Why full source (not just the patch)?
      The AST parser needs the complete file to build a syntax tree and extract
      whole function/class bodies. Sending only the patch would break the tree.
      The full source is fetched once here; the parser then discards ~95% of it,
      keeping only the semantically relevant chunks.

    Returns:
        (diff_text, {filename: full_source_code})
    """
    gh = Github(GITHUB_TOKEN)
    repo = gh.get_repo(repo_full_name)
    pr = repo.get_pull(pr_number)

    # PyGithub doesn't expose the raw diff directly — fetch via REST
    with httpx.Client(timeout=30, follow_redirects=True) as client:
        resp = client.get(
            pr.diff_url,
            headers={"Authorization": f"token {GITHUB_TOKEN}"},
        )
        resp.raise_for_status()
        diff_text = resp.text

    file_contents: dict[str, str] = {}
    for pr_file in pr.get_files():
        if not pr_file.filename.endswith(".py"):
            continue
        if pr_file.status == "removed":
            continue
        try:
            content_obj = repo.get_contents(pr_file.filename, ref=pr.head.sha)
            file_contents[pr_file.filename] = content_obj.decoded_content.decode("utf-8")
        except GithubException as exc:
            log.warning("Could not fetch %s: %s", pr_file.filename, exc)

    log.info(
        "Fetched diff (%d chars) and %d Python files for PR #%d",
        len(diff_text), len(file_contents), pr_number,
    )
    return diff_text, file_contents


def post_review_comments(
    repo_full_name: str,
    pr_number: int,
    findings: list[dict],
    commit_sha: str,
) -> None:
    """
    Post all findings as a single GitHub PR review with inline comments.

    Batching into one create_review() call is important:
      • Avoids triggering GitHub's notification spam filter
      • Stays within the 60 req/hour unauthenticated rate limit
      • Appears as one cohesive review rather than many bot comments

    Findings with invalid file paths or line numbers are skipped gracefully.
    """
    if not findings:
        return

    gh = Github(GITHUB_TOKEN)
    repo = gh.get_repo(repo_full_name)
    pr = repo.get_pull(pr_number)
    commit = repo.get_commit(commit_sha)

    severity_emoji = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}

    comments = []
    for f in findings:
        sev = f.get("severity", "Low")
        emoji = severity_emoji.get(sev, "🟢")
        body = (
            f"{emoji} **[{sev}]** {f.get('issue', 'No description')}\n\n"
            f"**Suggested fix:** {f.get('fix', 'N/A')}"
        )
        path = f.get("file", "")
        line = f.get("line", 1)
        if path and isinstance(line, int) and line > 0:
            comments.append({"path": path, "line": line, "body": body})

    if not comments:
        log.info("No valid comments to post for PR #%d", pr_number)
        return

    try:
        pr.create_review(
            commit=commit,
            body="## 🤖 AI Code Review\n\nFindings are sorted High → Medium → Low.",
            event="COMMENT",
            comments=comments,
        )
        log.info("Posted %d inline comments to PR #%d", len(comments), pr_number)
    except GithubException as exc:
        log.error("Failed to post review on PR #%d: %s", pr_number, exc)
