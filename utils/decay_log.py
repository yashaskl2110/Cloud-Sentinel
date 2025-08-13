import os
import json
from datetime import datetime
from dateutil import parser

DECAY_DB = "file_decay.json"

def load_decay_db():
    if os.path.exists(DECAY_DB):
        with open(DECAY_DB, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_decay_db(data):
    with open(DECAY_DB, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def get_decay_info(file_path):
    db = load_decay_db()
    now = datetime.utcnow().isoformat()

    if file_path not in db:
        db[file_path] = {
            "first_seen": now,
            "last_modified": now
        }
    else:
        db[file_path]["last_modified"] = now

    first_seen = parser.isoparse(db[file_path]["first_seen"])
    last_modified = parser.isoparse(db[file_path]["last_modified"])
    age_days = (last_modified - first_seen).days

    save_decay_db(db)

    return {
        "first_seen": db[file_path]["first_seen"],
        "last_modified": db[file_path]["last_modified"],
        "age": age_days
    }
