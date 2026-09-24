import re

with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r"const res = await apiFetch\('/api/audits'\);"
replacement = """const res = await apiFetch('/api/audits', {
      headers: { 'Authorization': `Bearer ${authToken}` }
    });"""

code = re.sub(pattern, replacement, code)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
