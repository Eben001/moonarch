import time
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime
from selenium.webdriver.common.keys import Keys


def get_token_age_text(token_age):
    try:
        # Convert the token_age string to a datetime object
        token_date = datetime.strptime(token_age, '%Y-%m-%d %H:%M')

        # Calculate token age
        current_date = datetime.now()
        age_difference = current_date - token_date

        # Calculate days, hours, and minutes from the difference
        days = age_difference.days
      
        age_text = f"{days} days"
        return age_text

    except Exception as e:
        print("Error occurred:", e)
        return "Unable to determine age"


def is_token_age_less_than_24hrs(token_age):
    try:
        # Convert the token_age string to a datetime object
        token_date = datetime.strptime(token_age, '%Y-%m-%d %H:%M')

        # Calculate token age
        current_date = datetime.now()
        age_difference = current_date - token_date

        # Check if token age is less than 24 hours
        if age_difference.total_seconds() / 3600 < 25:
            return True
        else:
            return False

    except Exception as e:
        print("Error occurred:", e)
        return False


driver = uc.Chrome()

temp_processed = []
processed_tokens = []

url = 'https://moonarch.app/top-gainers'
driver.get(url)

#time.sleep(35)

# Wait max for 600sec till you find this element
WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.CLASS_NAME, 'tokenName')))

soup = BeautifulSoup(driver.page_source, 'lxml')
all_rows = soup.find_all('tr')


for rows in all_rows: 
    token_url = rows.get('data-pk')
    temp_processed.append(token_url)

processed_tokens.extend(temp_processed)

temp_processed
search_bar = driver.find_element(By.XPATH, '//input[@placeholder="Search token for analysis"]')
search_bar.send_keys(Keys.CONTROL + "a")
search_bar.send_keys(Keys.DELETE)
search_bar.send_keys("0xc8f8ae2650bde9e795f3ea81afcf246ca4d1c4b5")




search_bar.send_keys("0xc8f8ae2650bde9e795f3ea81afcf246ca4d1c4b5")


WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[3]/div[2]/div/div/div[2]/div[1]/ul/li[1]')))


for token_address in temp_processed: 
    # Step 7: Visit token info
    search_bar = driver.find_element(By.XPATH, '//*[@id="typeahead-input-40458"]')
    search_bar.send_keys(Keys.CONTROL + "a")
    search_bar.send_keys(Keys.DELETE)

    search_bar.send_keys('0x9b8d6d08803cb4fd3b3b345819dbfe45e51686c2')

    # Wait till we find the price tag on the page
    WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[3]/div[2]/div/div/div[2]/div[1]/ul/li[1]')))


    #Locate the token's age element
    token_age_element = driver.find_element(By.XPATH, '//li[label[text()="Token age"]]/span[@class="value align-right"]')
    date_title = token_age_element.get_attribute("title")

    message_element = driver.find_element(By.CLASS_NAME, 'token-check-message')
    message_text = message_element.text
    message_text

    # Check if the specified message exists in the text content
    if "Moonarch rugcheck has not found" in message_text:
        print("The message exists.")
    else:
        print("The message does not exist.")


    if is_token_age_less_than_24hrs(date_title) and "Moonarch rugcheck has not found" in message_text: 
        print(f"Token age is less than 24hrs")
        print("The message exists.")
        
    else: 
        print(f"Token age is more than 24hrs")

        print(get_token_age_text(date_title))

    




 