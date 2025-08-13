import csv
import os
from cryptography.fernet import Fernet

ENCRYPTED_LOG = "encrypted_logs.csv"
DETECTION_CSV = "detection_logs.csv"

def generate_key():
    key = Fernet.generate_key()
    with open(".encryption.key", "wb") as f:
        f.write(key)
    return key

def load_key():
    try:
        with open(".encryption.key", "rb") as f:
            return f.read()
    except FileNotFoundError:
        return generate_key()

def format_report(data):
    key = load_key()
    fernet = Fernet(key)

    # Append to detection_logs.csv
    write_header = not os.path.exists(DETECTION_CSV)
    with open(DETECTION_CSV, "a", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=[
            "provider", "bucket", "file", "leak_type", "value", 
            "developer", "first_seen", "last_modified", "age"
        ])
        if write_header:
            writer.writeheader()
        for row in data:
            writer.writerow({
                "provider": row.get("provider", "unknown"),
                "bucket": row.get("bucket", "unknown"),
                "file": row.get("file", ""),
                "leak_type": row.get("leak_type", ""),
                "value": row.get("value", ""),
                "developer": row.get("developer", "Unknown"),
                "first_seen": row.get("first_seen", ""),
                "last_modified": row.get("last_modified", ""),
                "age": row.get("age", "")
            })

    # Append to encrypted_logs.csv
    write_enc_header = not os.path.exists(ENCRYPTED_LOG)
    with open(ENCRYPTED_LOG, "a", newline="", encoding="utf-8") as enc_file:
        enc_writer = csv.DictWriter(enc_file, fieldnames=[
            "provider", "bucket", "file", "leak_type", "encrypted_value", 
            "developer", "first_seen", "last_modified", "age"
        ])
        if write_enc_header:
            enc_writer.writeheader()
        for row in data:
            encrypted_value = fernet.encrypt(row.get("value", "").encode()).decode()
            enc_writer.writerow({
                "provider": row.get("provider", "unknown"),
                "bucket": row.get("bucket", "unknown"),
                "file": row.get("file", ""),
                "leak_type": row.get("leak_type", ""),
                "encrypted_value": encrypted_value,
                "developer": row.get("developer", "Unknown"),
                "first_seen": row.get("first_seen", ""),
                "last_modified": row.get("last_modified", ""),
                "age": row.get("age", "")
            })

    print(f"✅ Reports saved to: {DETECTION_CSV} and {ENCRYPTED_LOG}")
