from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup Chrome Options
chrome_options = Options()
#chrome_options.add_argument("--headless")  # You can remove this if you want browser to open

# Initialize Driver
service = Service()
driver = webdriver.Chrome(service=service, options=chrome_options)

try:
    # 1. Open URL
    url = "https://blockstream.info/block/000000000000000000076c036ff5119e5a5a74df77abf64203473364509f7732"
    driver.get(url)

    # 2. Wait for transaction list section
    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='txn font-p2']/a")))

    # 3. Get all 25 visible transactions
    transactions = driver.find_elements(By.XPATH, "//div[@class='txn font-p2']")

    print(f"Found {len(transactions)} transactions visible.")

    # 4. Loop through each transaction
    for idx, txn in enumerate(transactions, start=1):
        try:
            txn_hash = driver.find_element(By.XPATH, "//div[@class='txn font-p2']/a").text.strip()

            # Count number of input and output divs
            input_elements = driver.find_elements(By.XPATH, "//div[@class='txn font-p2']/a/ancestor::div[@class='header']//following-sibling::div[@class='ins-and-outs']//div[@class='vins']/div")
            output_elements = driver.find_elements(By.XPATH, "//div[@class='txn font-p2']/a/ancestor::div[@class='header']//following-sibling::div[@class='ins-and-outs']//div[@class='vout']/div")

            num_inputs = len(input_elements)
            num_outputs = len(output_elements)

            if num_inputs == 1 and num_outputs == 2:
                print(f"✅ Transaction Hash: {txn_hash} ➔ 1 input and 2 outputs")

        except Exception as e:
            print(f"⚠️ Error processing transaction {idx}: {e}")

finally:
    driver.quit()
