"""
IPQC FAI/LAI Module — Standalone Server
Cloned from ipqc-v2 into ipqc-v1/FAI

Run:   python server.py
Access: http://localhost:8001

This is a self-contained First & Last Article Inspection module
extracted from the Smart IPQC v2 system.
"""
import sys
import os

# Resolve paths so imports work correctly from this directory
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

# Load the FAI API module (fai_api.py = copy of ipqc-v2 api/index.py)
import importlib.util
api_path = os.path.join(current_dir, "api", "fai_api.py")
spec = importlib.util.spec_from_file_location("fai_api_mod", api_path)
api_module = importlib.util.module_from_spec(spec)
sys.modules["fai_api_mod"] = api_module
# Also register as 'api.index' so internal imports resolve
sys.modules["api_index_mod"] = api_module
spec.loader.exec_module(api_module)

# Also load pcba_inspection_service so the router can include it
pcba_path = os.path.join(current_dir, "api", "pcba_inspection_service.py")
pcba_spec = importlib.util.spec_from_file_location("api.pcba_inspection_service", pcba_path)
pcba_module = importlib.util.module_from_spec(pcba_spec)
sys.modules["api.pcba_inspection_service"] = pcba_module
pcba_spec.loader.exec_module(pcba_module)

# Get router and middleware
parent_router = api_module.router
VercelPathMiddleware = api_module.VercelPathMiddleware

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware

fai_app = FastAPI(title="Smart IPQC — FAI/LAI Module (ipqc-v1)")

fai_app.add_middleware(VercelPathMiddleware)
fai_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class NoCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

fai_app.add_middleware(NoCacheMiddleware)

# Include all API routes
fai_app.include_router(parent_router, prefix="/api")
fai_app.include_router(parent_router, prefix="")

# Serve static files from the FAI public directory
public_dir = os.path.join(current_dir, "public")
css_dir = os.path.join(public_dir, "css")
js_dir = os.path.join(public_dir, "js")

if os.path.exists(css_dir):
    fai_app.mount("/css", StaticFiles(directory=css_dir), name="css-fai")
if os.path.exists(js_dir):
    fai_app.mount("/js", StaticFiles(directory=js_dir), name="js-fai")
fai_app.mount("/", StaticFiles(directory=public_dir, html=True), name="static-fai")

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*65)
    print("  Smart IPQC — FAI/LAI Module (ipqc-v1/FAI)")
    print("  URL:  http://localhost:8001")
    print("  Stop: Ctrl+C")
    print("="*65 + "\n")
    uvicorn.run(fai_app, host="0.0.0.0", port=8001, reload=False, log_level="info")
