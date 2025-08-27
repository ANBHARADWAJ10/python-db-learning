from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto('http://demo.automationtesting.in/Selectable.html')

## Hover over a dropdown or anything
    page.locator('//a[text() = "SwitchTo"]').hover()

## click on the element
    page.locator('//a[text() = "SwitchTo"]').click()
## inner click after the clicking on the dropdown
    page.locator('//a[text() = "Alerts"]').click()

## Double click
    page.locator('//a[text() = "SwitchTo"]').dbclick()

## Right click
    page.locator('//a[text() = "SwitchTo"]').click(button='right')

## shift click
    page.locator('//a[text() = "Alerts"]').click(modifiers=["Shift"])

## Keyboard
    page.locator('//a[text() = "Alerts"]').click().press('A')

    page.wait_for_timeout(5000)
    browser.close()