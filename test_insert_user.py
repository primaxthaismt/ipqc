import urllib.request, json
import hashlib

SUPABASE_URL = "https://yfpowaudcciepubtjkdr.supabase.co"
SUPABASE_KEY = "sb_publishable_shOnteL2raHE5OynKjPkPw_aHX3vp5F"

def supabase_db_query(endpoint: str, method: str = "GET", data: dict = None, params: str = ""):
    url = f"{SUPABASE_URL}/rest/v1/{endpoint}"
    if params:
        url += f"?{params}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=5) as resp:
        res_body = resp.read().decode("utf-8")
        return json.loads(res_body) if res_body else []

pw_hash = hashlib.sha256("123456".encode()).hexdigest()

new_user = {
    "id": "USR-ADM-123456",
    "username": "08001104",
    "password_hash": pw_hash,
    "full_name": "norman",
    "role": "admin",
    "line_assignment": "All Lines",
    "language_pref": "zh",
    "is_active": True
}

try:
    print(supabase_db_query("users", method="POST", data=new_user))
except urllib.error.HTTPError as e:
    print(f"Error {e.code}: {e.read().decode('utf-8')}")
