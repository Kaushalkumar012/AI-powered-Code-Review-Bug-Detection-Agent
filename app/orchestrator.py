from groq import Groq
import json
from concurrent.futures import ThreadPoolExecutor
from app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


class BaseAgent:
    def __init__(self, name, focus):
        self.name = name
        self.focus = focus

    def analyze(self, code):
        prompt = f"""You are a {self.name}. Find {self.focus} in the code below.

Return ONLY a JSON array:
[{{"type": "{self.name}", "severity": "High | Medium | Low", "message": "explain issue", "line": "line number or null"}}]

CODE:
{code}
"""
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": f"You are an expert {self.name}."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=800
            )
            output = response.choices[0].message.content.strip()
            if output.startswith("```"):
                output = output.split("```")[1].strip()
                if output.startswith("json"):
                    output = output[4:].strip()
            return json.loads(output)
        except Exception as e:
            return [{"type": self.name, "severity": "Low", "message": str(e), "line": None}]


class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__("Security Agent", "security vulnerabilities, hardcoded secrets, injections")


class PerformanceAgent(BaseAgent):
    def __init__(self):
        super().__init__("Performance Agent", "performance bottlenecks, nested loops, inefficient queries")


class StyleAgent(BaseAgent):
    def __init__(self):
        super().__init__("Style Agent", "code quality issues, debug prints, naming conventions")


def run_agents(code):
    agents = [SecurityAgent(), PerformanceAgent(), StyleAgent()]

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(lambda a: a.analyze(code), agents))

    flat = [item for sublist in results for item in sublist]

    # deduplicate
    seen, unique = set(), []
    for r in flat:
        key = (r.get("type"), r.get("message"))
        if key not in seen:
            seen.add(key)
            unique.append(r)

    # sort by severity
    priority = {"High": 3, "Medium": 2, "Low": 1}
    unique.sort(key=lambda x: priority.get(x.get("severity"), 0), reverse=True)

    return unique
