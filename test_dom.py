import time
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By

options = Options()
options.add_argument('--headless')
driver = webdriver.Edge(options=options)

driver.get('http://localhost:8000')
time.sleep(2)

login_btn = driver.find_elements(By.XPATH, "//button[contains(text(), 'System Login')]")
if login_btn:
    driver.execute_script("document.getElementById('login-username').value='admin'; document.getElementById('login-password').value='password'; handleLoginSubmit();")
    time.sleep(2)

driver.execute_script("console.log('CLICKING NOW'); document.querySelector(\".b-nav-tab[data-tab='qrgen']\").click();")
time.sleep(1)

logs = driver.get_log('browser')
for entry in logs:
    print('LOG:', entry)

driver.quit()
