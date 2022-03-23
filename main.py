from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path="chromedriver.exe")

driver.get("https://contacts.google.com/")
driver.maximize_window()