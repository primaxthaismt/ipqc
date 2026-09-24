import re
with open('api/index.py', 'r', encoding='utf-8') as f: code = f.read()

# Remove the catch-all from the top
code = code.replace('''from fastapi import Request\n@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])\nasync def catch_all(request: Request, path_name: str):\n    return {"method": request.method, "url_path": request.url.path, "path_name": path_name}\n''', '')

# Add it to the bottom
code += '''\nfrom fastapi import Request\n@app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])\nasync def catch_all(request: Request, path_name: str):\n    return {"error": "CATCH_ALL", "method": request.method, "url_path": request.url.path, "path_name": path_name}\n'''

with open('api/index.py', 'w', encoding='utf-8') as f: f.write(code)
