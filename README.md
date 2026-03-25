# 🤖 AI-Powered Code Review & Bug Detection Agent

An intelligent multi-agent system that automatically reviews GitHub Pull Requests for **security vulnerabilities**, **performance issues**, and **code style problems** — powered by **Groq AI (Mixtral)** and **FastAPI**.

---

## 🚀 How It Works

1. GitHub sends a webhook event when a Pull Request is opened
2. The FastAPI server receives the webhook and fetches the PR details
3. Three specialized AI agents analyze the code in parallel:
   - 🔐 **Security Agent** — detects vulnerabilities (e.g. hardcoded passwords, injections)
   - ⚡ **Performance Agent** — finds bottlenecks (e.g. nested loops, inefficient queries)
   - 🎨 **Style Agent** — checks code quality (e.g. debug prints, naming conventions)
4. Results are deduplicated, sorted by severity, and posted as a comment on the PR

---

## 🏗️ Project Structure

```
ai-code-review/
├── app/
│   ├── main.py          # FastAPI webhook endpoint
│   ├── orchestrator.py  # Multi-agent runner with Groq AI
│   ├── agents.py        # Rule-based fallback agents
│   ├── github.py        # GitHub API integration (fetch PR, post comment)
│   ├── config.py        # Environment variable loader
│   └── .env             # Secret keys (never committed)
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/Kaushalkumar012/AI-powered-Code-Review-Bug-Detection-Agent.git
cd AI-powered-Code-Review-Bug-Detection-Agent
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create your `.env` file inside the `app/` folder

```env
GITHUB_TOKEN=<your_github_token>
GROQ_API_KEY=<your_groq_api_key>
```

### 4. Run the server

```bash
uvicorn app.main:app --reload
```

---

## 🔗 GitHub Webhook Setup

1. Go to your GitHub repo → **Settings** → **Webhooks** → **Add webhook**
2. Set **Payload URL** to your server URL:
   ```
   http://<your-server-ip>:8000/webhook
   ```
3. Set **Content type** to `application/json`
4. Select **Pull requests** as the trigger event
5. Save the webhook

> 💡 For local testing, use [ngrok](https://ngrok.com/) to expose your local server:
> ```bash
> ngrok http 8000
> ```

---

## 🧠 AI Agents

| Agent | Powered By | Detects |
|---|---|---|
| Security Agent | Groq Mixtral | Hardcoded secrets, vulnerabilities |
| Performance Agent | Groq Mixtral | Nested loops, slow operations |
| Style Agent | Groq Mixtral | Debug prints, code quality issues |

Each agent sends a focused prompt to **Groq's Mixtral-8x7b** model and returns structured JSON findings.

---

## 📋 Sample PR Comment Output

```
## 🤖 AI Code Review Report

### 🔍 Security (High)
📌 Hardcoded password detected
📍 Line: 12

---

### 🔍 Performance (Medium)
📌 Possible nested loops detected

---

✅ No further issues found. Code looks clean and safe!
```

---

## 🛠️ Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) — Web framework for the webhook server
- [Groq API](https://groq.com/) — Ultra-fast LLM inference (Mixtral-8x7b)
- [GitHub REST API](https://docs.github.com/en/rest) — Fetch PRs and post comments
- [python-dotenv](https://pypi.org/project/python-dotenv/) — Environment variable management

---

## 🔒 Security Note

Never commit your `.env` file. It is already excluded via `.gitignore`. Use the following as a reference:

```env
GITHUB_TOKEN=<your_github_personal_access_token>
GROQ_API_KEY=<your_groq_api_key>
```

---

## 📄 License

MIT License — feel free to use, modify, and distribute.
