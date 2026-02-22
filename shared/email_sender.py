"""Shared Gmail SMTP email utility."""
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

_MAX_RETRIES = 3
_RETRY_DELAY = 5  # seconds


def send_html_email(subject: str, html_body: str) -> None:
    """Send an HTML email via Gmail SMTP. Supports multiple recipients (comma-separated). Retries up to 3 times on failure."""
    sender     = os.environ["GMAIL_USER"]
    password   = os.environ["GMAIL_APP_PASSWORD"]
    recipients = [r.strip() for r in os.environ["RECIPIENT_EMAIL"].split(",")]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = sender
    msg["To"]      = ", ".join(recipients)
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    last_error = None
    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(sender, password)
                server.sendmail(sender, recipients, msg.as_string())
            print(f"[OK] Email sent to {', '.join(recipients)}")
            return
        except Exception as e:
            last_error = e
            print(f"[WARN] Email send error (attempt {attempt}/{_MAX_RETRIES}): {e}")
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY)

    raise RuntimeError(f"Email sending failed after {_MAX_RETRIES} attempts: {last_error}")
