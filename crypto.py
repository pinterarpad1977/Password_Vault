"""
Responsibility of this module:
• Turn a master password into an encryption key
• Encrypt bytes → encrypted bytes
• Decrypt bytes → original bytes
• Handle salt generation and usage
What it should NOT do:
• Know anything about Vault, VaultEntry, or JSON
• Touch the filesystem
• Deal with CLI or user interaction
It’s a pure crypto utility layer.
• Use:
	◦ Fernet for encryption/decryption
	◦ PBKDF2HMAC for key derivation
"""

import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode

# generates a random 16 bytes salt (added to the master password later)
def generate_salt() -> bytes: 
    return os.urandom(16)

##########################
# • PBKDF2 with SHA‑256
# 200k iterations (strong for personal use)
# 32‑byte key (required by Fernet)
# Base64‑encoded (Fernet requirement)
##########################

def derive_key(master_password: str, salt: bytes) -> bytes:
    password_bytes = master_password.encode("utf-8")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
    )

    key = kdf.derive(password_bytes)
    return urlsafe_b64encode(key)


def encrypt(data: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.encrypt(data)

# If the master password is wrong, this will raise an exception —
# we’ll catch that later in storage.py.
def decrypt(token: bytes, key: bytes) -> bytes:
    f = Fernet(key)
    return f.decrypt(token)

