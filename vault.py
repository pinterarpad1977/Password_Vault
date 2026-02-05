from datetime import datetime, timezone
from models import Vault, VaultEntry

class VaultManager:
    def __init__(self, vault: Vault):
        self.vault = vault

    def add_entry(self, service: str, username: str, password: str, notes: str | None = None):
        # prevent duplicates
        for e in self.vault.entries:
            if e.service.lower() == service.lower():
                raise ValueError("Entry already exists for {service}.")
            
        entry = VaultEntry(
            service=service,
            username=username,
            password=password,
            notes=notes
        )

        self.vault.entries.append(entry)
        self.update_metadata()

    def remove_entry(self, service: str) -> bool:
        before = len(self.vault.entries)

        self.vault.entries = [
            e for e in self.vault.entries 
            if e.service.lower() != service.lower() 
        ]

        after = len(self.vault.entries)

        if before != after:
            self.update_metadata()
            return True
        return False

    def find_entries(self, query: str) -> list[VaultEntry]:
        q = query.lower()
        return [
            e for e in self.vault.entries
            if q in e.service.lower()
            or q in e.username.lower()
        ]

    def list_entries(self) -> list[VaultEntry]:
        return list(self.vault.entries)

    def update_metadata(self) ->None:
        self.vault.metadata.updated_at = datetime.now(timezone.utc).isoformat()

