# Main login script

import asyncio
from playwright.async_api import async_playwright
import os


async def login_with_manual_otp():
    async with async_playwright() as p:
        # Launch browser in non-headless mode so you can see it
        browser = await p.chromium.launch(headless=False, slow_mo=1000)
        page = await browser.new_page()

        try:
            # Navigate to Site24x7 login
            await page.goto('https://www.site24x7.com/app/client?a=f#/home/monitors')

            # Fill login credentials - REPLACE WITH YOUR DETAILS
            user_name = page.locator("//input[@id='login_id']")
            await user_name.type('nanantharaju@crunchtime.com')

            next_button = page.locator("//button[@id='nextbtn']")
            await next_button.click()

            # Wait for OTP page to appear
            print("Waiting for OTP page...")
            await page.wait_for_selector('//div[@id="otp"]',timeout=10000)

            # Pause for manual OTP entry
            print("\n" + "=" * 50)
            print("🔐 MANUAL OTP ENTRY REQUIRED")
            print("=" * 50)
            print("1. Check your phone/email for the OTP code")
            print("2. Enter it in the browser window")
            print("3. Click submit or press Enter in the browser")
            print("4. Then press Enter here in the terminal...")
            print("=" * 50)

            input("Press Enter after you've entered OTP and submitted it...")

            # Wait for successful login (adjust URL pattern as needed)
            print("Waiting for successful login...")
            await page.wait_for_load_state('networkidle')
            await asyncio.sleep(2)  # Extra wait for complete load

            # Save session state
            session_file = "site24x7_session.json"
            await page.context.storage_state(path=session_file)
            print(f"✅ Session saved successfully to {session_file}")
            print("You can now use this session for future logins!")

        except Exception as e:
            print(f"❌ Error during login: {e}")
        finally:
            await browser.close()


if __name__ == "__main__":
    print("🚀 Starting Site24x7 login with manual OTP...")
    asyncio.run(login_with_manual_otp())
