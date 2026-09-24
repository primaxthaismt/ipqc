import re
with open('public/js/app.js', 'r', encoding='utf-8') as f: code = f.read()

# Replace the actual newlines inside the prompt string with \\n
# Let's just find the prompt call and fix it.
pattern = r'const pwd = prompt\("This station has already been audited for the current 2-hour time block\.\n\nPlease enter Supervisor or Manager password to unlock re-audit:"\);'
replacement = r'const pwd = prompt("This station has already been audited for the current 2-hour time block.\\n\\nPlease enter Supervisor or Manager password to unlock re-audit:");'
code = code.replace('const pwd = prompt("This station has already been audited for the current 2-hour time block.\n\nPlease enter Supervisor or Manager password to unlock re-audit:");', replacement)

with open('public/js/app.js', 'w', encoding='utf-8') as f: f.write(code)
