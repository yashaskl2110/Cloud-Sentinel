# CloudSentinel ☁️🔐  
**Cloud Storage Leak Detection Dashboard**

CloudSentinel is a **multi-cloud storage leak scanner** with an interactive **CustomTkinter GUI**.  
It scans **AWS S3** and **Azure Blob Storage** for sensitive data, encrypts detection logs, and provides real-time dashboards with analysis tools.

---

## 🚀 Features

- 🌍 **Multi-Cloud Support** – Scan both AWS S3 buckets and Azure Blob containers
- 📊 **Real-time Leak Dashboard** – Shows leaked files, types, and masked values instantly
- 🔐 **Encrypted Logging** – Stores leak values in `encrypted_logs.csv` using AES encryption
- 🗝️ **On-Demand Decryption** – “Decrypt All Logs” popup reveals actual values with your key
- ⏳ **File Decay Tracking** – Tracks first seen, last modified, and file age in days
- 🧑‍💻 **Developer Fingerprinting** – Identifies which developer introduced the leak
- 🆔 **Leak Fingerprinting** – Generates unique IDs to prevent duplicate tracking
- 🌐 **Cross-Cloud View** – See AWS + Azure leaks in one interface
- 🖥️ **Lightweight Desktop GUI** – Works without enterprise licensing costs

---

## 🆚 Enterprise vs CloudSentinel

| Feature                        | Azure Defender / Amazon Macie | **CloudSentinel** |
|--------------------------------|-------------------------------|-------------------|
| Sensitive Data Detection        | ✅                            | ✅ |
| Cross-Cloud Scanning            | ❌                            | ✅ |
| Developer Attribution           | ❌                            | ✅ |
| File Decay Tracking             | ❌                            | ✅ |
| AES-Encrypted Leak Logs         | ❌                            | ✅ |
| Offline Review of Logs          | ❌                            | ✅ |
| Cost                            | Enterprise pricing            | **Free & open-source** |

CloudSentinel adds **developer attribution, file decay tracking, and unified AWS/Azure dashboards** – features usually limited to enterprise-grade tools.

---

## 📸 Screenshots

| Dashboard | Leak Popup |
|-----------|------------|
| ![Dashboard](./docs/images/dashboard.png) | ![Leak Popup](./docs/images/leak_popup.png) |

| Quarantine | Encrypted Logs | CSV Logs |
|------------|----------------|----------|
| ![Quarantine](./docs/images/quarantine.png) | ![Encrypted Logs](./docs/images/encrypted_logs.png) | ![CSV Logs](./docs/images/csv_logs.png) |

| Terminal Output |
|-----------------|
| ![Terminal](./docs/images/terminal.png) |

---

## ⚡ Installation

```bash
git clone https://github.com/YOUR_USERNAME/CloudSentinel.git
cd CloudSentinel

python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.venv\\Scripts\\activate    # Windows

pip install -r requirements.txt

🔑 Configuration

Create a .env file in the root:
# AWS
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=your_region

# Azure
AZURE_STORAGE_ACCOUNT=your_account
AZURE_STORAGE_KEY=your_key

▶️ Run
python gui/main_gui.py

---
📜 Disclaimer
--- 
CloudSentinel is for educational and authorized security testing only.
Do NOT use it on systems you don’t own or have explicit permission to test.
