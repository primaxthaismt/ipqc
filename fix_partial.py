import re
with open('api/index.py', 'r', encoding='utf-8') as f: code = f.read()

pattern = r'latest_audit = sorted\(s_audits, key=lambda x: x\.get\("audit_time", ""\), reverse=True\)\[0\].*?s\["status"\] = latest_audit\.get\("overall_status", "OK"\)'

replacement = 'latest_audit = sorted(s_audits, key=lambda x: x.get("audit_time", ""), reverse=True)[0]\n                s["status"] = latest_audit.get("overall_status", "OK")'

new_code = re.sub(pattern, replacement, code, flags=re.DOTALL)
if new_code != code:
    with open('api/index.py', 'w', encoding='utf-8') as f:
        f.write(new_code)
    print('Patched api/index.py')
else:
    print('Failed to patch api/index.py')
