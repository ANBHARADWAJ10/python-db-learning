import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto('https://demo.automationtesting.in/Selectable.html')
        await page.wait_for_timeout(3000)

        # Using all() method
        b_locator = page.locator('b')
        all_elements = await b_locator.all()

        for element in all_elements:
            text = await element.text_content()
            print(text)

        await browser.close()


asyncio.run(main())
