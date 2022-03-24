import data
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(executable_path="chromedriver.exe")

driver.get("https://accounts.google.com/signin/v2/identifier?passive=1209600&continue=https%3A%2F%2Fcontacts.google.com%2F&followup=https%3A%2F%2Fcontacts.google.com%2F&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
driver.maximize_window()

# set wait time
driver.implicitly_wait(10)

# provided Google account username and hit next
driver.find_element(By.ID,"identifierId").send_keys(data.google_account_username)
driver.find_element(By.ID,"identifierNext").click()

# provided Google account password and hit next
driver.find_element(By.CSS_SELECTOR, "#password > div > div > div > input").send_keys(data.google_account_password)
driver.find_element(By.ID,"passwordNext").click()

for contact in data.contacts:
	# go to create new contact page
	driver.find_element(By.XPATH,"//button[@title='Add new contact']").click()
	time.sleep(2)
	driver.find_element(By.XPATH,"//span[@aria-label='Create a contact']").click()

	# enter new contact details
	driver.find_element(By.XPATH, "(//input[@type='text'])[3]").send_keys(contact["name"])
	driver.find_element(By.XPATH, "//input[@type='tel']").send_keys(contact["phone"])

	# click save button
	driver.find_element(By.XPATH, "//button[@aria-label='Save']").click()

	# wait for contact to be saved and check details
	time.sleep(5)
	print(">>> VERIFY ::::", driver.find_element(By.ID,"contactName").get_attribute('innerHTML'), "-", len(driver.find_elements(By.XPATH, "//a[@href='tel:" + contact["code"] + contact["phone"] + "']")))
	assert(driver.find_element(By.ID,"contactName").get_attribute('innerHTML') == contact["name"])
	assert(len(driver.find_elements(By.XPATH, "//a[@href='tel:" + contact["code"] + contact["phone"] + "']")) > 0)

	print(">>> ADDED ::::", contact["name"], "-", contact["code"], contact["phone"])

	time.sleep(2)

print("All contacts have been updated to your Google account")