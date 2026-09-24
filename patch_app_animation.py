import re

with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

animation_function = """function animateLoginSuccess(callback) {
  const icon = document.getElementById('login-lock-icon');
  if (icon) {
    icon.textContent = '🔓';
    icon.style.transform = 'scale(1.8) translateY(-10px)';
  }
  const title = document.getElementById('txt-loginModalTitle');
  if (title) {
    title.textContent = 'Login Successful / 登录成功';
    title.style.color = '#34d399';
  }
  const loginBtn = document.getElementById('btn-submit-login');
  if (loginBtn) {
    loginBtn.style.background = '#34d399';
    loginBtn.style.borderColor = '#34d399';
    loginBtn.textContent = 'Access Granted ✔️';
  }
  setTimeout(() => {
    document.getElementById('modal-login')?.classList.remove('active');
    if (callback) callback();
    // Reset modal for future logout
    setTimeout(() => {
      if (icon) {
        icon.textContent = '🔒';
        icon.style.transform = 'scale(1) translateY(0)';
      }
      if (title) {
        title.textContent = '登录 Smart IPQC 系统';
        title.style.color = '#fff';
      }
      if (loginBtn) {
        loginBtn.style.background = '';
        loginBtn.style.borderColor = '';
        loginBtn.innerHTML = '<span id="txt-loginBtn">登录 System Login</span>';
      }
    }, 1000);
  }, 3000);
}

async function handleLoginSubmit() {"""

code = code.replace("async function handleLoginSubmit() {", animation_function)

# Now modify the handleLoginSubmit success paths
pattern_success1 = """      if (res.ok) {
        const data = await res.json();
        authToken = data.token;
        localStorage.setItem('ipqc_token', authToken);
        setCurrentUser(data.user);
        document.getElementById('modal-login')?.classList.remove('active');
      } else {"""
replacement_success1 = """      if (res.ok) {
        const data = await res.json();
        authToken = data.token;
        localStorage.setItem('ipqc_token', authToken);
        animateLoginSuccess(() => {
          setCurrentUser(data.user);
        });
      } else {"""
code = code.replace(pattern_success1, replacement_success1)

pattern_success2 = """          setCurrentUser({
            id: 'USR-ADMIN-01',
            username: 'admin',
            full_name: 'Norman Nan (QA Manager)',
            role: 'admin',
            line_assignment: 'All Lines'
          });
          document.getElementById('modal-login')?.classList.remove('active');"""
replacement_success2 = """          animateLoginSuccess(() => {
            setCurrentUser({
              id: 'USR-ADMIN-01',
              username: 'admin',
              full_name: 'Norman Nan (QA Manager)',
              role: 'admin',
              line_assignment: 'All Lines'
            });
          });"""
code = code.replace(pattern_success2, replacement_success2)

pattern_success3 = """          setCurrentUser({
            id: 'USR-AUD-01',
            username: username,
            full_name: username + ' (IPQC Inspector)',
            role: 'auditor',
            line_assignment: 'All Lines'
          });
          document.getElementById('modal-login')?.classList.remove('active');"""
replacement_success3 = """          animateLoginSuccess(() => {
            setCurrentUser({
              id: 'USR-AUD-01',
              username: username,
              full_name: username + ' (IPQC Inspector)',
              role: 'auditor',
              line_assignment: 'All Lines'
            });
          });"""
code = code.replace(pattern_success3, replacement_success3)

# And remove quickLogin function since we deleted it
pattern_quick_login = r"function quickLogin\(u, p\) \{.*?\}"
code = re.sub(pattern_quick_login, "", code, flags=re.DOTALL)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
