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
    - Identify if the current version has known vulnerabilities.
    - If vulnerabilities exist, include the CVSS score (0.0-10.0) and severity (Critical/High/Medium/Low).
    - Explain the risk in terms so non-technical stakeholders can understand and you should also map that to the potential business impact.
    - Suggest the latest safe/stable version.

    Dependencies:
    {parsed_data}

    Note : output section should be exactly in this format (plain text only, no Markdown, no backticks, no bold)
    Output must include:
    1. "Risk Score: <0-100>" as an overall project risk.
    2. For each dependency:
       - Current version
       - CVSS score (if any)
       - Severity
       - Risk explanation
    3. A "Suggested Fixes:" section with package>=version lines.
    """

    gemini_response = call_gemini(prompt)

    match = re.search(r"Risk Score: (\d+)", gemini_response)
    risk_score = int(match.group(1)) if match else 50

    suggested_versions = extract_suggested_versions(gemini_response)

    if file_type == "json":
        patched_file = generate_updated_package_json(original_sections, suggested_versions)
    else:
        patched_file = generate_patched_requirements(original_sections, suggested_versions)

    return gemini_response, patched_file, risk_score
