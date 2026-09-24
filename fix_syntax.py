import re
with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# The incorrect string inserted:
target = """        } else {
            alert(`Audit Submitted Successfully! [ID: ${auditId}]`);
        }]`);
        }"""

# The correct string to replace it with:
replacement = """        } else {
            alert(`Audit Submitted Successfully! [ID: ${auditId}]`);
        }"""

code = code.replace(target, replacement)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
