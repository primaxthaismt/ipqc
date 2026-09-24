import re
with open('api/index.py', 'r', encoding='utf-8') as f: code = f.read()

middleware_code = '''
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from urllib.parse import urlparse

class VercelPathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        vpath = request.query_params.get("_vpath")
        if vpath:
            request.scope["path"] = vpath
            # Optional: remove _vpath from query string so it doesn't mess with endpoints
            # But it's usually fine to leave it.
        return await call_next(request)

app.add_middleware(VercelPathMiddleware)
'''

pattern = r'app = FastAPI\(title="Smart IPQC Digital Audit System API", version="2.0.0"\)'
code = re.sub(pattern, pattern + middleware_code, code)

with open('api/index.py', 'w', encoding='utf-8') as f: f.write(code)
print("Middleware injected")
