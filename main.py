import data
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

warnings = []

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

	# wait for contact to be saved
	time.sleep(5)

	# verify saved contact name
	try:
		assert(driver.find_element(By.ID,"contactName").get_attribute('innerHTML') == contact["name"])
	except Exception as e:
		print(">>> WARNING :::: By Name ::::", driver.find_element(By.ID,"contactName").get_attribute('innerHTML'))

	# verify saved contact number
	try:
		assert(len(driver.find_elements(By.XPATH, "//a[@href='tel:" + contact["code"] + contact["phone"] + "']")) > 0)
	except Exception as e:
		print(">>> WARNING :::: By Phone ::::", len(driver.find_elements(By.XPATH, "//a[@href='tel:" + contact["code"] + contact["phone"] + "']")))

	# confirmation of successful loop
	print(">>> ADDED ::::", contact["name"], "-", contact["code"], contact["phone"])

	# page refresh for selenium data reset
	driver.find_element(By.XPATH, "//a[@href='./']").click()
	driver.refresh()

	time.sleep(2)

print("Contacts have been updated to Google account")

if len(warnings) > 0:
	print("---- Manual Verfication Required ----")
	for i in len(warnings):
		print(i, "-", data.contacts[warnings[i]]["name"], "-", data.contacts[warnings[i]]["phone"])