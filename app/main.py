from fastapi import FastAPI, Request
from app.github import get_pr_diff, post_comment
from app.orchestrator import run_agents

app = FastAPI()


@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    print("Webhook received")

    if "pull_request" not in data:
        return {"status": "ignored"}

    repo = data["repository"]["full_name"]
    pr_number = data["pull_request"]["number"]

    print(f"PR received: {repo} #{pr_number}")

    # 🔥 FETCH PR DIFF
    pr_data = get_pr_diff(repo, pr_number)
    code = pr_data.get("body", "") or "sample code"

    # 🔥 RUN AI AGENTS
    results = run_agents(code)

    # 🔥 BUILD COMMENT
    comment = "## 🤖 AI Code Review Report\n\n"

    if results:
        for r in results:
            comment += f"### 🔍 {r.get('type')} ({r.get('severity')})\n"
            comment += f"📌 {r.get('message')}\n"

            if r.get("line"):
                comment += f"📍 Line: {r.get('line')}\n"

            comment += "\n---\n\n"
    else:
        comment += "✅ No issues found. Code looks clean and safe!"

    # 🔥 POST COMMENT
    post_comment(repo, pr_number, comment)

    return {"status": "processed"}