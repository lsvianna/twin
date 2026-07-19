from dotenv import load_dotenv
from email.message import EmailMessage
import os
import smtplib
load_dotenv(override=True)

EMAIL_ADDRESS = os.getenv("GMAIL_EMAIL")
EMAIL_APP_PASSWORD = os.getenv("GMAIL_SENHA")


def send_email(subject, text_body):
    msg = EmailMessage()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = subject
    msg.set_content(text_body)

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_APP_PASSWORD)
        server.send_message(msg)
