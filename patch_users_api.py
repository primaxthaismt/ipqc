import re

with open('api/index.py', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r"""@router\.post\("/auth/logout"\)
def logout\(authorization: Optional\[str\] = Header\(None\)\):
    if authorization and authorization\.startswith\("Bearer "\):
        token = authorization\.split\(" "\)\[1\]
        SESSIONS_DB\.pop\(token, None\)
    return \{"status": "SUCCESS"\}"""

replacement = """@router.post("/auth/logout")
def logout(authorization: Optional[str] = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        SESSIONS_DB.pop(token, None)
    return {"status": "SUCCESS"}

# USER MANAGEMENT ENDPOINTS
@router.get("/users")
def get_users(user=Depends(require_role(['admin']))):
    users = supabase_db_query("users", params="select=id,username,full_name,role,line_assignment,language_pref,is_active,email")
    if not isinstance(users, list): users = []
    return users

@router.post("/users")
def create_user(data: dict, user=Depends(require_role(['admin']))):
    clean_username = data.get("username", "").strip()
    if not clean_username:
        raise HTTPException(status_code=400, detail="Username is required")
        
    existing_db = supabase_db_query("users", params=f"username=eq.{clean_username}&select=id")
    if existing_db and len(existing_db) > 0:
        raise HTTPException(status_code=400, detail="Username already exists")
        
    pw_hash = hash_password(data.get("password", "123456"))
    import secrets
    user_id = f"USR-{data.get('role', 'aud').upper()[:3]}-{secrets.token_hex(3).upper()}"
    
    new_user = {
        "id": user_id,
        "username": clean_username,
        "password_hash": pw_hash,
        "full_name": data.get("full_name", "").strip(),
        "role": data.get("role", "auditor"),
        "line_assignment": data.get("line_assignment", "All Lines"),
        "language_pref": data.get("language_pref", "zh"),
        "email": data.get("email", ""),
        "is_active": True
    }
    
    supabase_db_query("users", method="POST", data=new_user)
    return {"status": "SUCCESS", "user": new_user}"""

code = re.sub(pattern, replacement, code)

with open('api/index.py', 'w', encoding='utf-8') as f:
    f.write(code)
