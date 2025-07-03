# test_smtp.py
import smtplib
import ssl
import os
from decouple import config

# Load environment variables (ensure .env file is in the same directory)
# You might need to adjust the path to .env if running this from outside project root
# For simplicity, assume .env is next to this script for testing.
# If not, comment out the config lines and hardcode for this test only.
EMAIL_HOST = config("EMAIL_HOST", "in-v3.mailjet.com")
EMAIL_PORT = config("EMAIL_PORT", default=587, cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
# EMAIL_USE_SSL = config('EMAIL_USE_SSL', default=False, cast=bool) # Use if needed instead of TLS
EMAIL_HOST_USER = config("EMAIL_HOST_USER", "bfdef101276ba71671b9b1bfdc5a8f04")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", "58591babf4845fa9fa0deb8bc4242ccb")

# Fallback to hardcoded values if config fails or for quick test
if "in-v3.mailjet.com" in EMAIL_HOST:
    print(
        "WARNING: Using hardcoded SMTP values. Make sure to replace them or set your .env correctly."
    )
    EMAIL_HOST = "in-v3.mailjet.com"  # REPLACE THIS
    EMAIL_PORT = 587  # REPLACE THIS
    EMAIL_USE_TLS = True  # REPLACE THIS (or False)
    EMAIL_HOST_USER = "bfdef101276ba71671b9b1bfdc5a8f04"  # REPLACE THIS
    EMAIL_HOST_PASSWORD = "58591babf4845fa9fa0deb8bc4242ccb"  # REPLACE THIS

SENDER_EMAIL = (
    "footroot@mytaller.info"  # Can be anything unless your provider enforces it
)
RECEIVER_EMAIL = "footroot.72@gmail.com"  # Send to an email you can check

print(f"Attempting to connect to SMTP server: {EMAIL_HOST}:{EMAIL_PORT}")
print(f"User: {EMAIL_HOST_USER}")
print(f"Use TLS: {EMAIL_USE_TLS}")

try:
    if EMAIL_USE_TLS:
        context = ssl.create_default_context()
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls(context=context)
    # elif EMAIL_USE_SSL:
    #     context = ssl.create_default_context()
    #     server = smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context)
    else:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)

    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    print("Authentication successful!")

    message = f"Subject: Test Email from Python\n\nHello from your SMTP test script!"
    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
    print(f"Test email sent from {SENDER_EMAIL} to {RECEIVER_EMAIL} successfully!")

except smtplib.SMTPAuthenticationError as e:
    print(f"SMTP Authentication Error: {e}")
    print(
        "Double-check your username, password, and app-specific passwords (for Gmail/Microsoft)."
    )
except smtplib.SMTPConnectError as e:
    print(f"SMTP Connection Error: {e}")
    print("Check EMAIL_HOST, EMAIL_PORT, and firewall settings.")
except smtplib.SMTPException as e:
    print(f"Other SMTP Error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
finally:
    if "server" in locals() and server:
        server.quit()
        print("SMTP server connection closed.")
