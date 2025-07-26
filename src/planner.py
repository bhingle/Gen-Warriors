def plan(deps, last_scan=None):
    # Plan: check outdated/insecure, plan report
    return {
        'check_outdated': True,
        'generate_report': True,
        'last_scan': last_scan
    }
