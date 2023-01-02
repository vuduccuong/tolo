from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOGGING = {
    "version": 1,
    "handlers": {
        "file": {
            "level": "WARNING",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs/warning.log",
        }
    },
}
