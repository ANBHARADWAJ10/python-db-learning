from pydoc import visiblename

from playwright.sync_api import sync_playwright
import time
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")

    # Xpath - Relative Xpath
    # Using Attribute - //'tagname[@attribute = "value"]'
    user = page.wait_for_selector('//input[@name="username"]')
    user.type("Admin")
    password = page.wait_for_selector('//input[@placeholder="Password"]')
    password.type("admin123")
    login = page.wait_for_selector('//button[@type="submit"]', state="visible", timeout=5000)
    login.click()
    time.sleep(10)
    print("You are logged in")

    # browser.close()


    # enter = page.wait_for_selector('//button[@type="submit"]', state="visible", timeout=5000)


















    enter = page.wait_for_selector('//button[@type="submit"]', state="visible", timeout=5000)
    enter.click()

    # text - //tagname[text()='text']
    # attributes - //tagname[contains(@attribute, "value")]
    # text - //tagname[contains(text(), 'text')]