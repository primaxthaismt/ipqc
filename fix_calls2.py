import re

with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace block 1
code = re.sub(
    r"setCurrentUser\(data\.user\);\s*document\.getElementById\('modal-login'\)\?\.classList\.remove\('active'\);",
    r"animateLoginSuccess(() => {\n          setCurrentUser(data.user);\n        });",
    code
)

# Replace block 2
code = re.sub(
    r"setCurrentUser\(\{\s*id: 'USR-ADMIN-01'.*?line_assignment: 'All Lines'\s*\}\);\s*document\.getElementById\('modal-login'\)\?\.classList\.remove\('active'\);",
    r"""animateLoginSuccess(() => {
            setCurrentUser({
              id: 'USR-ADMIN-01',
              username: 'admin',
              full_name: 'Norman Nan (QA Manager)',
              role: 'admin',
              line_assignment: 'All Lines'
            });
          });""",
    code,
    flags=re.DOTALL
)

# Replace block 3
code = re.sub(
    r"setCurrentUser\(\{\s*id: 'USR-AUD-01'.*?line_assignment: 'All Lines'\s*\}\);\s*document\.getElementById\('modal-login'\)\?\.classList\.remove\('active'\);",
    r"""animateLoginSuccess(() => {
            setCurrentUser({
              id: 'USR-AUD-01',
              username: username,
              full_name: username + ' (IPQC Inspector)',
              role: 'auditor',
              line_assignment: 'All Lines'
            });
          });""",
    code,
    flags=re.DOTALL
)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
