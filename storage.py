'''
This module handles:
✔ Reading the encrypted vault file
✔ Writing the encrypted vault file
✔ Managing the salt file
✔ Handling missing/corrupted vaults
✔ Converting between JSON ↔ dataclasses
✔ Integrating with crypto.py
It does not:
• ask for the master password
• manage CLI
• manage vault logic (add/delete/search)
It’s a pure persistence layer.'''

import os
import json
from dataclasses import asdict
from models import Vault, VaultMetadata, VaultEntry
from crypto import generate_salt, decrypt, encrypt
from config import SALT_FILE, VAULT_FILE

def load_salt(path: str) -> bytes:
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    else:
        salt = generate_salt()
        with open(path, "wb") as f:
            f.write(salt)
        return salt


def load_vault(path: str, key: bytes) -> Vault:
    if os.path.exists(path):
        with open(path, "rb") as f:
            encrypted_data = f.read()

        decrypted_bytes = decrypt(encrypted_data, key)
        
        data = json.loads(decrypted_bytes.decode("utf-8"))
        
        # rebuild entries
        entries = [
            VaultEntry(
                service = e["service"], 
                username = e["username"], 
                password = e["password"], 
                notes = e.get("notes")
            )
            for e in data["entries"]
        ]


        # rebuild metadata
        meta_dict = data["metadata"]
        metadata = VaultMetadata(
            created_at = meta_dict["created_at"],
            updated_at = meta_dict["updated_at"],
            version = meta_dict["version"]
        )

        return Vault(entries=entries, metadata=metadata)
    
    else:
        return Vault()

def save_vault(path: str, vault: Vault, key: bytes) -> None:
    # convert dataclasses to dict
    vault_dict = asdict(vault)

    # convert dict to JSON string
    json_str = json.dumps(vault_dict, indent=2)
    
    # convert json to bytes
    data_bytes = json_str.encode("utf-8")

    # encrypt the bytes
    encrypted = encrypt(data_bytes, key)

    with open(path, "wb") as f:
        f.write(encrypted)


