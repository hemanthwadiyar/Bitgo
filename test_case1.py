from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    url = "https://blockstream.info/block/000000000000000000076c036ff5119e5a5a74df77abf64203473364509f7732"
    driver.get(url)

    wait = WebDriverWait(driver, 15)
    heading_element = wait.until(
        EC.visibility_of_element_located((By.XPATH, "//h3[contains(text(), '25 of 2875 Transactions')]")))

    heading_xpath = "//h3[contains(text(), '25 of 2875 Transactions')]"
    try:
        heading_element = driver.find_element(By.XPATH, heading_xpath)
        heading_text = heading_element.text.strip()
        expected_text = "25 of 2875 Transactions"

        if heading_text == expected_text:
            print("✅ Heading validation passed!")
    except:
        print("Validation Failed: Heading not found.")

finally:
    driver.quit()
