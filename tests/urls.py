import os

HOST = os.environ.get("HOST", "localhost")
PORT = os.environ.get("PORT", "8000")

BASE_URL = f"http://{HOST}:{PORT}"

ENCODE = f"{BASE_URL}/encoding-standard/encode"
DECODE = f"{BASE_URL}/encoding-standard/decode"

GET_STANDARDS = f"{BASE_URL}/encoding-standard"
CREATE_STANDARD = f"{BASE_URL}/encoding-standard/create"
UPDATE_STANDARD = f"{BASE_URL}/encoding-standard/update"
DELETE_STANDARD = f"{BASE_URL}/encoding-standard/delete"
RENAME_STANDARD = f"{BASE_URL}/encoding-standard/rename"
