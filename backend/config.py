from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR/"data"

VAULT_FILE = DATA_DIR/ "vault.dat"
SALT_FILE = DATA_DIR/ "vault.salt"
