import re
with open('api/index.py', 'r', encoding='utf-8') as f: code = f.read()

pattern = r'details = supabase_db_query\("audit_details", params=f"audit_id=eq\.\{audit_id\}&select=\*"\)\s*if not isinstance\(details, list\): details = \[\]'

replacement = '''details = supabase_db_query("audit_details", params=f"audit_id=eq.{audit_id}&select=*")
    if not isinstance(details, list): details = []
    
    # Enrich with master questions
    master_items = get_master_data().get("all_items", [])
    for d in details:
        m = next((m for m in master_items if m.get("item_no") == d.get("item_no")), None)
        if m:
            d["question_en"] = m.get("en", "")
            d["category"] = m.get("process", "")'''

code = re.sub(pattern, replacement, code, flags=re.MULTILINE)
with open('api/index.py', 'w', encoding='utf-8') as f: f.write(code)
print('Patched preview')
