import re
with open('api/[...path].py', 'r', encoding='utf-8') as f: code = f.read()

pattern1 = r'from fastapi import Request\n@app\.api_route\("/\{path_name:path\}", methods=\["GET", "POST", "PUT", "DELETE", "OPTIONS"\]\)\nasync def catch_all\(request: Request, path_name: str\):\n    return \{"error": "CATCH_ALL", "headers": dict\(request\.headers\), "url_path": request\.url\.path, "path_name": path_name\}\n'
code = re.sub(pattern1, '', code)

pattern2 = r'class VercelPathMiddleware\(BaseHTTPMiddleware\):.*?\napp\.add_middleware\(VercelPathMiddleware\)'
code = re.sub(pattern2, '', code, flags=re.DOTALL)

with open('api/[...path].py', 'w', encoding='utf-8') as f: f.write(code)
print("Cleaned up [...path].py")
