import re
with open('public/js/app.js', 'r', encoding='utf-8') as f: code = f.read()

pattern = r'const totalQuestions = document.querySelectorAll\(\'.audit-item-row\'\)\.length;\s*const isPartial = details\.length < totalQuestions;\s*const hasNG = details\.some\(d => d\.result === \'X\'\);\s*let newStatus = \'OK\';\s*if \(hasNG\) newStatus = \'NG\';\s*else if \(isPartial\) newStatus = \'PARTIAL\';'

replacement = '''const totalQuestions = document.querySelectorAll('.audit-item-row').length;
  const isPartial = details.length < totalQuestions;
  const hasNG = details.some(d => d.result === 'X');
  let newStatus = 'OK';
  if (hasNG) newStatus = 'NG';
  else if (isPartial) newStatus = 'PARTIAL';
  
  const passCount = details.filter(d => d.result === 'O').length;
  const failCount = details.filter(d => d.result === 'X').length;
  const naCount = details.filter(d => d.result === '-').length;
  
  payload.overall_status = newStatus;
  payload.pass_count = passCount;
  payload.fail_count = failCount;
  payload.na_count = naCount;'''

new_code = re.sub(pattern, replacement, code, flags=re.MULTILINE)

if new_code != code:
    with open('public/js/app.js', 'w', encoding='utf-8') as f:
        f.write(new_code)
    print('Patched app.js')
else:
    print('Failed to patch app.js')
