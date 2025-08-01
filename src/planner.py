def plan(deps, last_scan=None):
    """
    Build a plan for analyzing dependencies with CVSS scoring and risk reporting.

    deps: merged dependencies in format {pkg: {"prefix": str, "version": str}}
    last_scan: previous scan result (optional)
    """

    tasks = []

    # A task for each dependency
    for pkg, data in deps.items():
        tasks.append({
            "package": pkg,
            "version": data.get("version")
        })

    return {
        "tasks": tasks,
        "check_vulnerabilities": True,     # check CVSS scores
        "generate_report": True,           # produce risk report
        "last_scan": last_scan
    }
