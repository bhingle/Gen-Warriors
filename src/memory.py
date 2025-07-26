import json
import os

data_path = os.path.join(os.path.dirname(__file__), 'data', 'data_db.json')

def retrieve_memory(dep_file_path):
    try:
        with open(data_path, 'r') as f:
            db = json.load(f)
        return db.get(dep_file_path, None)
    except Exception:
        return None

def store_memory(dep_file_path, scan_data):
    try:
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                db = json.load(f)
        else:
            db = {}
        db[dep_file_path] = scan_data
        with open(data_path, 'w') as f:
            json.dump(db, f, indent=2)
    except Exception as e:
        print(f"Memory store error: {e}")
