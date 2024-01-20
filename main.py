import time
from datetime import datetime

import requests
import undetected_chromedriver as uc
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

options = uc.ChromeOptions()
options.add_argument("--auto-open-devtools-for-tabs")

driver = uc.Chrome(options=options)


# Function to extract token address from URL
def extract_token_address(url):
    return url.split('/')[-1]


# Function to send a Telegram message (you need to implement this function)
def send_telegram_message(token_address):
    # Implement your code to send a Telegram message here
    pass


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


def clear_search_bar():
    search_bar = driver.find_element(By.XPATH, '//input[contains(@placeholder, "Search token for analysis")]')

    search_bar.send_keys(Keys.ENTER)

    search_bar.send_keys(Keys.CONTROL + "a")
    search_bar.send_keys(Keys.DELETE)


# Initialize variables
processed_tokens = []
potential_gems = []
temp_processed = []

while True:  # Infinite loop for continuous scraping
    url = 'https://moonarch.app/top-gainers'
    # Step 1: Go to the top gainer section
    driver.get(url)
    response = requests.get(url)

    if response.status_code == 200:

        # Wait max for 600secs till the 'tokenName' element is found on the page before continuing
        WebDriverWait(driver, 600).until(EC.presence_of_element_located((By.CLASS_NAME, 'tokenName')))

        soup = BeautifulSoup(driver.page_source, 'lxml')
        all_rows = soup.find_all('tr')

        # Step 2: Extract all 30 list of tokens URL
        for rows in all_rows:
            token_url = rows.get('data-pk')
            if token_url:
                temp_processed.append(token_url)

        # Step 3
        for token_address in temp_processed:

            if token_address not in processed_tokens:
                processed_tokens.append(token_address)

                # Step 4: Locate the search element

                clear_search_bar()

                search_bar = driver.find_element(By.XPATH,
                                                 '//input[contains(@placeholder, "Search token for analysis")]')

                search_bar.send_keys(token_address)

                # Wait for max 600secs till we find the price tag on the page
                WebDriverWait(driver, 600).until(EC.presence_of_element_located(
                    (By.XPATH, '//*[@id="app"]/div[3]/div[2]/div/div/div[2]/div[1]/ul/li[1]')))

                # Locate the token's age element
                token_age_element = driver.find_element(By.XPATH,
                                                        '//li[label[text()="Token age"]]/span[@class="value align-right"]')
                date_title = token_age_element.get_attribute("title")

                # Locate the message text element
                message_element = driver.find_element(By.CLASS_NAME, 'token-check-message')
                message_text = message_element.text

                if is_token_age_less_than_24hrs(date_title) and "Moonarch rugcheck has not found" in message_text:
                    print(
                        f"Token age is less than 24hrs and Moonarch rugcheck hasn't found anything suspecious. {token_address}")

                    # Step 5: Send Telegram message and store in potential_gems
                    send_telegram_message(token_address)
                    potential_gems.append(token_address)

                else:
                    print(f"Token age is more than 24hrs {get_token_age_text(date_title)}  *  {token_address}")

        # Step 6: Clear lists
        temp_processed.clear()
        print(f"Processed {len(processed_tokens)} tokens so far")

        # toggle_button = driver.find_element(By.XPATH, '//*[@id="app"]/div[2]/nav/div[3]/button')
        # toggle_button.click()

        # nav_item_top_gainers = driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div[1]/div/ul/li[2]')

        # nav_item_top_gainers = driver.find_element(By.XPATH, '//*[@id="app"]/div[3]/div[1]/div/ul/li[2]')
        # nav_item_top_gainers.click()
        # Step 7: Wait for 15 seconds
        time.sleep(10)

    else:
        print('Failed to fetch data. Status code:', response.status_code)
        break  # Break the loop if failed to fetch data
