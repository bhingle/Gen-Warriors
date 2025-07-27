import json
import os
from collections import OrderedDict

data_path = os.path.join(os.path.dirname(__file__), 'data', 'data_db.json')
MAX_ENTRIES = 10

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
        
        # Add the new entry
        db[dep_file_path] = scan_data
        
        # If we have more than MAX_ENTRIES, remove the oldest entries
        if len(db) > MAX_ENTRIES:
            # Convert to OrderedDict to maintain insertion order
            ordered_db = OrderedDict(db)
            
            # Remove the oldest entries (first inserted)
            while len(ordered_db) > MAX_ENTRIES:
                # Remove the first item (oldest)
                ordered_db.popitem(last=False)
            
            # Convert back to regular dict
            db = dict(ordered_db)
        
        with open(data_path, 'w') as f:
            json.dump(db, f, indent=2)
    except Exception as e:
        print(f"Memory store error: {e}")
