import re

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://demo.automationtesting.in/Windows.html")

    page.wait_for_selector("//button[contains(text(), 'cli')]").click()
    page.wait_for_timeout(5000)

    # Total pages that have been opened.

    total_pages = context.pages
    print(len(total_pages))

    for i in total_pages:
        print(f'{i.title()} -> URL: {re.sub('<[^<]+?>', ' ', i.url)}')

    # parent title()
    print(page.title())
    # How to switch to new page
    new_page = total_pages[1]
    new_page.bring_to_front()
    new_page.wait_for_timeout(5000)
    clickable = new_page.locator('//a[text()="Submit your talk."]')
    new_page.wait_for_timeout(5000)
    print(new_page.title())
    new_page.close()
    # browser.close()