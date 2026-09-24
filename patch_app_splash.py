import re

with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

new_animate_function = """function animateLoginSuccess(user, callback) {
  // If only callback passed
  if (typeof user === 'function') {
    callback = user;
    user = null;
  }

  // 1. Immediately hide login modal so NO OTHER MODAL/LOCK exists behind
  const loginModal = document.getElementById('modal-login');
  if (loginModal) loginModal.classList.remove('active');

  // 2. Activate the dedicated fullscreen unlock splash screen
  const splash = document.getElementById('unlock-splash-overlay');
  const svg = document.getElementById('unlock-svg');
  const title = document.getElementById('unlock-title');
  const subtitle = document.getElementById('unlock-subtitle');

  if (subtitle && user) {
    subtitle.textContent = `Welcome, ${user.full_name || user.username} • Smart IPQC System`;
  }
  if (title) {
    title.textContent = 'VERIFYING CREDENTIALS';
    title.style.color = '#38bdf8';
  }

  if (splash && svg) {
    svg.classList.remove('unlocked');
    splash.classList.remove('unlocked');
    splash.style.display = 'flex';
    
    // Force browser reflow
    void splash.offsetWidth;
    splash.classList.add('active');

    // After 0.6s: Pop unlock the shackle & turn glowing green
    setTimeout(() => {
      svg.classList.add('unlocked');
      splash.classList.add('unlocked');
      if (title) {
        title.textContent = 'SYSTEM UNLOCKED';
      }
      if (window.confetti) {
        try {
          confetti({
            particleCount: 50,
            spread: 70,
            origin: { y: 0.55 },
            colors: ['#34d399', '#38bdf8', '#60a5fa']
          });
        } catch(e){}
      }
    }, 600);

    // After 2.5s: Smoothly fade out the splash screen
    setTimeout(() => {
      splash.classList.remove('active');
    }, 2500);

    // After 3.0s: Clean up splash display and finalize user state
    setTimeout(() => {
      splash.style.display = 'none';
      if (svg) svg.classList.remove('unlocked');
      if (splash) splash.classList.remove('unlocked');
      if (callback) callback();
    }, 3000);
  } else {
    if (callback) callback();
  }
}"""

# Replace the animateLoginSuccess definition
pattern_animate = r'function animateLoginSuccess\(callback\) \{.*?async function handleLoginSubmit\(\) \{'
new_animate_section = new_animate_function + "\n\nasync function handleLoginSubmit() {"

code = re.sub(pattern_animate, new_animate_section, code, flags=re.DOTALL)

# Update call inside handleLoginSubmit
code = re.sub(
    r'animateLoginSuccess\(\(\) => \{\s*setCurrentUser\(data\.user\);\s*\}\);',
    r'animateLoginSuccess(data.user, () => {\n        setCurrentUser(data.user);\n      });',
    code
)

code = re.sub(
    r'animateLoginSuccess\(\(\) => \{\s*setCurrentUser\(\{\s*id: \'USR-ADMIN-01\',',
    r'const adminUser = { id: \'USR-ADMIN-01\', username: \'admin\', full_name: \'Norman Nan (QA Manager)\', role: \'admin\', line_assignment: \'All Lines\' };\n        animateLoginSuccess(adminUser, () => {\n          setCurrentUser(adminUser);\n          //',
    code
)

with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated app.js successfully")
