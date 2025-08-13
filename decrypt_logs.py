from utils.crypto_utils import decrypt_value
import csv, os

ENCRYPTED_LOG_PATH = "encrypted_logs.csv"

def get_encrypted_log(file_path):
    try:
        file_name_only = os.path.basename(file_path)
        with open(ENCRYPTED_LOG_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get("file") == file_name_only:
                    return f"{row.get('encrypted_value')}"
    except Exception as e:
        return f"Error reading log: {e}"
    return "No matching encrypted log found."

def get_developer_identity(file_path):
    try:
        file_name_only = os.path.basename(file_path)
        with open(ENCRYPTED_LOG_PATH, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get("file") == file_name_only:
                    return row.get("developer", "Unknown Developer")
    except Exception as e:
        return f"Error reading developer info: {e}"
    return "Unknown Developer"

# ✅ ADD THIS FUNCTION:
def decrypt_logs_with_key(file_path, key):
    encrypted = get_encrypted_log(file_path)
    if encrypted.startswith("Error") or encrypted.startswith("No matching"):
        return encrypted
    try:
        return decrypt_value(encrypted, key)
    except Exception as e:
        return f"Decryption failed: {e}"








