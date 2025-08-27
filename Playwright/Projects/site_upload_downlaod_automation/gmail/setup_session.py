from playwright.async_api import async_playwright
import asyncio


async def setup_initial_session():
    async with async_playwright() as p:
        # Launch browser in visible mode for manual 2FA
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            # Navigate to your office mail login
            await page.goto("https://outlook.office365.com")

            # Enter your email
            await page.fill('//input[@id="input28"]', 'nanantharaju@crunchtime.com')
            await page.click('//input[@type="submit"]')

            # Wait for password field and enter password
            # await page.wait_for_selector('input[name="passwd"]')
            # await page.fill('input[name="passwd"]', 'your-password')
            # await page.click('input[type="submit"]')

            # Manual step: Approve push notification on your phone
            print("🔔 Push notification sent to your phone!")
            print("👆 Please approve it using Face ID/Fingerprint...")
            print("⏳ Waiting for login to complete...")

            # Wait for successful login (adjust selector based on your mail interface)
            await page.wait_for_url("**/mail/**", timeout=120000)  # 2 minutes timeout
            print("✅ Login successful!")

            # Save the authenticated state
            await context.storage_state(path="auth_state.json")
            print("💾 Session state saved to auth_state.json")

        except Exception as e:
            print(f"❌ Error during setup: {e}")
        finally:
            await browser.close()


# Run the setup
if __name__ == "__main__":
    asyncio.run(setup_initial_session())
