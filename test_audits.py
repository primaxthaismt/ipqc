import urllib.request, json

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

audits = supabase_db_query("audits", params="select=*&order=audit_time.desc&limit=5")
print(json.dumps(audits, indent=2))
