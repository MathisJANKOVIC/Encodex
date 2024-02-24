import os

HOST = os.environ.get("HOST", "localhost")
PORT = os.environ.get("PORT", "8000")

BASE = f"http://{HOST}:{PORT}"

CREATE = f"{BASE}/encodex/create/"
UPDATE = f"{BASE}/encodex/update/"
