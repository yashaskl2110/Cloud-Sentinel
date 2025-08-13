# main.py

import argparse
import os
from dotenv import load_dotenv
from reports.formatter import format_report

# Load variables from .env if available
load_dotenv()

# Fallback: Load from .encryption.key if ENCRYPTION_KEY is not in environment
if "ENCRYPTION_KEY" not in os.environ:
    try:
        with open(".encryption.key", "r") as f:
            os.environ["ENCRYPTION_KEY"] = f.read().strip()
    except FileNotFoundError:
        raise ValueError("❌ ENCRYPTION_KEY not found in environment and .encryption.key file is missing.")

def main():
    parser = argparse.ArgumentParser(description="CloudSentinel - Cloud Storage Leak Scanner")
    parser.add_argument("--provider", choices=["aws", "azure"], required=True, help="Cloud provider to scan")
    parser.add_argument("--bucket", help="AWS S3 bucket name (for --provider aws)")
    parser.add_argument("--container", help="Azure container name (for --provider azure)")
    args = parser.parse_args()

    report = []

    if args.provider == "aws":
        if not args.bucket:
            print("❌ Please provide an AWS S3 bucket name using --bucket")
            return
        from scanners.aws_scanner import scan_aws_bucket
        print(f"🟡 Scanning AWS S3 bucket: {args.bucket}")
        report = scan_aws_bucket(args.bucket)

    elif args.provider == "azure":
        if not args.container:
            print("❌ Please provide an Azure container name using --container")
            return
        from scanners.azure_scanner import scan_azure_container
        print(f"🟡 Scanning Azure container: {args.container}")
        report = scan_azure_container(args.container)

    print("✅ Scan complete. Generating report...")
    format_report(report)

if __name__ == "__main__":
    main()
