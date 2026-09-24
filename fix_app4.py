import re

with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

code = re.sub(r"apiFetch\(`/api/users`,", r"apiFetch(`/api/users?t=${Date.now()}`,", code)
code = re.sub(r"apiFetch\('/api/users',", r"apiFetch(`/api/users?t=${Date.now()}`,", code)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
