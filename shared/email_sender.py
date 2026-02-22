"""공통 Gmail SMTP 이메일 발송 유틸리티."""
import os
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

_MAX_RETRIES = 3
_RETRY_DELAY = 5  # seconds


def send_html_email(subject: str, html_body: str) -> None:
    """Gmail SMTP로 HTML 이메일을 발송합니다. 쉼표로 구분된 여러 수신자 지원. 실패 시 최대 3회 재시도합니다."""
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
            print(f"✅ 이메일 발송 완료 → {', '.join(recipients)}")
            return
        except Exception as e:
            last_error = e
            print(f"⚠️  이메일 발송 오류 (시도 {attempt}/{_MAX_RETRIES}): {e}")
            if attempt < _MAX_RETRIES:
                time.sleep(_RETRY_DELAY)

    raise RuntimeError(f"이메일 발송 {_MAX_RETRIES}회 모두 실패: {last_error}")
