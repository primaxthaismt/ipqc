import re
with open('public/js/app.js', 'r', encoding='utf-8') as f: code = f.read()

pattern = r'function startAuditForStation\(st\) \{\n\s*if \(\!st\) return;\n\s*activeStation = st;'
replacement = '''function startAuditForStation(st) {
  if (!st) return;
  
  if (st.status === 'OK' || st.status === 'NG') {
    const pwd = prompt("This station has already been audited for the current 2-hour time block.\\n\\nPlease enter Supervisor or Manager password to unlock re-audit:");
    if (!pwd || !['admin123', 'manager123', 'supervisor123', 'password123'].includes(pwd)) {
      alert("Invalid password. Re-audit unlock cancelled.");
      return;
    }
  }
  
  activeStation = st;'''

new_code = re.sub(pattern, replacement, code, flags=re.MULTILINE)
with open('public/js/app.js', 'w', encoding='utf-8') as f: f.write(new_code)
print('Patched app.js for re-audit')
