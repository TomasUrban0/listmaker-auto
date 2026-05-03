import json
import os

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive


def get_drive(service_account_json_path: str | None = None) -> GoogleDrive:
    """Authenticate with Google Drive using a Service Account.

    Resolution order for the SA credentials:
    1. Explicit *service_account_json_path* argument.
    2. ``GDRIVE_SA_JSON`` env-var containing the raw JSON string
       (GitHub Actions injects secrets this way).
    3. A ``service_account.json`` file in the working directory.
    """
    sa_path = service_account_json_path
    if sa_path is None:
        raw_json = os.environ.get("GDRIVE_SA_JSON")
        if raw_json:
            sa_path = "_sa_tmp.json"
            with open(sa_path, "w") as f:
                f.write(raw_json)
        elif os.path.exists("service_account.json"):
            sa_path = "service_account.json"
        else:
            raise RuntimeError(
                "No Service Account credentials found. "
                "Set GDRIVE_SA_JSON env-var or provide service_account.json."
            )

    gauth = GoogleAuth(settings={
        "client_config_backend": "service",
        "service_config": {
            "client_json_file_path": sa_path,
        },
        "oauth_scope": ["https://www.googleapis.com/auth/drive"],
    })
    gauth.ServiceAuth()

    drive = GoogleDrive(gauth)
    try:
        email = drive.GetAbout().get("user", {}).get("emailAddress", "?")
        print(f"Drive account: {email}")
    except Exception:
        pass
    return drive
