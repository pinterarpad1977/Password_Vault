from getpass import getpass

from storage import load_salt, load_vault, save_vault
from crypto import derive_key
from vault import VaultManager
from config import SALT_FILE, VAULT_FILE


def interactive_shell(mgr, key):
    print("Vault shell started. Type 'help' for commands, 'exit' to quit.")

    while True:
        cmd = input("vault> ").strip()

        if cmd in ("exit", "quit"):
            print("Goodbye.")
            break

        if cmd == "help":
            print("""
Commands:
  add <service> <username> <password> [notes...]   Add a new entry
  list                                             List all entries
  search <query>                                   Search entries (shows passwords)
  remove <service>                                 Remove an entry
  exit                                             Quit the shell
""")
            continue

        parts = cmd.split()
        if not parts:
            continue

        command = parts[0]

        try:
            if command == "add":
                if len(parts) < 4:
                    print("Usage: add <service> <username> <password> [notes...]")
                    continue

                service = parts[1]
                username = parts[2]
                password = parts[3]
                notes = " ".join(parts[4:]) if len(parts) > 4 else None

                mgr.add_entry(service, username, password, notes)
                save_vault(VAULT_FILE, mgr.vault, key)
                print("Entry added.")

            elif command == "list":
                entries = mgr.list_entries()
                if not entries:
                    print("Vault is empty.")
                else:
                    for e in entries:
                        print(f"{e.service}: {e.username}")

            elif command == "search":
                if len(parts) < 2:
                    print("Usage: search <query>")
                    continue

                query = parts[1]
                results = mgr.find_entries(query)

                if not results:
                    print("No matching entries.")
                else:
                    for e in results:
                        print(f"{e.service}")
                        print(f"  username: {e.username}")
                        print(f"  password: {e.password}")
                        if e.notes:
                            print(f"  notes: {e.notes}")

            elif command == "remove":
                if len(parts) < 2:
                    print("Usage: remove <service>")
                    continue

                service = parts[1]
                if mgr.remove_entry(service):
                    save_vault(VAULT_FILE, mgr.vault, key)
                    print("Entry removed.")
                else:
                    print("No such entry.")

            else:
                print("Unknown command. Type 'help'.")

        except Exception as e:
            print("Error:", e)


def main():
    print("Password Vault Shell")
    master = getpass("Master password: ")

    salt = load_salt(SALT_FILE)
    key = derive_key(master, salt)

    vault = load_vault(VAULT_FILE, key)
    mgr = VaultManager(vault)

    interactive_shell(mgr, key)


if __name__ == "__main__":
    main()
