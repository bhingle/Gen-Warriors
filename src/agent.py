from planner import plan
from executor import execute
from memory import retrieve_memory, store_memory
from utils.parser import parse_dependency_file

def agent_main(dep_file_path):
    # Parse dependencies
    deps = parse_dependency_file(dep_file_path)
    # Retrieve last scan memory
    last_scan = retrieve_memory(dep_file_path)
    # Plan tasks (parse, check, plan report)
    plan_tasks = plan(deps, last_scan)
    # Execute (analyze, generate report, patched file)
    report, patched_file, risk_score = execute(plan_tasks, deps)
    # Store scan in memory
    store_memory(dep_file_path, {
        'dependencies': deps,
        'risk_score': risk_score,
        'report': report
    })
    return report, patched_file
