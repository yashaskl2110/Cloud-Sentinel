# Decrypt popup module placeholder
import customtkinter as ctk
from tkinter import scrolledtext
from cryptography.fernet import Fernet, InvalidToken
import csv

ENCRYPTED_CSV = "encrypted_logs.csv"

class DecryptPopup:
    def __init__(self, master):
        self.top = ctk.CTkToplevel(master)
        self.top.title("🔓 Decrypt All Leak Logs")
        self.top.geometry("800x500")
        self.top.grab_set()

        # Title label
        ctk.CTkLabel(self.top, text="Enter Decryption Key:", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))

        # Password entry
        self.key_entry = ctk.CTkEntry(self.top, show="*", width=600)
        self.key_entry.pack(pady=10)

        # Output box
        self.output_box = scrolledtext.ScrolledText(self.top, wrap="word", height=18, font=("Consolas", 11))
        self.output_box.pack(fill="both", expand=True, padx=20, pady=(10, 10))

        # Decrypt Button
        self.decrypt_button = ctk.CTkButton(self.top, text="📂 Decrypt All", command=self.decrypt_logs)
        self.decrypt_button.pack(pady=10)

    def decrypt_logs(self):
        key = self.key_entry.get().strip()

        if not key:
            self.output_box.insert("end", "❌ Please enter a decryption key.\n")
            return

        try:
            fernet = Fernet(key.encode())
        except Exception as e:
            self.output_box.insert("end", f"❌ Invalid key format: {e}\n")
            return

        try:
            with open(ENCRYPTED_CSV, newline='', encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                self.output_box.insert("end", "")  # Clear box

                for row in reader:
                    file = row["file"]
                    leak_type = row["leak_type"]
                    encrypted = row["encrypted_value"]
                    try:
                        decrypted_value = fernet.decrypt(encrypted.encode()).decode()
                        output = f"File: {file}\nType: {leak_type}\nDecrypted: {decrypted_value}\n\n"
                    except InvalidToken:
                        output = f"File: {file}\nType: {leak_type}\n❌ Invalid Key - Cannot Decrypt\n\n"

                    self.output_box.insert("end", output)

        except FileNotFoundError:
            self.output_box.insert("end", "❌ Encrypted log file not found.\n")
        except Exception as e:
            self.output_box.insert("end", f"❌ Error reading logs: {e}\n")
