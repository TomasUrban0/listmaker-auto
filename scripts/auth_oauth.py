"""One-time OAuth flow to obtain a refresh token for the listmaker pipeline.

Reads ``oauth_client.json`` (downloaded from GCP, OAuth client of type
"Desktop app") in the repo root, opens a browser to authorize, and prints
the three values you need to set as GitHub secrets:

  GDRIVE_OAUTH_CLIENT_ID
  GDRIVE_OAUTH_CLIENT_SECRET
  GDRIVE_OAUTH_REFRESH_TOKEN

Run from the repo root:
    python scripts/auth_oauth.py

Prerequisites: ``oauth_client.json`` exists in the cwd; you have a browser
available; the email you authorize with is the owner of the Drive folder.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pydrive2.auth import GoogleAuth

OAUTH_CLIENT_FILE = "oauth_client.json"
TOKEN_FILE = "oauth_token.json"
SCOPE = ["https://www.googleapis.com/auth/drive"]


def main():
    if not Path(OAUTH_CLIENT_FILE).exists():
        print(f"ERROR: {OAUTH_CLIENT_FILE} no encontrado en el directorio actual.")
        print("Descárgalo desde GCP Console > Credentials > tu OAuth client > Download JSON")
        sys.exit(1)

    # Cargar client_id / client_secret del JSON
    with open(OAUTH_CLIENT_FILE) as f:
        client_config = json.load(f)
    # GCP envuelve el config en "installed" (Desktop app) o "web"
    inner = client_config.get("installed") or client_config.get("web")
    if not inner:
        print(f"ERROR: {OAUTH_CLIENT_FILE} no parece un OAuth client válido.")
        sys.exit(1)
    client_id = inner["client_id"]
    client_secret = inner["client_secret"]

    print("Abriendo navegador para autorizar...")
    print("Si Google avisa de 'app no verificada', click en 'Advanced' -> 'Go to app (unsafe)'.")
    print()

    gauth = GoogleAuth(settings={
        "client_config_backend": "settings",
        "client_config": {
            "client_id": client_id,
            "client_secret": client_secret,
        },
        "oauth_scope": SCOPE,
        "save_credentials": True,
        "save_credentials_backend": "file",
        "save_credentials_file": TOKEN_FILE,
        "get_refresh_token": True,
    })
    gauth.LocalWebserverAuth()
    gauth.SaveCredentialsFile(TOKEN_FILE)

    refresh_token = gauth.credentials.refresh_token
    if not refresh_token:
        print("ERROR: no se obtuvo refresh_token. Revoca acceso a la app en")
        print("https://myaccount.google.com/permissions y vuelve a intentarlo.")
        sys.exit(1)

    print()
    print("=" * 70)
    print("REFRESH TOKEN OBTENIDO. Configura estos 3 secrets en GitHub:")
    print("=" * 70)
    print()
    print(f"GDRIVE_OAUTH_CLIENT_ID={client_id}")
    print(f"GDRIVE_OAUTH_CLIENT_SECRET={client_secret}")
    print(f"GDRIVE_OAUTH_REFRESH_TOKEN={refresh_token}")
    print()
    print(f"(También guardado en {TOKEN_FILE} por si los pierdes — gitignored)")


if __name__ == "__main__":
    main()
