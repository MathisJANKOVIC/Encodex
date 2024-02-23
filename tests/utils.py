from requests.models import Response
import os

HOST = os.environ.get("HOST", "localhost")
PORT = os.environ.get("PORT", "8000")

BASE_URL = f"http://{HOST}:{PORT}"

def failure_message(response: Response):
    return response.json().get("detail") or response.text