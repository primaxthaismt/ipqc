with open('public/sw.js', 'r', encoding='utf-8') as f: code = f.read()
code = code.replace("CACHE_NAME = 'ipqc-prod-v16'", "CACHE_NAME = 'ipqc-prod-v17'")
with open('public/sw.js', 'w', encoding='utf-8') as f: f.write(code)
