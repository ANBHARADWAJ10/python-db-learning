# cache -  stores the data in the browser
# cookies  - stores the data in browser as well as server (DataBase)
import csv
from os import write
from venv import create

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    # url
    page.goto("https://www.redbus.in/")
    my_cookies = page.context.cookies()

## saving all the cookies that are available in a csv format.
    filename = "cookies.csv"
    with open(filename, 'w', newline='') as csvfile:
        if my_cookies:
            writer = csv.DictWriter(csvfile, fieldnames=my_cookies[0].keys())
            writer.writeheader()
            writer.writerows(my_cookies)

        # print cookies to terminal
        for cookie in my_cookies:
            print(cookie)


## clearing all the cookies
    page.context.clear_cookies()

## insert personal cookies
    new_cookies = {
        'name' : 'ravi',
        'udid' : '6546548464'
    }
## The below command to pass the cookies.
    # page.context.add_cookies(new_cookies)

## take a screenshot
    # page.wait_for_load_state('networkidle')
    page.wait_for_timeout(5000)
    page.screenshot(path='tmp/redbus.png', full_page=True)
    browser.close()


