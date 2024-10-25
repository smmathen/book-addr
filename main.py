from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import sys
import time
import configparser

goodreads_sign_in = f'https://www.goodreads.com/ap/signin?language=en_US&openid.assoc_handle=amzn_goodreads_web_na&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.goodreads.com%2Fap-handler%2Fsign-in&siteState=eyJyZXR1cm5fdXJsIjoiaHR0cHM6Ly93d3cuZ29vZHJlYWRzLmNvbS8ifQ%3D%3D'
config = configparser.ConfigParser()
config.read('config.ini')
goodreads_email = config['goodreads']['email']
goodreads_password = config['goodreads']['password']


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
    driver.get(f"https://www.goodreads.com/search?q={search}")
    time.sleep(5)
    book_title = search.replace("+", " ")
    # search_results = driver.find_elements(By.CLASS_NAME, 'book')
    first_book = driver.find_element(By.CLASS_NAME, "wtrButtonContainer")
    progress_trigger = first_book.find_element(
        By.CLASS_NAME, "progressTrigger")
    if progress_trigger.text == 'Want to Read':
        progress_trigger.click()
        time.sleep(2)
        return True

    return False


def generate_allen_url(search):
    return f"https://allen.na2.iiivega.com/search?query={search}&searchType=title&pageSize=10"


def main():

    allen_suffix = "%20".join(sys.argv[1:])
    goodreads_suffix = "+".join(sys.argv[1:])
    url = generate_allen_url(allen_suffix)

    driver = webdriver.Chrome()
    login_to_goodreads(driver)
    added = goodreads_search(driver, goodreads_suffix)
    if added:
        print("Book added to Goodreads")
    else:
        print("Book already in a shelf")

    driver.quit()


if __name__ == "__main__":
    main()
