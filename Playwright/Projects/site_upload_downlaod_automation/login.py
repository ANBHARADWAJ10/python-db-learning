from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.site24x7.com/app/client?a=f#/home/monitors")
    page.wait_for_timeout(3000)
    user_name = page.locator("//input[@id='login_id']")
    user_name.type('nanantharaju@crunchtime.com')
    page.wait_for_timeout(3000)
    next_button = page.locator("//button[@id='nextbtn']")
    next_button.click()
    page.wait_for_timeout(3000)
    enter_otp = page.locator('//div[@id="otp"]')
    enter_otp.type('')