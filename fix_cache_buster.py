import re

with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

code = re.sub(r"apiFetch\(`/api/users`,", r"apiFetch(`/api/users?t=${Date.now()}`,", code)
code = re.sub(r"apiFetch\('/api/users',", r"apiFetch(`/api/users?t=${Date.now()}`,", code)

# also fix the fast refresh issue on logout cache by updating the quick login if it exists, wait quicklogin is removed in index.html already.

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
