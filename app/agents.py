def security_agent(code):
    issues = []
    if "password" in code.lower():
        issues.append({
            "type": "Security",
            "severity": "High",
            "message": "Hardcoded password detected"
        })
    return issues


def performance_agent(code):
    issues = []
    if code.count("for") > 1:
        issues.append({
            "type": "Performance",
            "severity": "Medium",
            "message": "Possible nested loops detected"
        })
    return issues


def style_agent(code):
    issues = []
    if "print(" in code:
        issues.append({
            "type": "Style",
            "severity": "Low",
            "message": "Debug print statement found"
        })
    return issues