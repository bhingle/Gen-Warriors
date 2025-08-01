import json
import os
from collections import OrderedDict

data_path = os.path.join(os.path.dirname(__file__), 'data', 'data_db.json')
MAX_ENTRIES = 10

def retrieve_memory(dep_file_path):
    try:
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                try:
                    db = json.load(f)
                except json.JSONDecodeError:
                    # Handles empty or corrupt file
                    return None
            return db.get(dep_file_path, None)
        return None
    except Exception:
        return None

def store_memory(dep_file_path, scan_data):
    try:
        if os.path.exists(data_path):
            with open(data_path, 'r') as f:
                try:
                    db = json.load(f)
                except json.JSONDecodeError:
                    # Reset to empty if file is invalid
                    db = {}
        else:
            db = {}
        
        # Add the new entry
        db[dep_file_path] = scan_data
        
        # Keep only the last MAX_ENTRIES
        if len(db) > MAX_ENTRIES:
            ordered_db = OrderedDict(db)
            while len(ordered_db) > MAX_ENTRIES:
                ordered_db.popitem(last=False)
            db = dict(ordered_db)
        
        with open(data_path, 'w') as f:
            json.dump(db, f, indent=2)
    except Exception as e:
        print(f"Memory store error: {e}")
