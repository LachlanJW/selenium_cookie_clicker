from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time

# Keep chrome browser open
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")


# Click rapidly for 5 seconds
def click_five_seconds():
    cookie = driver.find_element(By.ID, value="cookie")
    begin = time.time()
    while time.time() - begin < 5:
        cookie.click()


# Choose purchases for cookies
def choose_upgrade():
    # Find out how many cookies in the budget
    money = driver.find_element(By.ID, value="money").text
    money = int(money.replace(',', ''))

    # Find out the available upgrades, buy the most expensive first
    store = driver.find_elements(By.CSS_SELECTOR, value="#store div b")
    store.pop()
    store.reverse()

    for choice in store:
        try:
            # Extract the number part
            price_str = choice.text.split(' - ')[-1].strip()
            # Remove commas and convert to integer
            price = int(price_str.replace(',', ''))

            # Click on item if we can afford it
            if money >= price:
                choice.click()
                return

        except StaleElementReferenceException:
            choose_upgrade()


def run_game():
    # Execute the code for 5 mins total
    start_time = time.time()
    while time.time() - start_time < 300:  # 5 minutes in seconds
        click_five_seconds()
        choose_upgrade()

    # Assess result by clicks per second (cps)
    result = driver.find_element(By.CSS_SELECTOR, value="#saveMenu #cps")
    print(result.text)
    driver.quit


run_game()
