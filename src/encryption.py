import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()


def get_cipher() -> Fernet:
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError("ENCRYPTION_KEY not set in .env")
    return Fernet(key.encode())


def encrypt_data(data: bytes) -> bytes:
    cipher = get_cipher()
    return cipher.encrypt(data)


def decrypt_data(encrypted_data: bytes) -> bytes:
    cipher = get_cipher()
    return cipher.decrypt(encrypted_data)
