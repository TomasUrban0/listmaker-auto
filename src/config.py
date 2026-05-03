import os

BASE_URL = "https://forum.questionablequesting.com/"

LIST_DIR = "lists"
COOKIES_FILE = os.path.join(LIST_DIR, "qq_verified_session.cookies")
ARTISTS_FILE = os.path.join(LIST_DIR, "artists.txt")
HISTORY_FILE = os.path.join(LIST_DIR, "history.json")
DELTA_FILE = os.path.join(LIST_DIR, "deltas.txt")
DELTA_JSONL_FILE = os.path.join(LIST_DIR, "deltas.jsonl")
OUTPUT_FILE = os.path.join(LIST_DIR, "final_list.txt")
FAILED_FILE = os.path.join(LIST_DIR, "failed_artists.json")
ARTISTS_INDEX_FILE = os.path.join(LIST_DIR, "artists_index.json")

LOCAL_FOLDER = "Artists"
DRIVE_TARGET_FOLDER = "Artists"
PARENT_DRIVE_ID = "root"
LISTS_FOLDER = "lists"

# ID directo de la carpeta `Artists` en Drive. Imprescindible cuando se usa
# Service Account, porque el SA no ve la carpeta bajo su 'root' (está en
# "Shared with me"). Si no se setea, caemos al lookup por nombre desde 'root'
# (modo legacy con auth de usuario normal).
ARTISTS_FOLDER_ID = os.environ.get("ARTISTS_FOLDER_ID", "").strip() or None

# Safety net contra paginación infinita
MAX_PAGES_PER_LOOP = 300
# Backoff escalado ante rate limit detectado
RATE_LIMIT_BACKOFF = [5, 15, 45, 120]
