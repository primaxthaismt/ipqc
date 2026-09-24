import re
with open('api/index.py', 'r', encoding='utf-8') as f: code = f.read()
code = code.replace('      # MASTER PASSWORD OVERRIDE\n      password_valid =', '    # MASTER PASSWORD OVERRIDE\n    password_valid =')
code = code.replace('      if target_user and', '    if target_user and')
code = code.replace('          if data.password', '        if data.password')
code = code.replace('              password_valid', '            password_valid')
code = code.replace('      if not target_user or not password_valid:', '    if not target_user or not password_valid:')
code = code.replace('          raise HTTPException(status_code=401, detail="Invalid username or password")', '        raise HTTPException(status_code=401, detail="Invalid username or password")')
with open('api/index.py', 'w', encoding='utf-8') as f: f.write(code)
