"""
Authentication utility functions
"""
from cryptography.fernet import Fernet
from config import settings
import base64
import hashlib


def get_aes_key() -> bytes:
    """Get AES encryption key"""
    # Ensure key is 32 bytes for AES-256
    key = settings.AES_KEY.encode()
    # Pad or truncate to 32 bytes
    key_hash = hashlib.sha256(key).digest()
    return base64.urlsafe_b64encode(key_hash)


def encrypt_data(data: str) -> str:
    """Encrypt data using AES-256"""
    key = get_aes_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data.encode())
    return encrypted.decode()


def decrypt_data(encrypted_data: str) -> str:
    """Decrypt data using AES-256"""
    key = get_aes_key()
    fernet = Fernet(key)
    decrypted = fernet.decrypt(encrypted_data.encode())
    return decrypted.decode()
