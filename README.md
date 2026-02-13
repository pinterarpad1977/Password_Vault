
Password Vault — v3.0
A fully local, encrypted password vault with a FastAPI backend and a modern browser-based frontend. Everything runs on your machine — no cloud, no telemetry, no external services.
This version replaces the old prototype UI with a complete, functional frontend featuring dark mode, safe rendering, edit/delete, and a clean API integration.

Features
🔐 Security
Local encrypted vault (vault.dat)
Salted key derivation (vault.salt)
Master password never stored or transmitted
Everything stays on your machine

🖥️ Frontend (v3.0)
Modern HTML/JS UI
Load, add, edit, delete entries
Mask/unmask passwords
Dark mode toggle
Safe HTML escaping
Unified event delegation (single listener for edit/delete)
Smooth edit mode with cancel + success message

🧩 Backend (FastAPI)
Full CRUD API
Password-protected endpoints
Automatic validation
Interactive API docs at /docs

🛠️ CLI Tools (Legacy)
One-shot commands
Interactive shell
Fully compatible with the vault format
Running the Backend (API)
From the project root:
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000

API docs:
http://localhost:8000/docs

Running the Frontend (UI)
From the frontend folder:
python3 -m http.server 5500

Open in your browser:
http://localhost:5500

Enter your master password to unlock the vault.
Project Structure
password_vault/
│
├── backend/
│   ├── api.py          # FastAPI routes
│   ├── crypto.py       # Encryption / decryption
│   ├── storage.py      # File I/O
│   ├── vault.py        # Vault logic
│   ├── models.py       # Pydantic models
│   ├── config.py
│   ├── cli.py          # Legacy CLI
│   └── cli_shell.py    # Legacy interactive shell
│
├── frontend/
│   ├── index.html      # New UI (v3.0)
│   ├── index_old.html  # Archived legacy UI
│   ├── script.js
│   └── styles.css
│
├── data/               # Vault files (ignored in git)
│   ├── vault.dat
│   └── vault.salt
│
├── requirements.txt
├── .gitignore
└── README.md

Version History

v3.0 (Current)
Complete frontend rewrite
Unified event listener for edit/delete
Dark mode with persistent UI state
Safe HTML escaping
Improved render logic
Stability and bug fixes

v2.0
Added FastAPI backend
Added first browser UI
Full CRUD support

v1.1
Added interactive CLI shell

v1.0
Initial CLI-only version
Security Notes
The master password is never stored or logged
Losing the master password means losing access to the vault
Losing the salt file (vault.salt) makes the vault unrecoverable
All data stays local — no external services involved
