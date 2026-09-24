with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

bad_str = """    if (loginBtn) loginBtn.textContent = '登录 System Login';
  }
}  apiFetch('/api/auth/logout', {"""

good_str = """    if (loginBtn) loginBtn.textContent = '登录 System Login';
  }
}

function handleLogoutSubmit() {
  if (authToken) {
    apiFetch('/api/auth/logout', {"""

code = code.replace(bad_str, good_str)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed handleLogoutSubmit definition")
