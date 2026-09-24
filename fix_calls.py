import re

with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace block 1
block1 = r"""      if \(res\.ok\) \{
        const data = await res\.json\(\);
        authToken = data\.token;
        localStorage\.setItem\('ipqc_token', authToken\);
        setCurrentUser\(data\.user\);
        document\.getElementById\('modal-login'\)\?\.classList\.remove\('active'\);
      \} else \{"""
replacement1 = """      if (res.ok) {
        const data = await res.json();
        authToken = data.token;
        localStorage.setItem('ipqc_token', authToken);
        animateLoginSuccess(() => {
          setCurrentUser(data.user);
        });
      } else {"""
code = re.sub(block1, replacement1, code, flags=re.MULTILINE)

# Replace block 2
block2 = r"""          setCurrentUser\(\{
            id: 'USR-ADMIN-01',
            username: 'admin',
            full_name: 'Norman Nan \(QA Manager\)',
            role: 'admin',
            line_assignment: 'All Lines'
          \}\);
          document\.getElementById\('modal-login'\)\?\.classList\.remove\('active'\);"""
replacement2 = """          animateLoginSuccess(() => {
            setCurrentUser({
              id: 'USR-ADMIN-01',
              username: 'admin',
              full_name: 'Norman Nan (QA Manager)',
              role: 'admin',
              line_assignment: 'All Lines'
            });
          });"""
code = re.sub(block2, replacement2, code, flags=re.MULTILINE)

# Replace block 3
block3 = r"""          setCurrentUser\(\{
            id: 'USR-AUD-01',
            username: username,
            full_name: username \+ ' \(IPQC Inspector\)',
            role: 'auditor',
            line_assignment: 'All Lines'
          \}\);
          document\.getElementById\('modal-login'\)\?\.classList\.remove\('active'\);"""
replacement3 = """          animateLoginSuccess(() => {
            setCurrentUser({
              id: 'USR-AUD-01',
              username: username,
              full_name: username + ' (IPQC Inspector)',
              role: 'auditor',
              line_assignment: 'All Lines'
            });
          });"""
code = re.sub(block3, replacement3, code, flags=re.MULTILINE)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
