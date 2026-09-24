import re
with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r"if\s*\(selectedLayoutMode === 'option1'\)\s*\{\s*renderAuditFlow\([^)]+\);\s*\}\s*else\s*\{\s*document\.getElementById\('panel-map-layout'\)\.style\.display = 'block';\s*renderFactoryMap\(\);\s*\}"

replacement = """document.getElementById('panel-map-layout').style.display = 'block';
        renderFactoryMap();"""

code = re.sub(pattern, replacement, code)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
