import uvicorn
import os
import sys

# Ensure UTF-8 output encoding on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure root directory is on Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.index import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8082))
    print(f"[IPQC] Starting Smart IPQC Digital Audit System on http://0.0.0.0:{port} ...")
    uvicorn.run("api.index:app", host="0.0.0.0", port=port, reload=False)
