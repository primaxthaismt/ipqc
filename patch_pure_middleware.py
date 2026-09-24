import re
with open('api/index.py', 'r', encoding='utf-8') as f: code = f.read()

pattern = r'from starlette\.middleware\.base import BaseHTTPMiddleware.*?app\.add_middleware\(VercelPathMiddleware\)'

replacement = '''
class VercelPathMiddleware:
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            query = scope.get("query_string", b"").decode("utf-8")
            from urllib.parse import parse_qs
            qs = parse_qs(query)
            if "_vpath" in qs:
                scope["path"] = qs["_vpath"][0]
        await self.app(scope, receive, send)

app.add_middleware(VercelPathMiddleware)
'''
code = re.sub(pattern, replacement, code, flags=re.DOTALL)

with open('api/index.py', 'w', encoding='utf-8') as f: f.write(code)
