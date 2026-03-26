from groq import Groq
from openai import OpenAI
import os
import json
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_agents(code):
    prompt = f"""
Analyze the following code and find:
- Bugs
- Security issues
- Bad practices

Return ONLY JSON:
[
  {{
    "type": "Bug | Security | Performance | Style",
    "severity": "High | Medium | Low",
    "message": "Explain issue",
    "line": "line number or null"
  }}
]

CODE:
{code}
"""

    # 🔥 GROQ (FREE WORKING)
    try:
        response = groq_client.chat.completions.create(
            model="llama-3.1-8b-instant",   # ✅ FIXED
            messages=[
                {"role": "system", "content": "Expert code reviewer"},
                {"role": "user", "content": prompt}
            ]
        )
        output = response.choices[0].message.content.strip()

        try:
            return json.loads(output)
        except:
            return [{
                "type": "AI",
                "severity": "Low",
                "message": output,
                "line": None
            }]

    except Exception as e:
        print("Groq failed:", e)

    # 🔥 OPENAI (fallback)
    try:
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Expert code reviewer"},
                {"role": "user", "content": prompt}
            ]
        )
        output = response.choices[0].message.content.strip()

        try:
            return json.loads(output)
        except:
            return [{
                "type": "AI",
                "severity": "Low",
                "message": output,
                "line": None
            }]

    except Exception as e:
        return [{
            "type": "System",
            "severity": "High",
            "message": f"All AI providers failed: {str(e)}",
            "line": None
        }]