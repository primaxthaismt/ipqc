import re
with open('api/index.py', 'r', encoding='utf-8') as f: code = f.read()

pattern = r'# Initialize FastAPI App\napp = FastAPI\(title="Smart IPQC Digital Audit System API", version="2.0.0"\)'
replacement = '''# Initialize FastAPI App
app = FastAPI(title="Smart IPQC Digital Audit System API", version="2.0.0")

from fastapi import Request
@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])
async def catch_all(request: Request, path_name: str):
    return {"method": request.method, "url_path": request.url.path, "path_name": path_name}
'''
code = re.sub(pattern, replacement, code, count=1)
with open('api/index.py', 'w', encoding='utf-8') as f: f.write(code)
