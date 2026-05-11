import os

# URL del foro a scrapear. Se inyecta vía secret/env-var FORUM_BASE_URL para no
# acoplar el código a un foro concreto y no exponer el target en el repo público.
BASE_URL = os.environ.get("FORUM_BASE_URL", "").strip()
if not BASE_URL:
    raise RuntimeError(
        "FORUM_BASE_URL no está definida. Configúrala como secret en GitHub "
        "Actions (Settings → Secrets → Actions) o como variable de entorno local."
    )
if not BASE_URL.endswith("/"):
    BASE_URL += "/"

LIST_DIR = "lists"
COOKIES_FILE = os.path.join(LIST_DIR, "session.cookies")
ARTISTS_FILE = os.path.join(LIST_DIR, "artists.txt")
HISTORY_FILE = os.path.join(LIST_DIR, "history.json")
DELTA_FILE = os.path.join(LIST_DIR, "deltas.txt")
DELTA_JSONL_FILE = os.path.join(LIST_DIR, "deltas.jsonl")
OUTPUT_FILE = os.path.join(LIST_DIR, "final_list.txt")
FAILED_FILE = os.path.join(LIST_DIR, "failed_artists.json")
ARTISTS_INDEX_FILE = os.path.join(LIST_DIR, "artists_index.json")
SEEN_REMOVALS_FILE = os.path.join(LIST_DIR, "seen_removals.json")
PENDING_CHAPTERS_FILE = os.path.join(LIST_DIR, "pending_chapters.json")

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
# Backoff escalado ante rate limit detectado.
# Scraper: corto (185s total) — preferimos abortar el artista y seguir.
# Writer: largo (~55min total) — los capítulos rate-limited no son recuperables
# si el writer aborta antes de tiempo (history.json ya tiene el cambio del scrape).
RATE_LIMIT_BACKOFF = [5, 15, 45, 120]
WRITER_RATE_LIMIT_BACKOFF = [30, 120, 300, 900, 1800]
