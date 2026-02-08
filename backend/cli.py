import argparse
from getpass import getpass

from storage import load_salt, load_vault, save_vault
from crypto import derive_key
from vault import VaultManager
from config import SALT_FILE, VAULT_FILE


def main():
    parser = argparse.ArgumentParser(description="Password Vault CLI")

    sub = parser.add_subparsers(dest="command")

    # add
    add = sub.add_parser("add")
    add.add_argument("service")
    add.add_argument("username")
    add.add_argument("password")
    add.add_argument("notes", nargs="*", default=None)

    # list
    sub.add_parser("list")

    # search
    search = sub.add_parser("search")
    search.add_argument("query")

    # remove
    remove = sub.add_parser("remove")
    remove.add_argument("service")

    args = parser.parse_args()

    # ask for master password
    master = getpass("Master password: ")

    # load salt + derive key
    salt = load_salt(SALT_FILE)
    key = derive_key(master, salt)

    # load vault
    vault = load_vault(VAULT_FILE, key)
    mgr = VaultManager(vault)

    # dispatch commands
    if args.command == "add":
        notes = " ".join(args.notes) if args.notes else None
        mgr.add_entry(args.service, args.username, args.password, notes)
        save_vault(VAULT_FILE, vault, key)
        print("Entry added")

    elif args.command == "list":
        for e in mgr.list_entries():
            print(f"{e.service}: {e.username}")

    elif args.command == "search":
        results = mgr.find_entries(args.query)
        for e in results:
            print(f"{e.service}") 
            print(f"username: {e.username}")
            print(f"password: {e.password}")
            if e.notes:
                print(f"notes: {e.notes}")          

    elif args.command == "remove":
        if mgr.remove_entry(args.service):
            save_vault(VAULT_FILE, vault, key)
            print("Entry removed,")
        else:
            print("No such entry.")
    else:
        parser.print_help()        

if __name__ == "__main__":
    main()
