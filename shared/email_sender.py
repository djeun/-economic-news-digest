"""공통 Gmail SMTP 이메일 발송 유틸리티."""
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_html_email(subject: str, html_body: str) -> None:
    """Gmail SMTP로 HTML 이메일을 발송합니다."""
    sender    = os.environ["GMAIL_USER"]
    recipient = os.environ["RECIPIENT_EMAIL"]
    password  = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = sender
    msg["To"]      = recipient
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"✅ 이메일 발송 완료 → {recipient}")
