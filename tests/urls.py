import os
from pickle import GET

HOST = os.environ.get("HOST", "localhost")
PORT = os.environ.get("PORT", "8000")

BASE_URL = f"http://{HOST}:{PORT}"

GET_STANDARDS = f"{BASE_URL}/encoding-standard"
CREATE_STANDARD = f"{BASE_URL}/encoding-standard/create"
UPDATE_STANDARD = f"{BASE_URL}/encoding-standard/update"
DELETE_STANDARD = f"{BASE_URL}/encoding-standard/delete"

ENCODE = f"{BASE_URL}/encoding-standard/encode"
DECODE = f"{BASE_URL}/encoding-standard/decode"