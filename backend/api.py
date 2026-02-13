from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# “I’m importing the persistence layer, the crypto layer, 
# the config paths, and the manager that handles vault logic.”

from backend.storage import load_salt, load_vault
from backend.crypto import derive_key
from backend.config import SALT_FILE, VAULT_FILE
from backend.vault import VaultManager

# create the fastapi app
# the app object is my API, the endpoints will attach to it
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"], # allow all origins for now
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],

)

# when a get request is sent to /health, FastAPI will call
# health_check() and the the dict will be returned as JSON.
@app.get("/health")
def health_check():
    return {"status": "ok"}

# terminal call:
# uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000

# helper function to access the vault:
def get_vault_manager(master_password: str) -> tuple[VaultManager, bytes]:
    # 1. load or create salt
    salt = load_salt(SALT_FILE)

    # 2. derive key
    key = derive_key(master_password, salt)

    # 3. load vault
    vault = load_vault(VAULT_FILE, key)

    # 4. wrap in a manager
    manager = VaultManager(vault)
    return manager, key

@app.get("/entries")
def get_entries(password: str, q: str | None = None):
    manager, key = get_vault_manager(password)
    entries = manager.list_entries()

    if q:
        q_lower = q.lower()
        entries = [
            e for e in entries
            if q_lower in e.service.lower()
            or q_lower in e.username.lower()
            or (e.notes and q_lower in e.notes.lower())
        ]

    return [entry.__dict__ for entry in entries]


@app.get("/entries/{entry_id}")
def get_entry_by_id(entry_id:  str, password: str):
    manager, key = get_vault_manager(password)

    entry = manager.get_entry_by_id(entry_id)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    
    return entry.__dict__

@app.delete("/entries/{entry_id}")
def delete_entry(entry_id: str, password: str):
    manager, key = get_vault_manager(password)
   
    try:

        deleted = manager.remove_entry(entry_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Entry not found.")
        
        # save the updated vault
        from backend.storage import save_vault
        save_vault(VAULT_FILE, manager.vault, key)

        return {"status": "deleted", "id": entry_id}
    except Exception as e:
        print("DELETE ERROR:", e)
        raise


class EntryCreate(BaseModel):
    service: str
    username: str
    password: str
    notes: str | None = None

@app.post("/entries")
def create_entry(data: EntryCreate, password: str):
    manager, key = get_vault_manager(password)

    # create the entry
    manager.add_entry(
        service = data.service,
        username = data.username,
        password = data.password,
        notes = data.notes
    )

    # save the vault
    from backend.storage import save_vault
    save_vault(VAULT_FILE, manager.vault, key)

    # return the last entry
    entry = manager.vault.entries[-1]
    return entry.__dict__


class EntryUpdate(BaseModel):
    service: str | None = None
    username: str | None = None
    password: str | None = None
    notes: str | None = None


@app.put("/entries/{entry_id}")
def update_entry(entry_id: str, data: EntryUpdate, password: str):
    manager, key = get_vault_manager(password)

    updated = manager.update_entry(
        entry_id=entry_id,
        service=data.service,
        username=data.username,
        password=data.password,
        notes=data.notes
    )

    if updated is None:
        raise HTTPException(status_code=404, detail="Entry not found.")
    
    from backend.storage import save_vault
    save_vault(VAULT_FILE, manager.vault, key)

    return updated.__dict__

# use this request in the browser:
# http://localhost:8000/entries?password=YOUR_MASTER_PASSWORD

'''
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
• uvicorn → the ASGI server
• backend.api:app → path to your FastAPI app object
• –reload → auto‑reload on file changes
• –host 0.0.0.0 → listen on all interfaces (needed in containers)
• –port 8000 → your chosen port
'''

