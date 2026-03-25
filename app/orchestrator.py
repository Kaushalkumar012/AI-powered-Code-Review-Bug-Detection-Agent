from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def call_ai(prompt):
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": "You are an expert code reviewer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1000
    )

    output = response.choices[0].message.content.strip()

    try:
        if output.startswith("```"):
            output = output.split("```")[1]

        return json.loads(output)
    except:
        return [{
            "type": "AI",
            "severity": "Low",
            "message": output,
            "line": None
        }]


# 🔥 MULTI AGENTS

def security_agent(code):
    prompt = f"""
Find security vulnerabilities in this code.

Return JSON only.

CODE:
{code}
"""
    return call_ai(prompt)


def performance_agent(code):
    prompt = f"""
Find performance issues in this code.

Return JSON only.

CODE:
{code}
"""
    return call_ai(prompt)


def style_agent(code):
    prompt = f"""
Find code quality and style issues.

Return JSON only.

CODE:
{code}
"""
    return call_ai(prompt)


# 🔥 ORCHESTRATOR

def run_agents(code):
    try:
        results = []

        results += security_agent(code)
        results += performance_agent(code)
        results += style_agent(code)

        # 🔥 REMOVE DUPLICATES
        unique = []
        seen = set()

        for r in results:
            key = (r.get("type"), r.get("message"))
            if key not in seen:
                seen.add(key)
                unique.append(r)

        # 🔥 SORT BY SEVERITY
        priority = {"High": 3, "Medium": 2, "Low": 1}
        unique.sort(key=lambda x: priority.get(x.get("severity"), 0), reverse=True)

        return unique

    except Exception as e:
        return [{
            "type": "System",
            "severity": "High",
            "message": str(e),
            "line": None
        }]