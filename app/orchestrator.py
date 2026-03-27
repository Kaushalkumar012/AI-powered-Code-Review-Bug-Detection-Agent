from groq import Groq
import json
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
import operator
from app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


# ── State ──────────────────────────────────────────────────────────────────────

class ReviewState(TypedDict):
    code: str
    security_findings: Annotated[list, operator.add]
    performance_findings: Annotated[list, operator.add]
    style_findings: Annotated[list, operator.add]
    final_findings: list


# ── Base Agent ─────────────────────────────────────────────────────────────────

class BaseAgent:
    def __init__(self, name: str, focus: str):
        self.name = name
        self.focus = focus

    def _call_llm(self, code: str) -> list:
        prompt = f"""You are a {self.name}. Find {self.focus} in the code below.

Return ONLY a JSON array:
[{{"type": "{self.name}", "severity": "High | Medium | Low", "message": "explain issue", "line": "line number or null", "suggested_fix": "fix or null"}}]

CODE:
{code}
"""
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": f"You are an expert {self.name}. Return only valid JSON."},
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
            return [{"type": self.name, "severity": "Low", "message": str(e), "line": None, "suggested_fix": None}]

    def run(self, state: ReviewState) -> dict:
        raise NotImplementedError


# ── Worker Agents ──────────────────────────────────────────────────────────────

class SecurityAgent(BaseAgent):
    def __init__(self):
        super().__init__("Security Agent", "security vulnerabilities, hardcoded secrets, SQL injection, XSS")

    def run(self, state: ReviewState) -> dict:
        findings = self._call_llm(state["code"])
        return {"security_findings": findings}


class PerformanceAgent(BaseAgent):
    def __init__(self):
        super().__init__("Performance Agent", "performance bottlenecks, nested loops, N+1 queries, inefficient operations")

    def run(self, state: ReviewState) -> dict:
        findings = self._call_llm(state["code"])
        return {"performance_findings": findings}


class StyleAgent(BaseAgent):
    def __init__(self):
        super().__init__("Style Agent", "code quality issues, debug prints, poor naming conventions, dead code")

    def run(self, state: ReviewState) -> dict:
        findings = self._call_llm(state["code"])
        return {"style_findings": findings}


# ── Orchestrator Agent ─────────────────────────────────────────────────────────

class OrchestratorAgent:
    def run(self, state: ReviewState) -> dict:
        all_findings = (
            state.get("security_findings", []) +
            state.get("performance_findings", []) +
            state.get("style_findings", [])
        )

        # deduplicate
        seen, unique = set(), []
        for r in all_findings:
            key = (r.get("type"), r.get("message"))
            if key not in seen:
                seen.add(key)
                unique.append(r)

        # sort by severity
        priority = {"High": 3, "Medium": 2, "Low": 1}
        unique.sort(key=lambda x: priority.get(x.get("severity"), 0), reverse=True)

        return {"final_findings": unique}


# ── LangGraph Pipeline ─────────────────────────────────────────────────────────

security_agent = SecurityAgent()
performance_agent = PerformanceAgent()
style_agent = StyleAgent()
orchestrator_agent = OrchestratorAgent()

graph = StateGraph(ReviewState)

graph.add_node("security", security_agent.run)
graph.add_node("performance", performance_agent.run)
graph.add_node("style", style_agent.run)
graph.add_node("orchestrator", orchestrator_agent.run)

graph.set_entry_point("security")
graph.add_edge("security", "performance")
graph.add_edge("performance", "style")
graph.add_edge("style", "orchestrator")
graph.add_edge("orchestrator", END)

pipeline = graph.compile()


# ── Entry Point ────────────────────────────────────────────────────────────────

def run_agents(code: str) -> list:
    result = pipeline.invoke({
        "code": code,
        "security_findings": [],
        "performance_findings": [],
        "style_findings": [],
        "final_findings": []
    })
    return result["final_findings"]
