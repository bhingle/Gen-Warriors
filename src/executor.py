from gemini_api import call_gemini

# Mock vulnerability DB for demo
MOCK_VULN_DB = {
    'django': {'min_safe': '4.0', 'risk': 'Outdated, no longer receives security patches.'},
    'requests': {'min_safe': '2.31', 'risk': 'Known CVEs for versions <2.20.'},
}

def check_outdated(deps):
    results = []
    for name, version in deps:
        if name in MOCK_VULN_DB:
            info = MOCK_VULN_DB[name]
            min_safe = info['min_safe']
            risk = info['risk']
            results.append({
                'name': name,
                'version': version,
                'risk': risk,
                'recommendation': f"Upgrade to {name}>={min_safe}.",
                'suggested_version': min_safe
            })
        else:
            results.append({
                'name': name,
                'version': version,
                'risk': 'No known issues.',
                'recommendation': 'Up to date.',
                'suggested_version': version
            })
    return results

def generate_patched_file(deps, check_results):
    lines = []
    for res in check_results:
        lines.append(f"{res['name']}>={res['suggested_version']}")
    return '\n'.join(lines)

def execute(plan_tasks, deps):
    check_results = check_outdated(deps)
    # Prepare data for Gemini
    parsed_data = "\n".join([
        f"{r['name']}=={r['version']} (Risk: {r['risk']})" for r in check_results
    ])
    prompt = f"""
Analyze these dependencies and versions for security risks:
{parsed_data}

Output a risk score (0-100), explain risks in plain language, and suggest safe upgrade recommendations.
"""
    gemini_response = call_gemini(prompt)
    # Extract risk score (simple parse for demo)
    import re
    match = re.search(r"Risk Score: (\d+)", gemini_response)
    risk_score = int(match.group(1)) if match else 50
    # Generate patched file
    patched_file = generate_patched_file(deps, check_results)
    # Build report
    report = f"Dependency Risk Score: {risk_score}/100\n\n"
    for res in check_results:
        report += f"- {res['name']}=={res['version']}\n  Risk: {res['risk']}\n  Recommendation: {res['recommendation']}\n\n"
    report += f"\nSuggested Fixes (requirements.txt):\n{patched_file}\n\n---\nGemini Analysis:\n{gemini_response}"
    return report, patched_file, risk_score
