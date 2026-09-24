import re

with open('public/js/app.js', 'r', encoding='utf-8') as f: code = f.read()

pattern = r'if \(res\.ok\) \{\s*const data = await res\.json\(\);\s*alert\(`\$\{\s*translations\[currentLang\]\?.auditSuccess \|\| \'Audit Submitted Successfully!\'\s*\}\s*\[ID: \$\{auditId\}\]`\);\s*if \(activeStation\)'

replacement = '''if (res.ok) {
      const data = await res.json();
      
      if (confirm(`${translations[currentLang]?.auditSuccess || 'Audit Submitted Successfully!'} [ID: ${auditId}]\\n\\nWould you like to generate and preview the formal Audit Report (PDF/HTML) to send to Management?`)) {
          openEmailModal('audit', auditId);
      }
      
      if (activeStation)'''

code = re.sub(pattern, replacement, code, flags=re.MULTILINE)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
print('Patched app.js')
