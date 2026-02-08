# Password Vault — v2.0

A small, local password vault with encryption.
Everything runs on your machine.
No cloud, no tracking, no external services.

This version adds a backend API and a simple browser-based frontend on top of the original CLI tools.

## Features 

- Local encrypted vault (vault.dat)
- Salted key derivation (vault.salt)
- FastAPI backend with CRUD endpoints
- Simple frontend UI (HTML + JS)
- Search, add, edit, delete entries
- One-shot CLI
- Interactive shell

## Running the Backend (API)

From the project root:

uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000

API docs:

http://localhost:8000/docs

## Running the Frontend (UI)

From the frontend folder:

python3 -m http.server 5500

Open in your browser:

http://localhost:5500

Enter your master password and press Load.

## CLI (v1.x)

One-shot commands:

python backend/cli.py add <service> <username> <password> [notes]
python backend/cli.py list
python backend/cli.py search <query>
python backend/cli.py remove <service>

Interactive shell:

python backend/cli_shell.py

## Project Structure

password_vault/
│
├── backend/
│   ├── api.py
│   ├── crypto.py
│   ├── storage.py
│   ├── vault.py
│   ├── models.py
│   ├── config.py
│   ├── cli.py
│   └── cli_shell.py
│
├── frontend/
│   └── index.html
│
├── data/          (vault files, ignored in git)
│   ├── vault.dat
│   └── vault.salt
│
├── requirements.txt
├── .gitignore
└── README.md

## Version History

v2.0
- Added FastAPI backend
- Added browser frontend
- Added full CRUD support
- New project structure

v1.1
- Added interactive shell

v1.0
- Initial CLI version

## Security Notes

- The master password is never stored
- Losing the master password means losing access
- Losing the salt file also makes the vault unrecoverable
- Everything stays local
