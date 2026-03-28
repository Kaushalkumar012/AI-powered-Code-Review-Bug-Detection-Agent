<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0a0a,30:0d1117,60:00d9ff,100:7b2fbe&height=260&section=header&text=AI%20Code%20Review%20Agent&fontSize=58&fontColor=ffffff&fontAlignY=40&desc=LangGraph%20%E2%80%A2%20Tree-sitter%20AST%20%E2%80%A2%20FastAPI%20%E2%80%A2%20GPT-4o-mini&descSize=20&descAlignY=62&descFontColor=00d9ff&animation=fadeIn" />

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=800&size=24&duration=2500&pause=600&color=00D9FF&center=true&vCenter=true&repeat=true&width=800&height=60&lines=AI-Powered+Code+Review+%26+Bug+Detection;OWASP+Top-10+Security+Analysis;N%2B1+Query+%26+Performance+Detection;PEP+8+%26+Style+Enforcement;95%25+Token+Reduction+via+Tree-sitter+AST;Production-Ready+%7C+Docker+%7C+35+Tests+Passing" alt="Typing SVG" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white&labelColor=0d1117)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white&labelColor=0d1117)](https://fastapi.tiangolo.com)
[![LangGraph](https://img.shields.io/badge/LangGraph-1.1.3-FF6B6B?style=for-the-badge&logo=chainlink&logoColor=white&labelColor=0d1117)](https://langchain-ai.github.io/langgraph/)
[![OpenAI](https://img.shields.io/badge/GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white&labelColor=0d1117)](https://openai.com)

<br/>

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white&labelColor=0d1117)](https://docker.com)
[![Tests](https://img.shields.io/badge/Tests-35%20Passing-00C853?style=for-the-badge&logo=pytest&logoColor=white&labelColor=0d1117)](https://pytest.org)
[![Coverage](https://img.shields.io/badge/Token%20Reduction-95%25-00C853?style=for-the-badge&logo=codecov&logoColor=white&labelColor=0d1117)](#)
[![License](https://img.shields.io/badge/License-MIT-F7DF1E?style=for-the-badge&logo=opensourceinitiative&logoColor=black&labelColor=0d1117)](LICENSE)

<br/>

<img src="https://readme-typing-svg.demolab.com?font=Roboto&weight=400&size=16&duration=5000&pause=3000&color=888888&center=true&vCenter=true&width=780&height=30&lines=A+production-ready+AI+agent+that+intercepts+GitHub+PRs+and+posts+intelligent+inline+review+comments." alt="desc" />

<br/>

**[Quick Start](#-quick-start)** &nbsp;•&nbsp; **[Architecture](#-architecture)** &nbsp;•&nbsp; **[Installation](#-installation)** &nbsp;•&nbsp; **[Docker](#-docker)** &nbsp;•&nbsp; **[Tests](#-running-tests)** &nbsp;•&nbsp; **[API](#-api-endpoints)**

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00d9ff,100:7b2fbe&height=3&section=header" width="100%"/>

## ✨ Features

<table>
<tr>
<td align="center" width="25%">

**🔐 Security Analysis**

SQL/NoSQL Injection · Hardcoded Secrets · Command Injection · Insecure Deserialization · Path Traversal · **OWASP Top-10**

</td>
<td align="center" width="25%">

**⚡ Performance Analysis**

N+1 Queries · O(n²) Loops · Blocking I/O · Missing Bulk Ops · Repeated Calls · **Caching Hints**

</td>
<td align="center" width="25%">

**🎨 Style Analysis**

PEP 8 · Missing Docstrings · Type Hints · Magic Numbers · Unclear Names · **Import Order**

</td>
<td align="center" width="25%">

**🧠 Smart Pipeline**

**~95% Token Reduction** · Parallel Agents · Dedup + Sort · Rate Limiting · Batched Comments

</td>
</tr>
</table>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:7b2fbe,100:00d9ff&height=3&section=header" width="100%"/>

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                       GitHub PR Event                            │
└─────────────────────────────┬────────────────────────────────────┘
                              │  POST /webhook
                              ▼
┌──────────────────────────────────────────────────────────────────┐
│                   FastAPI  (src/main.py)                         │
│   ① HMAC-SHA256 signature verification                           │
│   ② Filter: opened / synchronize / reopened only                 │
└─────────────────────────────┬────────────────────────────────────┘
                              │
                   ┌──────────▼──────────┐
                   │  github_client.py   │
                   │  • Fetch raw diff   │
                   │  • Fetch .py files  │
                   └──────────┬──────────┘
                              │
                   ┌──────────▼──────────┐
                   │     parser.py       │  ◄── ~95% Token Reduction
                   │  Tree-sitter AST    │  500 lines → ~30 lines
                   │  Semantic Chunking  │  (only changed functions)
                   └──────────┬──────────┘
                              │
         ┌────────────────────▼─────────────────────┐
         │            LangGraph Pipeline             │
         │                                           │
         │          ┌─── Orchestrator ───┐           │
         │          │                   │           │
         │    ┌─────▼─────┐  ┌──────────▼──┐  ┌────▼──────┐
         │    │ Security  │  │ Performance │  │  Style    │
         │    │  Agent    │  │   Agent     │  │  Agent    │
         │    │ OWASP Top │  │ N+1, O(n²) │  │  PEP 8   │
         │    └─────┬─────┘  └──────┬──────┘  └────┬──────┘
         │          └───────────────┼───────────────┘
         │                          │
         │               ┌──────────▼──────────┐
         │               │    Synthesizer       │
         │               │  Dedup + Sort        │
         │               │  High → Medium → Low │
         │               └──────────┬──────────┘
         └──────────────────────────┼──────────────┘
                                    │
                   ┌────────────────▼────────────────┐
                   │       github_client.py           │
                   │   Post inline PR comments        │
                   │   (single batched review)        │
                   └─────────────────────────────────┘
```

### 💡 Why ~95% Token Reduction?

| Approach | Tokens Sent | Cost |
|:---|:---:|:---:|
| Raw diff (500-line file) | ~5,000 tokens | 💸 Expensive |
| **AST Semantic Chunking** | **~300 tokens** | ✅ **94% cheaper** |

> Tree-sitter extracts **only** the `function_definition` / `class_definition` nodes that overlap with changed lines — complete, syntactically valid units, not truncated diff hunks.

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00d9ff,100:7b2fbe&height=3&section=header" width="100%"/>

## 🛠️ Tech Stack

<div align="center">

<img src="https://skillicons.dev/icons?i=python,fastapi,docker,git,github,vscode,linux&theme=dark&perline=7" />

<br/><br/>

| Layer | Technology |
|:---|:---|
| 🌐 Web Framework | [FastAPI](https://fastapi.tiangolo.com) + Uvicorn |
| 🤖 AI Orchestration | [LangGraph 1.x](https://langchain-ai.github.io/langgraph/) |
| 🧠 LLM | [OpenAI GPT-4o-mini](https://openai.com) via LangChain |
| 🌳 AST Parsing | [Tree-sitter 0.25](https://tree-sitter.github.io) + tree-sitter-python |
| 🐙 GitHub Integration | [PyGithub](https://pygithub.readthedocs.io) |
| 🔗 HTTP Client | [httpx](https://www.python-httpx.org) |
| ⚙️ Config | [python-dotenv](https://pypi.org/project/python-dotenv/) |
| 🧪 Testing | [pytest](https://pytest.org) + pytest-asyncio |
| 🐳 Containerisation | Docker + docker-compose |

</div>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:7b2fbe,100:00d9ff&height=3&section=header" width="100%"/>

## 📁 Project Structure

```
AI-powered-Code-Review-Bug-Detection-Agent/
│
├── 📁 src/                        ← Application source code
│   ├── main.py                    FastAPI entrypoint + webhook handler
│   ├── agents.py                  LangGraph state machine + agent nodes
│   ├── parser.py                  Tree-sitter AST semantic chunker
│   ├── github_client.py           GitHub API: fetch PR data, post comments
│   └── config.py                  Env-var loading via python-dotenv
│
├── 📁 tests/                      ← All test files
│   ├── test_parser.py             Diff parsing, AST, token reduction
│   ├── test_agents.py             LLM mocking, agents, synthesizer
│   └── test_webhook.py            FastAPI endpoint integration tests
│
├── 📁 docker/                     ← Container configuration
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── requirements.txt
├── pytest.ini
├── .env.example
└── .gitignore
```

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00d9ff,100:7b2fbe&height=3&section=header" width="100%"/>

## ⚙️ Installation

### Prerequisites

| Tool | Version | Download |
|:---|:---:|:---:|
| Python | 3.11+ | [python.org](https://python.org/downloads) |
| Git | Any | [git-scm.com](https://git-scm.com/downloads) |
| ngrok *(dev only)* | Any | [ngrok.com/download](https://ngrok.com/download) |
| Docker *(optional)* | Any | [docker.com](https://docker.com/get-started) |

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:7b2fbe,100:00d9ff&height=3&section=header" width="100%"/>

## 🚀 Quick Start

### Step 1 — Clone the repository

```bash
git clone https://github.com/AI-Code-Review-Team/AI-powered-Code-Review-Bug-Detection-Agent.git
cd AI-powered-Code-Review-Bug-Detection-Agent
```

### Step 2 — Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Configure environment variables

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and fill in your credentials:

```env
GITHUB_TOKEN=ghp_your_github_token_here
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here
OPENAI_API_KEY=sk-your_openai_key_here
LLM_MODEL=gpt-4o-mini
```

> **Get your keys:**
> - GitHub Token → [github.com/settings/tokens](https://github.com/settings/tokens) → Classic → `repo` scope
> - OpenAI Key → [platform.openai.com/api-keys](https://platform.openai.com/api-keys)

### Step 5 — Run the server

```bash
uvicorn src.main:app --reload --port 8000
```

Visit **http://localhost:8000/health** ✅

### Step 6 — Expose via ngrok

```bash
ngrok http 8000
# Copy the https URL → e.g. https://abc123.ngrok-free.app
```

### Step 7 — Register GitHub Webhook

| Field | Value |
|:---|:---|
| Payload URL | `https://abc123.ngrok-free.app/webhook` |
| Content type | `application/json` |
| Secret | value of `GITHUB_WEBHOOK_SECRET` |
| Events | Pull requests only |

### Step 8 — Open a PR and watch it work!

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00d9ff,100:7b2fbe&height=3&section=header" width="100%"/>

## 🐳 Docker

```bash
git clone https://github.com/AI-Code-Review-Team/AI-powered-Code-Review-Bug-Detection-Agent.git
cd AI-powered-Code-Review-Bug-Detection-Agent
cp .env.example .env

# docker-compose
docker-compose -f docker/docker-compose.yml up --build

# plain Docker
docker build -f docker/Dockerfile -t ai-code-review-agent .
docker run -p 8000:8000 --env-file .env ai-code-review-agent
```

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:7b2fbe,100:00d9ff&height=3&section=header" width="100%"/>

## 🧪 Running Tests

```bash
pytest -v
```

```
tests/test_agents.py::test_call_llm_parses_json_array          PASSED
tests/test_agents.py::test_security_agent_returns_findings     PASSED
tests/test_agents.py::test_synthesizer_sorts_by_severity       PASSED
tests/test_agents.py::test_full_graph_returns_final_findings   PASSED
tests/test_parser.py::test_parse_diff_hunks_returns_correct_file PASSED
tests/test_parser.py::test_ast_extracts_function               PASSED
tests/test_parser.py::test_token_reduction_demonstration       PASSED
tests/test_webhook.py::test_webhook_processes_opened_pr        PASSED
...
====================== 35 passed in 3.64s ======================
```

| Test File | Coverage |
|:---|:---|
| `tests/test_parser.py` | Diff parsing, AST extraction, regex fallback, token reduction |
| `tests/test_agents.py` | LLM mocking, all agent nodes, synthesizer dedup/sort, full graph |
| `tests/test_webhook.py` | Signature validation, event filtering, happy path, error handling |

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00d9ff,100:7b2fbe&height=3&section=header" width="100%"/>

## 📡 API Endpoints

| Method | Endpoint | Description |
|:---:|:---|:---|
| `POST` | `/webhook` | GitHub PR webhook receiver |
| `GET` | `/health` | Liveness probe |

```json
{
  "status": "ok",
  "pr": 42,
  "chunks_analysed": 7,
  "findings_count": 4,
  "findings": [
    {
      "file": "app/views.py",
      "line": 42,
      "severity": "High",
      "issue": "SQL injection via f-string interpolation",
      "fix": "Use parameterised queries: db.execute('SELECT * FROM users WHERE name=?', (user,))"
    }
  ]
}
```

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:7b2fbe,100:00d9ff&height=3&section=header" width="100%"/>

## 🔍 Sample PR Comments

```
[High]   SQL injection via f-string interpolation
         Fix: db.execute('SELECT * FROM users WHERE name=?', (user,))

[Medium] N+1 query pattern — DB call inside a for-loop
         Fix: users = User.objects.filter(id__in=user_ids)

[Low]    Missing docstring on public function process_payment
         Fix: Add a docstring describing parameters and return value.
```

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00d9ff,100:7b2fbe&height=3&section=header" width="100%"/>

## 🛡️ Rate Limiting & Safety

| Protection | Implementation |
|:---|:---|
| LLM rate limiting | `asyncio.Semaphore(5)` — max 5 concurrent OpenAI calls |
| GitHub API safety | All findings batched into **one** `create_review()` call |
| Blocking I/O | GitHub calls run in thread pool via `run_in_executor` |
| Webhook security | HMAC-SHA256 signature verified on every request |

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:7b2fbe,100:00d9ff&height=3&section=header" width="100%"/>

## 🔧 Troubleshooting

<details>
<summary><b>tree-sitter import error</b></summary>

```bash
pip install tree-sitter==0.25.2 tree-sitter-python==0.23.6
```
</details>

<details>
<summary><b>OpenAI AuthenticationError</b></summary>

Check that `OPENAI_API_KEY` is set correctly in your `.env` file in the project root.
</details>

<details>
<summary><b>Webhook shows Invalid signature</b></summary>

`GITHUB_WEBHOOK_SECRET` in `.env` must exactly match the secret entered in GitHub webhook settings.
</details>

<details>
<summary><b>ngrok tunnel not working</b></summary>

```bash
uvicorn src.main:app --port 8000   # terminal 1
ngrok http 8000                    # terminal 2
```
</details>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7b2fbe,50:00d9ff,100:0d1117&height=160&section=footer&animation=fadeIn" width="100%"/>

<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=15&duration=3000&pause=1500&color=00D9FF&center=true&vCenter=true&width=500&height=35&lines=Star+this+repo+if+it+helped+you!;Built+with+LangGraph+%2B+Tree-sitter+%2B+FastAPI;Keeping+your+PRs+secure+%26+clean" alt="footer" />

<br/><br/>

**Made with ❤️ by [r4hul-s3thi](https://github.com/r4hul-s3thi)**

<br/>

[![Stars](https://img.shields.io/github/stars/AI-Code-Review-Team/AI-powered-Code-Review-Bug-Detection-Agent?style=for-the-badge&logo=github&color=FFD700&labelColor=0d1117)](https://github.com/AI-Code-Review-Team/AI-powered-Code-Review-Bug-Detection-Agent/stargazers)
[![Forks](https://img.shields.io/github/forks/AI-Code-Review-Team/AI-powered-Code-Review-Bug-Detection-Agent?style=for-the-badge&logo=github&color=00D9FF&labelColor=0d1117)](https://github.com/AI-Code-Review-Team/AI-powered-Code-Review-Bug-Detection-Agent/network/members)
[![Issues](https://img.shields.io/github/issues/AI-Code-Review-Team/AI-powered-Code-Review-Bug-Detection-Agent?style=for-the-badge&logo=github&color=FF6B6B&labelColor=0d1117)](https://github.com/AI-Code-Review-Team/AI-powered-Code-Review-Bug-Detection-Agent/issues)

</div>
