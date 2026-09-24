import re
with open('api/index.py', 'r', encoding='utf-8') as f: code = f.read()

pattern = r'"category": master_item\.get\("process"\) if master_item else "",\s*"question_zh": master_item\.get\("zh"\) if master_item else "",\s*"question_en": master_item\.get\("en"\) if master_item else "",'
code = re.sub(pattern, '', code, flags=re.MULTILINE)

with open('api/index.py', 'w', encoding='utf-8') as f: f.write(code)
print('Patched api/index.py')
