with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = """    try {
      const res = await apiFetch(`/api/users`, {
        headers: { 'Authorization': `Bearer ${authToken}` }
      });
      if (res.ok) users = await res.json();
    } catch (e) {}"""

replacement = """    try {
      const res = await apiFetch(`/api/users?t=${Date.now()}`, {
        headers: { 'Authorization': `Bearer ${authToken}` }
      });
      if (res.ok) users = await res.json();
    } catch (e) {}"""

code = code.replace(pattern, replacement)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
