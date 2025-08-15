import asyncio
from playwright.async_api import Playwright, async_playwright

async def run(playwright: Playwright, *, url) -> dict:
    browser = await playwright.chromium.launch(headless=False)
    page = await browser.new_page()

    await asyncio.sleep(1)

    await page.goto(url)

    await asyncio.sleep(1)

    title = await page.title()

    await browser.close()

    return {'title': title, 'url': url}

async def main() -> None:
    async with async_playwright() as playwright:
        result = await run(playwright, url='https://crawlee.dev')
        print(result)

if __name__ == '__main__':
    asyncio.run(main())