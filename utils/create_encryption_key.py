from cryptography.fernet import Fernet


def generate_encryption_key() -> bytes:
    return Fernet.generate_key()
