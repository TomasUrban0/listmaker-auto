"""Entry point: sube PDFs y estado de listas a Google Drive."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.uploader import GDriveUploader


def main():
    uploader = GDriveUploader()
    try:
        uploader.run()
    except KeyboardInterrupt:
        print("\nDetenido por el usuario.")
        sys.exit(130)


if __name__ == "__main__":
    main()
