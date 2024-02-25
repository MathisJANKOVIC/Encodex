import os

HOST = os.environ.get("HOST", "localhost")
PORT = os.environ.get("PORT", "8000")

BASE_URL = f"http://{HOST}:{PORT}"

CREATE_STANDARD = f"{BASE_URL}/encoding-standard/create"
UPDATE_STANDARD = f"{BASE_URL}/encoding-standard/update"
DELETE_STANDARD = f"{BASE_URL}/encoding-standard/delete"