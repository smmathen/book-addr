from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from rich.console import Console
import configparser
import re
import sys
import time

goodreads_sign_in = f'https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads.com%2Fap-handler%2Fsign-in&siteState=eyJyZXR1cm5fdXJsIjoiaHR0cHM6Ly93d3cuZ29vZHJlYWRzLmNvbS8ifQ%3D%3D'
goodreads_search_prefix = "https://www.goodreads.com/search?q="
allen_url_start = "https://allen.na2.iiivega.com/search?query="
allen_url_paramters = "&searchType=title&pageSize=10&materialTypeIds=1"

config = configparser.ConfigParser()
config.read('config.ini')

goodreads_email = config['goodreads']['email']
goodreads_password = config['goodreads']['password']

console = Console()


def login_to_goodreads(driver):
    driver.get(goodreads_sign_in)
    time.sleep(2)

    email_input = driver.find_element(By.ID, 'ap_email')
    password_input = driver.find_element(By.ID, 'ap_password')

    email_input.send_keys(goodreads_email)
    password_input.send_keys(goodreads_password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(5)


def goodreads_search(driver, search):
    driver.get(f"{goodreads_search_prefix}{search}")
    time.sleep(3)
    first_book = driver.find_element(By.CLASS_NAME, "wtrButtonContainer")
    progress_trigger = first_book.find_element(
        By.CLASS_NAME, "progressTrigger")
    if progress_trigger.text == 'Want to Read':
        progress_trigger.click()
        time.sleep(2)
        return True

    return False


def generate_allen_url(search):
    return f"{allen_url_start}{search}{allen_url_paramters}"


def find_at_allen(driver, url):
    driver.get(url)
    time.sleep(3)
    second_h2 = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "(//h2)[2]"))
    )
    first_book_text = second_h2.text
    allen_book = re.sub(r'[^a-zA-Z0-9+]', '',
                        first_book_text.replace(" ", "+").lower())
    inputted_book = re.sub(r'[^a-zA-Z0-9+]', '',
                           "+".join(sys.argv[1:]).lower())

    return allen_book == inputted_book


def main():

    allen_suffix = "%20".join(sys.argv[1:])
    goodreads_suffix = "+".join(sys.argv[1:])
    allen_url = generate_allen_url(allen_suffix)

    driver = webdriver.Chrome()

    found_at_allen = find_at_allen(driver, allen_url)
    if not found_at_allen:
        console.print("[red]Book not found at Allen[/red]")
        driver.quit()
        return

    login_to_goodreads(driver)

    added = goodreads_search(driver, goodreads_suffix)
    if added:
        console.print("[green]Book added to Goodreads[/green]")
    else:
        console.print("[blue]Book already in a shelf[/blue]")

    driver.quit()


if __name__ == "__main__":
    main()
