"""Entry point: descarga PDFs de capítulos nuevos según el último delta."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.bootstrap import bootstrap_state
from src.writer import QQWriter


def main():
    bootstrap_state()
    bot = QQWriter()
    exit_code = 0
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\nDetenido.")
        exit_code = 130
    except RuntimeError as e:
        print(f"\nAbortado por rate limit: {e}")
        exit_code = 3
    finally:
        bot.close()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
