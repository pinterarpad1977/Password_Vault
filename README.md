# 🔐 Password Vault — v1.1

A lightweight, fully local, encrypted password vault written in Python.  
All data is encrypted using **Fernet (AES‑128)** with a key derived from your **master password** using **PBKDF2‑HMAC‑SHA256**.

No cloud.  
No telemetry.  
Your passwords stay on your machine.

---

## 🚀 Features

- Secure encryption using Fernet  
- Salted key derivation (PBKDF2)  
- Encrypted vault storage (`vault.dat`)  
- Automatic salt handling (`vault.salt`)  
- Add, list, search, and remove entries  
- Notes support  
- One‑shot CLI (`cli.py`)  
- Interactive shell (`cli_shell.py`)  
- Clean modular architecture

---

## 📦 Installation

```bash
pip install cryptography
```

---

## 🖥️ One‑Shot CLI Usage (v1.0)

Run commands directly:

```bash
python cli.py add <service> <username> <password> [notes...]
python cli.py list
python cli.py search <query>
python cli.py remove <service>
```

You will be prompted for your **master password** each time.

---

## 🖥️ Interactive Shell (v1.1)

Start the shell:

```bash
python cli_shell.py
```

You will see:

```
Password Vault Shell
Master password:
Vault shell started. Type 'help' for commands, 'exit' to quit.
vault>
```

### Shell Commands

```
add <service> <username> <password> [notes...]
list
search <query>
remove <service>
help
exit
```

---

## 🧱 Project Structure

```
pwd_vault/
│
├── cli.py            # One-shot CLI
├── cli_shell.py      # Interactive shell (v1.1)
├── crypto.py         # Encryption / decryption
├── storage.py        # File I/O
├── vault.py          # Business logic
├── models.py         # Dataclasses
├── config.py         # File paths
└── README.md         # Documentation
```

---

## 🏷️ Version History

### **v1.1 — Interactive Shell**
- Added persistent shell mode (`cli_shell.py`)
- No repeated password prompts
- Built‑in help command
- Unified syntax with one‑shot CLI

### **v1.0 — One‑Shot CLI**
- Initial release
- Add/list/search/remove commands
- Encrypted vault storage
- PBKDF2 key derivation
- Notes support

---

## 🛡️ Security Notes

- Your master password is **never stored**  
- Losing your master password makes the vault unrecoverable  
- Losing `vault.salt` also makes the vault unrecoverable  
- Everything stays local on your machine  

---
