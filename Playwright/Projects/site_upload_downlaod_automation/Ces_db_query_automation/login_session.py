# Main code

import asyncio
from playwright.async_api import async_playwright

async def login():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto("http://proem001.prod.crunchtime.it:8080/ords/f?p=107:LOGIN_DESKTOP:16389919548826:::::")

        user_name = page.locator("//input[@id = 'P9999_USERNAME']")
        # Enter your username here
        await user_name.type('nanantharaju')

        user_pass = page.locator("//input[@id = 'P9999_PASSWORD']")
        # Enter your okta password here
        await user_pass.type('Nikhil#1911')

        await page.wait_for_timeout(3000)
        # Click the SignIn button
        signin_btn = page.locator("//span[text()='Sign In']")
        await signin_btn.click()

        # Click on the OUTAGES REPORT
        report_btn = page.locator("//span[text()='OUTAGE REPORT']")
        await report_btn.click()

        # Click on Upload button
        upload_btn = page.locator("//span[text()='Upload Site 24x7 Outages']")
        await upload_btn.click()

        # Keep browser open for manual inspection
        input("Press Enter to close browser...")

if __name__ == "__main__":
    asyncio.run(login())