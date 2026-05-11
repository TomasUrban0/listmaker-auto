"""Materializa archivos de estado desde env-vars base64.

En CI el primer run no tiene `lists/session.cookies` (Drive vacío) —
las cookies se inyectan vía secret FORUM_COOKIES_B64. Lo mismo aplica opcionalmente
a `artists.txt` vía ARTISTS_TXT_B64.

Llamado desde los entry points de scrape/write antes de instanciar el bot.
"""
import base64
import os

from .config import ARTISTS_FILE, COOKIES_FILE, LIST_DIR


def _materialize(env_var: str, dest_path: str, label: str) -> bool:
    """Decodifica el contenido base64 de *env_var* y lo escribe en *dest_path*.

    Devuelve True si materializó el archivo, False si no había env-var o ya existía.
    """
    if os.path.exists(dest_path):
        return False
    raw = os.environ.get(env_var)
    if not raw:
        return False
    try:
        data = base64.b64decode(raw)
    except Exception as e:
        print(f"{env_var} no decodifica como base64: {e}")
        return False
    os.makedirs(os.path.dirname(dest_path) or ".", exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(data)
    print(f"{label} materializado desde {env_var} ({len(data)} bytes) en {dest_path}")
    return True


def bootstrap_state():
    """Materializa cookies y (si está disponible) artists.txt desde env-vars."""
    os.makedirs(LIST_DIR, exist_ok=True)
    _materialize("FORUM_COOKIES_B64", COOKIES_FILE, "Cookies")
    _materialize("ARTISTS_TXT_B64", ARTISTS_FILE, "artists.txt")
