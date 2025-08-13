# utils/crypto_utils.py

from cryptography.fernet import Fernet
import os

# Load encryption key from environment variable
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

if ENCRYPTION_KEY is None:
    raise ValueError("❌ ENCRYPTION_KEY not found in environment variables.")

fernet = Fernet(ENCRYPTION_KEY)

def encrypt_value(value):
    """
    Encrypts a string value using Fernet encryption.
    Returns the encrypted string (UTF-8 encoded).
    """
    if not isinstance(value, str):
        value = str(value)
    encrypted = fernet.encrypt(value.encode())
    return encrypted.decode()
