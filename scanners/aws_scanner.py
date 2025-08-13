import boto3
import os
from tempfile import NamedTemporaryFile
from utils.detectors import detect_sensitive_content
from reports.formatter import format_report
from utils.dev_fingerprint import get_developer_identity
from utils.decay_log import get_decay_info


def get_aws_session():
    return boto3.Session(
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="eu-north-1"
    )


def scan_aws_bucket(bucket_name):
    session = get_aws_session()
    s3 = session.client("s3")

    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
    except Exception as e:
        print(f"❌ Failed to list objects in bucket '{bucket_name}': {e}")
        return []

    all_leaks = []

    for obj in response.get("Contents", []):
        key = obj["Key"]
        extension = os.path.splitext(key)[-1].lower()
        if extension not in ['.env', '.log', '.json', '.txt']:
            continue

        tmp_file = NamedTemporaryFile(delete=False)
        try:
            s3.download_fileobj(bucket_name, key, tmp_file)
            tmp_file.close()
            with open(tmp_file.name, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                leaks = detect_sensitive_content(content, key)
                if leaks:
                    for file_path, leak_type, value in leaks:
                        developer = get_developer_identity(file_path)
                        decay = get_decay_info(file_path)
                        all_leaks.append({
                            "provider": "aws",
                            "bucket": bucket_name,
                            "file": file_path,
                            "leak_type": leak_type,
                            "value": value,
                            "developer": developer,
                            "first_seen": decay["first_seen"],
                            "last_modified": decay["last_modified"],
                            "age": decay["age"]
                        })
        except Exception as err:
            print(f"❌ Error reading {key}: {err}")
        finally:
            os.remove(tmp_file.name)

    if all_leaks:
        format_report(all_leaks)
    else:
        print("✅ No leaks found.")

    return all_leaks
