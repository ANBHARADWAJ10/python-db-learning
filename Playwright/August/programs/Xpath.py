import time

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    # user = page.wait_for_selector("//input[@name='username']")
    # user.type("Admin")
    # user_pass = page.wait_for_selector("//input[@name='password']")
    # user_pass.type("admin123")
    #
    # login = page.wait_for_selector("//button[@type='submit']")
    # login.click()

    #forgot password
    forgot_pass = page.get_by_text("Forgot your password? ")
    forgot_pass.click()

    # //tagname[text()= "text"]
    # //label[contains(text(), "value")]
    # //tagname[starts-with(@id,'value')]
    # //tagname[ends-with(@id,'value')]

    # family
        # parent - //tagname[@id="xy']/parent::input[]
        # child - //tagname[@id='xy']/parent::input[]
        # ancestor

    # time.sleep(3)
    page.wait_for_load_state('networkidle')
    # page.wait_for_timeout(3000)


    browser.close()