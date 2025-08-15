# Master element selection, perform user like actions, and handle dynamic content loading

# CSS Selectors

# page.click("button#submit") ## By ID

# page.click('.btn-primary) ## by class

# page.click("input[name='email']") ## by attribute

## Text Selectors

# page.click("text=Sign In")

## Xpath Sequence

# page.click("//button[@id='submit']")

## Role Selector

# page.get_by_role("button", name="Submit").click()

####
    # The below code opens a new page and then clicks a screenshot of it.

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://bing.com/")
    # page.click("text=Images")
    with context.expect_page() as new_page_info:
        page.click("text=Images")
    new_page = new_page_info.value

    new_page.wait_for_load_state("networkidle")
    new_page.screenshot(path="tmp/screenshot.png")
    browser.close()

    # # Click something that opens a new page (popup/new tab)
    # with context.expect_page() as new_page_info:
    #     page.click("a[target='_blank']")  # Example: link opens in new tab
    # new_page = new_page_info.value  # Get the newly opened page
    #
    # # Wait for the new page to load completely
    # new_page.wait_for_load_state("networkidle")
    #
    # # Take screenshot of the new page
    # new_page.screenshot(path="second_page.png", full_page=True)