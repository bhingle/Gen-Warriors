from gemini_api import call_gemini
import re
import json


def extract_suggested_versions(gemini_response):
    suggestions = {}
    capture = False
    for line in gemini_response.splitlines():
        line = line.strip()
        if line.lower().startswith("suggested fixes"):
            capture = True
            continue
        if capture and line:
            match = re.match(r"([a-zA-Z0-9_\-]+)[>=]+([\d\.]+)", line)
            if match:
                pkg, version = match.groups()
                suggestions[pkg] = version
    return suggestions

def generate_patched_requirements(original_sections, suggested_versions):
    lines = []
    for pkg, ver in suggested_versions.items():
        prefix = original_sections["dependencies"].get(pkg, {}).get("prefix", "==")
        if ver:
            lines.append(f"{pkg}{prefix}{ver}")
        else:
            lines.append(pkg)
    return "\n".join(lines)


def generate_updated_package_json(original_sections, suggested_versions):
    deps = {}
    dev_deps = {}

    for pkg, ver in suggested_versions.items():
        if pkg in original_sections.get("dependencies", {}):
            prefix = original_sections["dependencies"][pkg]["prefix"]
            deps[pkg] = f"{prefix}{ver}"
        elif pkg in original_sections.get("devDependencies", {}):
            prefix = original_sections["devDependencies"][pkg]["prefix"]
            dev_deps[pkg] = f"{prefix}{ver}"

    return json.dumps({
        "dependencies": deps,
        "devDependencies": dev_deps
    }, indent=2)


def execute(plan_tasks, combined_deps, original_sections, file_type):
    parsed_data = "\n".join([
        f"{name}=={data['version'] if data['version'] else 'No version'}"
        for name, data in combined_deps.items()
    ])

    prompt = f"""
    You are a dependency risk analyzer.

    For each dependency below:
    - Identify if the current version has known vulnerabilities, check public databases (e.g., National Vulneability Database, Open Source Vulneabilities).
    - If multiple vulnerabilities exist for a version, use the highest CVSS score and the corresponding severity.
    - Explain the risk in terms so non-technical stakeholders can understand and you should also map that to the potential business impact.Explain business impact in a bit detail.
    - Suggest the latest safe/stable version.

    Dependencies:
    {parsed_data}

    Output only valid JSON. 
    ❌ Do NOT include markdown formatting.
    ❌ Do NOT wrap the JSON in ``` or add 'json'.
    ❌ Do NOT add explanations outside the JSON..

    Use this format:
    {{
    "risk_score": <0-100>,
    "dependencies": [
        {{
        "package": "<name>",
        "current_version": "<version>",
        "cvss": "<score or N/A>",
        "severity": "<Critical/High/Medium/Low>",
        "explanation": "<plain risk explanation>",
        "fix": "<package>=<version>"
        }}
    ],
    "suggested_fixes": [
        "<package>=<version>",
        "<package>=<version>"
    ]
    }}
    """

    gemini_response = call_gemini(prompt)
    # ✅ Parse JSON safely
    if gemini_response.strip().startswith("```"):
        match = re.search(r"\{.*\}", gemini_response, re.DOTALL)
        if match:
            gemini_response = match.group(0)
    try:
        parsed = json.loads(gemini_response)
    except json.JSONDecodeError:
        parsed = {"risk_score": 50, "dependencies": [], "suggested_fixes": []}

    risk_score = parsed.get("risk_score", 50)
    parsed_results = parsed.get("dependencies", [])

    # ✅ Build suggested_versions dict
    suggested_versions = {}
    for item in parsed.get("suggested_fixes", []):
        if ">=" in item:
            pkg, ver = item.split(">=")
            suggested_versions[pkg.strip()] = ver.strip()

    if file_type == "json":
        patched_file = generate_updated_package_json(original_sections, suggested_versions)
    else:
        patched_file = generate_patched_requirements(original_sections, suggested_versions)

    return parsed_results, patched_file, risk_score
