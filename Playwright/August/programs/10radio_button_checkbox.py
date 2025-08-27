from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demo.automationtesting.in/Register.html")

    # radio button
    radio_button = page.query_selector("//input[@type='radio']")
    radio_button.check()
    if radio_button.is_checked():
        print("yes")



    # checkbox
    # check_box = page.query_selector("//input[@type='checkbox']")
    check_box = page.query_selector("//input[@type='checkbox' and @value='Cricket']")
    check_box.check()
    check_box_cric = page.query_selector("//input[@value='Movies']")
    check_box_cric.click()

    page.wait_for_timeout(3000)
    browser.close()