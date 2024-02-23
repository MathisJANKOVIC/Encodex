import os

HOST = os.environ.get("HOST", "localhost")
PORT = os.environ.get("PORT", "8000")

BASE_URL = f"http://{HOST}:{PORT}"
