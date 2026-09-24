import re
with open('api/index.py', 'r', encoding='utf-8') as f: code = f.read()
code = code.replace('app = FastAPI\\(title="Smart IPQC Digital Audit System API", version="2.0.0"\\)', 'app = FastAPI(title="Smart IPQC Digital Audit System API", version="2.0.0")')
with open('api/index.py', 'w', encoding='utf-8') as f: f.write(code)
