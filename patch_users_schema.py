import re

with open('api/index.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix GET /api/users
pattern_get = r'users = supabase_db_query\("users", params="select=id,username,full_name,role,line_assignment,language_pref,is_active,email"\)'
replacement_get = 'users = supabase_db_query("users", params="select=id,username,full_name,role,line_assignment,language_pref,is_active")'
code = re.sub(pattern_get, replacement_get, code)

# Fix POST /api/users
pattern_post = r'''    new_user = \{
        "id": user_id,
        "username": clean_username,
        "password_hash": pw_hash,
        "full_name": data\.get\("full_name", ""\)\.strip\(\),
        "role": data\.get\("role", "auditor"\),
        "line_assignment": data\.get\("line_assignment", "All Lines"\),
        "language_pref": data\.get\("language_pref", "zh"\),
        "email": data\.get\("email", ""\),
        "is_active": True
    \}'''
replacement_post = '''    new_user = {
        "id": user_id,
        "username": clean_username,
        "password_hash": pw_hash,
        "full_name": data.get("full_name", "").strip(),
        "role": data.get("role", "auditor"),
        "line_assignment": data.get("line_assignment", "All Lines"),
        "language_pref": data.get("language_pref", "zh"),
        "is_active": True
    }'''
code = re.sub(pattern_post, replacement_post, code)

# Fix POST /auth/register
pattern_register = r'''      new_user = \{
          "id": user_id,
          "username": clean_username,
          "password_hash": pw_hash,
          "full_name": data\.full_name\.strip\(\),
          "role": "auditor", # Production inspector default role
          "line_assignment": data\.line_assignment or "All Lines",
          "language_pref": data\.language_pref or "en",
          "email": data\.email\.strip\(\) if data\.email else "",
          "is_active": True
      \}'''
replacement_register = '''      new_user = {
          "id": user_id,
          "username": clean_username,
          "password_hash": pw_hash,
          "full_name": data.full_name.strip(),
          "role": "auditor", # Production inspector default role
          "line_assignment": data.line_assignment or "All Lines",
          "language_pref": data.language_pref or "en",
          "is_active": True
      }'''
code = re.sub(pattern_register, replacement_register, code)

with open('api/index.py', 'w', encoding='utf-8') as f:
    f.write(code)
