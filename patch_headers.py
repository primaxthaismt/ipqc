import re
with open('api/index.py', 'r', encoding='utf-8') as f: code = f.read()

# Update the catchall to return headers
pattern = r'return \{"error": "CATCH_ALL", "method": request\.method, "url_path": request\.url\.path, "path_name": path_name\}'
replacement = r'return {"error": "CATCH_ALL", "headers": dict(request.headers), "url_path": request.url.path, "path_name": path_name}'

code = re.sub(pattern, replacement, code)
with open('api/index.py', 'w', encoding='utf-8') as f: f.write(code)
