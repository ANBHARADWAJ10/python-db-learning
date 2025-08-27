from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demo.automationtesting.in/Register.html")
    # page.wait_for_timeout(3000)
    # page.wait_for_load_state('networkidle')

    ## Select DropDown
    # 1. Find the location
    ## select_dropdown = page.query_selector("//select[@id='Skills']")
    # 2. Select the Option
    ## select_dropdown.select_option(label='Art Design')

    ## we can do all the in single line
    page.select_option("//select[@id='Skills']", label="AutoCAD")

    page.wait_for_timeout(3000)
    browser.close()