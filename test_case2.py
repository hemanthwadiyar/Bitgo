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
count = 0
try:

    url = "https://blockstream.info/block/000000000000000000076c036ff5119e5a5a74df77abf64203473364509f7732"
    driver.get(url)

    wait = WebDriverWait(driver, 15)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='txn font-p2']/a")))

    transactions = driver.find_elements(By.XPATH, "//div[@class='txn font-p2']")

    print(f"Found {len(transactions)} transactions visible.")

    for idx, txn in enumerate(transactions, start=1):
        try:
            txn_hash = txn.find_element(By.XPATH, ".//a").text.strip()
            #print(txn_hash)

            # Count number of input and output divs
            input_elements = txn.find_elements(By.XPATH,
                                               ".//ancestor::div[@class='header']//following-sibling::div[@class='ins-and-outs']//div[@class='vins']/div//a")
            #print([inp.text for inp in input_elements])

            output_elements = txn.find_elements(By.XPATH,
                                                ".//ancestor::div[@class='header']//following-sibling::div[@class='ins-and-outs']//div[@class='vout']/div")
            #print([op.text for op in output_elements])

            num_inputs = len(input_elements)
            #print(num_inputs)
            num_outputs = len(output_elements)
            #print(num_outputs)

            if num_inputs == 1 and num_outputs == 2:
                print(f" Transaction Hash: {txn_hash} ➔ 1 input and 2 outputs")
                count += 1

        except Exception as e:
            print(f"Error processing transaction {idx}: {e}")
    print(f"\nTotal transactions with exactly 1 input and 2 outputs: {count}")
finally:
    driver.quit()
