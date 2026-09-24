import re
with open('public/js/app.js', 'r', encoding='utf-8') as f: code = f.read()

pattern = r"\} else if \(auditedSet\.has\(stCode\)\) \{"
replacement = r"} else if (st.status === 'OK' || auditedSet.has(stCode)) {"

code = re.sub(pattern, replacement, code)
with open('public/js/app.js', 'w', encoding='utf-8') as f: f.write(code)
