import re
with open('api/index.py', 'r', encoding='utf-8') as f: code = f.read()

middleware_code = '''
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

class VercelPathMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Vercel now rewrites the path to /api/index.py, but we want the original URL path
        # The original path is usually in request.url.path or x-now-route
        original_path = request.headers.get("x-vercel-forwarded-for-path") or request.scope.get("raw_path", b"").decode("utf-8")
        
        # We can just extract it from the ASGI scope's raw URI or headers
        # Actually, Vercel sets request.scope['path'] to /api/index.py
        # But the original request path is in the header 'x-invoke-path' or similar, or we can reconstruct it.
        # Let's just blindly replace /api/index.py with the real path from request.url!
        
        # Let's see if we can just use the path from the request URL
        path = request.url.path
        if request.scope["path"] == "/api/index.py" or request.scope["path"] == "/index.py":
            request.scope["path"] = path
            
        return await call_next(request)

app.add_middleware(VercelPathMiddleware)
'''

# Insert middleware after app = FastAPI(...)
pattern = r'app = FastAPI\(title="Smart IPQC Digital Audit System API", version="2.0.0"\)'
code = re.sub(pattern, pattern + middleware_code, code)

with open('api/index.py', 'w', encoding='utf-8') as f: f.write(code)
print("Middleware injected")
