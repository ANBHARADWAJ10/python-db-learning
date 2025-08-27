from playwright.sync_api import sync_playwright

alert_text = []

def handle_dialog_box(dialog):
    message = dialog.message
    alert_text.append(message)
    dialog.accept()
    print(alert_text[0])


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demo.automationtesting.in/Alerts.html")

    # alert box
    # One slash = direct child of the parent
    # Two slash = second child of the parent
    # alert_button = page.query_selector("//div[@id='OKTab']/button")
    # page.locator('//div[@id="OKTab"]/button').click
    # page.wait_for_timeout(3000)

    page.locator('//a[@href="#CancelTab"]').click()
    page.wait_for_timeout(3000)

    # click cancel
    # page.on("dialog", lambda dialog: dialog.dismiss())

## Inorder to make code readable we can combine the both in a single function
    # click ok
    # page.on("dialog", lambda dialog: dialog.accept())
    #
    # # print the message
    # page.on("dialog", lambda dialog: print(dialog.message))

## dialog box using handler

    page.on("dialog", handle_dialog_box)


    page.wait_for_selector('//div[@id="CancelTab"]/button').click()
    page.wait_for_timeout(3000)

    # control alert

    browser.close()

