from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

path = "C:/driver/chromedriver-win64/chromedriver/chromedriver.exe"
service = Service(executable_path=path)
driver = webdriver.Chrome(service=service)

driver.maximize_window()
driver.get('https://google.com')

search = driver.find_element(By.ID,"APjFqb").send_keys('Github.com')
search_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, 'btnK'))).click()
git_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'github'))).click()