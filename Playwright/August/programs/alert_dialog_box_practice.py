from playwright.sync_api import sync_playwright

import time

alert_text = []

def dialog_box(dialog):
    dialog.type('Nikhil')
    dialog.accept()
    # alert_text.append(msg)
    msg = page.wait_for_selector("//p[@id=demo1]")
    print(msg)
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demo.automationtesting.in/Alerts.html")

    # step 1
    page.locator("//a[@href='#Textbox']").click()

    # step 2
    page.wait_for_selector("//div[@id='Textbox']/button").click()
    page.wait_for_timeout(5000)
    # step 3
    # first create a function handler for dialog box
    page.on("dialog", dialog_box)
    page.wait_for_timeout(3000)

    browser.close()

# still pending i will look into later.
