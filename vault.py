from datetime import datetime, timezone
from .models import Vault, VaultEntry

class VaultManager:
    def __init__(self, vault: Vault):
        self.vault = vault

    def add_entry(self, service: str, username: str, password: str, notes: str | None = None):
            
        entry = VaultEntry(
            service=service,
            username=username,
            password=password,
            notes=notes
        )

        self.vault.entries.append(entry)
        self.update_metadata()


    def remove_entry(self, entry_id: str) -> bool:
        before = len(self.vault.entries)

        self.vault.entries = [
            e for e in self.vault.entries 
            if e.id != entry_id
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
            or q in e.id
        ]

    def list_entries(self) -> list[VaultEntry]:
        return list(self.vault.entries)

    def update_metadata(self) ->None:
        self.vault.metadata.updated_at = datetime.now(timezone.utc).isoformat()


    def update_entry(
            self,
            entry_id: str,
            service: str | None = None,
            username: str | None = None,
            password: str | None = None,
            notes: str | None = None
        ) -> VaultEntry | None:
        for entry in self.vault.entries:
            if entry.id == entry_id:
                if service is not None:
                    entry.service = service

                if username is not None:
                    entry.username = username

                if password is not None:
                    entry.password = password

                if notes is not None:
                    entry.notes = notes
                self.update_metadata()
                return entry
        return None
    
    def get_entry_by_id(self, entry_id: str) -> VaultEntry | None:
        for entry in self.vault.entries:
            if entry.id == entry_id:
                return entry
        return None