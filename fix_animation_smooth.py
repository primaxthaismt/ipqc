import re

with open('public/js/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the display: none part
pattern = r"""  if \(formContent\) \{
    formContent\.style\.opacity = '0';
    setTimeout\(\(\) => \{
      formContent\.style\.display = 'none';
    \}, 500\);
  \}"""

replacement = """  if (formContent) {
    formContent.style.opacity = '0';
    formContent.style.pointerEvents = 'none';
  }"""
code = re.sub(pattern, replacement, code)

# Fix the lock animation transform
pattern_icon = r"icon\.style\.transform = 'scale\(4\) translateY\(20px\)';"
replacement_icon = r"icon.style.transform = 'translateY(80px) scale(4)';"
code = re.sub(pattern_icon, replacement_icon, code)

# Fix the reset part
pattern_reset = r"""      if \(formContent\) \{
        formContent\.style\.display = 'block';
        setTimeout\(\(\) => formContent\.style\.opacity = '1', 50\);
      \}"""
replacement_reset = """      if (formContent) {
        formContent.style.pointerEvents = 'auto';
        formContent.style.opacity = '1';
      }"""
code = re.sub(pattern_reset, replacement_reset, code)


with open('public/js/app.js', 'w', encoding='utf-8') as f:
    f.write(code)
