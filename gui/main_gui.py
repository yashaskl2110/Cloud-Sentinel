import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import customtkinter as ctk
from tkinter import ttk
from scanners.aws_scanner import scan_aws_bucket
from scanners.azure_scanner import scan_azure_container
from decrypt_logs import decrypt_logs_with_key
from dotenv import load_dotenv
from tkinter import messagebox

load_dotenv()


class CloudSentinelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CloudSentinel - Cloud Storage Leak Scanner")
        self.root.geometry("1100x650")

        self.sidebar = ctk.CTkFrame(self.root, width=200)
        self.sidebar.grid(row=0, column=0, padx=10, pady=10, sticky="ns")

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Sidebar UI
        ctk.CTkLabel(self.sidebar, text="Select Cloud Provider").pack(pady=(20, 5))
        self.provider_combobox = ctk.CTkComboBox(self.sidebar, values=["AWS", "Azure"])
        self.provider_combobox.set("AWS")
        self.provider_combobox.pack(pady=(0, 20))

        ctk.CTkLabel(self.sidebar, text="Enter Bucket/Container").pack(pady=(0, 5))
        self.bucket_entry = ctk.CTkEntry(self.sidebar)
        self.bucket_entry.pack(pady=(0, 20))

        self.scan_button = ctk.CTkButton(self.sidebar, text="Start Scan", command=self.start_scan)
        self.scan_button.pack(pady=(10, 10))

        self.decrypt_button = ctk.CTkButton(self.sidebar, text="🔓 Decrypt All Logs", command=self.open_decrypt_popup)
        self.decrypt_button.pack(pady=(0, 20))

        self.message_label = ctk.CTkLabel(self.sidebar, text="")
        self.message_label.pack(pady=(5, 20))

        # Table (Top)
        ctk.CTkLabel(self.main_frame, text="Leak Detection Dashboard", font=ctk.CTkFont(size=16, weight="bold")).pack()
        columns = ("File", "Leak Type", "Masked Value")
        self.treeview = ttk.Treeview(self.main_frame, columns=columns, show="headings", height=12)
        for col in columns:
            self.treeview.heading(col, text=col)
            self.treeview.column(col, width=300, anchor="center")
        self.treeview.pack(fill="x", pady=(10, 5))
        self.treeview.bind("<<TreeviewSelect>>", self.on_row_select)

        # Analysis Panel (Bottom)
        ctk.CTkLabel(self.main_frame, text="Analysis Panel", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(5, 0))
        self.analysis_panel = ctk.CTkFrame(self.main_frame)
        self.analysis_panel.pack(fill="both", expand=True, pady=(10, 0))
        self.analysis_text = ctk.CTkTextbox(self.analysis_panel, wrap="word", height=200)
        self.analysis_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.analysis_text.insert("1.0", "Select a row above to view detailed leak analysis.")
        self.analysis_text.configure(state="disabled")

        self.leak_data = []  # store full data for analysis panel

    def start_scan(self):
        provider = self.provider_combobox.get().lower()
        bucket = self.bucket_entry.get().strip()

        # Clear tables and message
        self.treeview.delete(*self.treeview.get_children())
        self.analysis_text.configure(state="normal")
        self.analysis_text.delete("1.0", "end")
        self.analysis_text.insert("1.0", "Select a row above to view detailed leak analysis.")
        self.analysis_text.configure(state="disabled")
        self.message_label.configure(text="")
        self.leak_data = []

        if not bucket:
            self.message_label.configure(text="⚠️ Please enter a valid bucket or container.")
            return

        try:
            results = scan_aws_bucket(bucket) if provider == "aws" else scan_azure_container(bucket)

            if not results:
                self.message_label.configure(text="✅ Scan complete. No leaks found.")
            else:
                self.leak_data = results
                for r in results:
                    masked_val = self.mask_value(r["value"])
                    self.treeview.insert("", "end", values=(r["file"], r["leak_type"], masked_val))
        except Exception as e:
            self.message_label.configure(text=f"❌ {str(e)}")
            print(f"❌ Error during scan: {e}")

    def on_row_select(self, event):
        selected = self.treeview.focus()
        if not selected:
            return

        index = self.treeview.index(selected)
        if index >= len(self.leak_data):
            return

        r = self.leak_data[index]
        full_info = (
            f"File: {r['file']}\n"
            f"Leak Type: Encrypted\n"
            f"Dev: {r['developer']}\n"
            f"First Seen: {r['first_seen']}\n"
            f"Last Modified: {r['last_modified']}\n"
            f"File Age: {r['age']}\n"
            f"Encrypted Leak: {r['value']}"
        )

        self.analysis_text.configure(state="normal")
        self.analysis_text.delete("1.0", "end")
        self.analysis_text.insert("1.0", full_info)
        self.analysis_text.configure(state="disabled")

    def mask_value(self, value):
        if len(value) <= 4:
            return "***"
        return "*" * (len(value) - 3) + value[-3:]

    def open_decrypt_popup(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("🔐 Decrypt All Leak Logs")
        popup.geometry("800x500")

        ctk.CTkLabel(popup, text="Enter Decryption Key:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20, 10))
        key_entry = ctk.CTkEntry(popup, show="*", width=500)
        key_entry.pack(pady=(0, 20))

        output_text = ctk.CTkTextbox(popup, wrap="word")
        output_text.pack(expand=True, fill="both", padx=20, pady=10)

        def decrypt():
            key = key_entry.get().strip()
            if not key:
                messagebox.showwarning("Warning", "Please enter a valid encryption key.")
                return
            try:
                results = decrypt_logs_with_key(key)
                if not results:
                    output_text.insert("1.0", "No encrypted logs found or key is invalid.")
                else:
                    output_text.delete("1.0", "end")
                    for line in results:
                        output_text.insert("end", line + "\n")
            except Exception as e:
                output_text.insert("1.0", f"❌ Error: {str(e)}")

        ctk.CTkButton(popup, text="🔓 Decrypt All", command=decrypt).pack(pady=(0, 20))


if __name__ == "__main__":
    root = ctk.CTk()
    app = CloudSentinelApp(root)
    root.mainloop()
