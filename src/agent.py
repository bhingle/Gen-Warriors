from planner import plan
from executor import execute
from memory import retrieve_memory, store_memory
from utils.parser import parse_dependency_file
from datetime import datetime, timezone


def merge_all_deps(parsed_data):
    combined = {}
    combined.update(parsed_data.get("dependencies", {}))
    combined.update(parsed_data.get("devDependencies", {}))
    return combined

def agent_main(dep_file_path):
    with open(dep_file_path, "r") as f:
        content = f.read()

    parsed_data, file_type = parse_dependency_file(dep_file_path, content)
    combined_deps = merge_all_deps(parsed_data)

    last_scan = retrieve_memory(dep_file_path)
    plan_tasks = plan(combined_deps, last_scan)

    report, patched_file, risk_score = execute(plan_tasks, combined_deps, parsed_data, file_type)


    store_memory(dep_file_path, {
        'dependencies': parsed_data,
        'risk_score': risk_score,
        'report': report,
        'patched_file': patched_file,
        'scan_date': datetime.now(timezone.utc).isoformat(),
        'file_type': file_type
    })


    return report, patched_file
