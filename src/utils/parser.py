import re

def parse_requirements_txt(path):
    deps = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            match = re.match(r'([a-zA-Z0-9_\-]+)==([\d\.]+)', line)
            if match:
                deps.append((match.group(1), match.group(2)))
    return deps

def parse_package_json(path):
    # Stub: implement if needed
    return []

def parse_dependency_file(path):
    if path.endswith('.txt'):
        return parse_requirements_txt(path)
    elif path.endswith('.json'):
        return parse_package_json(path)
    else:
        return []
