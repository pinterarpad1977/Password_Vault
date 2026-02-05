from dataclasses import dataclass, field
from datetime import datetime, timezone

@dataclass
class VaultEntry:
    service: str
    username: str
    password: str
    notes: str | None = None

@dataclass
class VaultMetadata:
    created_at: str = field(
        default_factory=lambda: 
        datetime.now(timezone.utc).isoformat())
    updated_at: str = field(
        default_factory=lambda: 
        datetime.now(timezone.utc).isoformat())
    version: int = 1


@dataclass
class Vault:
    entries: list[VaultEntry] = field(default_factory=list)
    metadata: VaultMetadata = field(default_factory=VaultMetadata)
