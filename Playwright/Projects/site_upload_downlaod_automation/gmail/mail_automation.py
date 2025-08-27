from playwright.async_api import async_playwright
import asyncio
import os


async def automate_mail():
    # Check if auth state file exists
    if not os.path.exists("auth_state.json"):
        print("❌ No saved session found!")
        print("🔧 Run setup_session.py first to save authentication state")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)  # Run headless for automation

        try:
            # Load the saved authentication state
            context = await browser.new_context(storage_state="auth_state.json")
            page = await context.new_page()

            # Navigate to mailbox - should be already logged in
            await page.goto("https://outlook.office365.com/mail")

            # Check if we're actually logged in
            try:
                await page.wait_for_selector('[data-testid="app-header"]', timeout=10000)
                print("✅ Successfully accessed mailbox without login!")

                # Your email automation tasks here
                # Example: Check for new emails
                await page.wait_for_selector('[role="listbox"]')  # Email list
                emails = await page.locator('[role="option"]').count()
                print(f"📧 Found {emails} emails in inbox")

                # Add your specific automation logic here
                # e.g., read emails, send emails, filter, etc.

            except:
                print("❌ Session expired or login required")
                print("🔧 Re-run setup_session.py to refresh authentication")

        except Exception as e:
            print(f"❌ Error during automation: {e}")
        finally:
            await browser.close()


# Run the automation
if __name__ == "__main__":
    asyncio.run(automate_mail())
