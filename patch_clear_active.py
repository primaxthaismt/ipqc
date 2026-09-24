import re
with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

pattern = r"if \(match\) match\.status = newStatus;"
replacement = """if (match) match.status = newStatus;
        
        // Clear active station so it doesn't reopen after submission
        activeStation = null;
        activeAuditData = {};"""

code = re.sub(pattern, replacement, code)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
