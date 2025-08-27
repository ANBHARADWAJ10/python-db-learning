# Present Version of Playwright
    playwright==1.47.0

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium

# First time login (With OTP)
python login_with_otp.py

# What happens:
    Browser opens showing Site24x7 login
    Your credentials are filled automatically
    After OTP page appears, you manually enter the code
    Press Enter in terminal after submitting OTP
    Session gets saved to site24x7_session.json

# Subsequent Runs
python use_session.py

# What happens:
    Browser opens and automatically logs you in
    No OTP required - goes straight to dashboard
    Ready for your automation tasks
    
    
# Important Notes
    Update Credentials: Replace 'your_email@domain.com' and 'your_password' in login_with_otp.py
    Session Validity: The saved session typically lasts weeks/months. When it expires, just run login_with_otp.py again
    Browser Visibility: Both scripts run with headless=False so you can see what's happening. Change to headless=True for background execution later
    Error Handling: If session fails, the script will tell you to re-run the login script
    This setup gives you a reusable system where you only need to manually enter OTP occasionally, while most of your automation runs seamlessly with the saved session!