import os
from azure.storage.blob import BlobServiceClient
from tempfile import NamedTemporaryFile
from utils.detectors import detect_sensitive_content
from reports.formatter import format_report
from utils.dev_fingerprint import get_developer_identity
from utils.decay_log import get_decay_info


def get_azure_blob_service():
    conn_str = os.getenv("AZURE_CONNECTION_STRING")
    return BlobServiceClient.from_connection_string(conn_str)


def scan_azure_container(container_name):
    service = get_azure_blob_service()
    container = service.get_container_client(container_name)
    all_leaks = []

    for blob in container.list_blobs():
        blob_client = container.get_blob_client(blob.name)

        try:
            with NamedTemporaryFile(delete=False, mode='wb') as tmp_file:
                tmp_file.write(blob_client.download_blob().readall())
                tmp_file_path = tmp_file.name

            with open(tmp_file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                leaks = detect_sensitive_content(content, blob.name)
                if leaks:
                    for file_path, leak_type, value in leaks:
                        developer = get_developer_identity(file_path)
                        decay = get_decay_info(file_path)
                        all_leaks.append({
                            "provider": "azure",
                            "bucket": container_name,
                            "file": file_path,
                            "leak_type": leak_type,
                            "value": value,
                            "developer": developer,
                            "first_seen": decay["first_seen"],
                            "last_modified": decay["last_modified"],
                            "age": decay["age"]
                        })
        except Exception as e:
            print(f"❌ Error processing blob {blob.name}: {e}")
        finally:
            try:
                os.remove(tmp_file_path)
            except Exception as e:
                print(f"⚠️ Warning: Could not delete temp file {tmp_file_path}: {e}")

    if all_leaks:
        format_report(all_leaks)
    else:
        print("✅ No leaks found.")

    return all_leaks
