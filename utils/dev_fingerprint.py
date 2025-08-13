# utils/dev_fingerprint.py

import hashlib
import os

def get_developer_identity(file_path: str) -> str:
    """
    Generate a consistent hash-based developer identity from file metadata.
    """
    try:
        stat = os.stat(file_path)
        unique_string = f"{stat.st_ctime}-{stat.st_mtime}-{stat.st_size}-{file_path}"
        return hashlib.sha256(unique_string.encode()).hexdigest()[:10]
    except Exception as e:
        return "unknown-dev"
