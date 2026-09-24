import re
with open('public/sw.js', 'r', encoding='utf-8') as f: code = f.read()
code = re.sub(r"CACHE_NAME = 'ipqc-prod-v\d+'", "CACHE_NAME = 'ipqc-prod-v29'", code)
with open('public/sw.js', 'w', encoding='utf-8') as f: f.write(code)
