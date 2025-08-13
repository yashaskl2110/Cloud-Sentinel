import csv
import os
from utils.crypto_utils import encrypt_value
from utils.dev_fingerprint import get_developer_identity


def save_leaks(leaks, provider, bucket):
    with open("detection_logs.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["provider", "bucket", "file", "leak_type", "value"])
        for leak in leaks:
            writer.writerow([
                provider, bucket,
                leak.get("file", ""),
                leak.get("leak_type", ""),
                leak.get("value", "")
            ])

    with open("encrypted_logs.csv", "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if f.tell() == 0:
            writer.writerow(["provider", "bucket", "file", "leak_type", "encrypted_value", "developer"])
        for leak in leaks:
            encrypted = encrypt_value(leak.get("value", ""))
            developer = get_developer_identity(leak.get("file", ""))
            writer.writerow([
                provider, bucket,
                leak.get("file", ""),
                leak.get("leak_type", ""),
                encrypted,
                developer
            ])
