import re

with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix the syntax error
code = code.replace('\/api/users?t=${Date.now()}"', "`/api/users?t=${Date.now()}`")
code = code.replace("const res = await apiFetch(`/api/users?t=${Date.now()}`", "const res = await apiFetch(`/api/users`") # Undo POST
code = code.replace("""    try {
      const res = await apiFetch(`/api/users`, {
        headers: { 'Authorization': `Bearer ${authToken}` }
      });""", """    try {
      const res = await apiFetch(`/api/users?t=${Date.now()}`, {
        headers: { 'Authorization': `Bearer ${authToken}` }
      });""")

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
