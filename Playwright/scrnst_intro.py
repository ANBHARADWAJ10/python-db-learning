from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()
#     page.goto("https://playwright.dev/")
#     page.screenshot(path="example01.png")
#     browser.close()
#
# interactive mode
#
# playwright = sync_playwright().start()
# browser = playwright.chromium.launch(headless=False)
# page = browser.new_page()
# page.goto("https://playwright.dev/")
# page.screenshot(path="example01.png")
# browser.close()
# playwright.stop()

# with sync_playwright() as p:
#     browser = p.chromium.launch()
#     page = browser.new_page()
#     page.goto("https://bing.com/")
#     page.get_by_role("textbox").fill("Peter")
#     page.screenshot(path="peter.png")
#     browser.close()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://demoqa.com/automation-practice-form")
    page.get_by_role("input['textarea']").fill("Nikhil Bharadwaj")
    page.get_by_role("Birth date").fill(10-1-2002)
    page.screenshot(path="birthdate.png")
    browser.close()