from email.message import EmailMessage
from smtplib import SMTP

from app.config import settings


def send_password_reset_email(to_email: str, reset_link: str) -> None:
    # Keep email sending optional in development if SMTP is not configured.
    if not settings.SMTP_HOST or not settings.SMTP_FROM_EMAIL:
        print(f"[password-reset] {to_email} -> {reset_link}")
        return

    message = EmailMessage()
    message["Subject"] = "Password reset request"
    message["From"] = settings.SMTP_FROM_EMAIL
    message["To"] = to_email
    message.set_content(
        "Use this link to reset your password:\n"
        f"{reset_link}\n\n"
        "If you did not request this, you can ignore this email."
    )

    with SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as smtp:
        if settings.SMTP_USE_TLS:
            smtp.starttls()
        if settings.SMTP_USERNAME and settings.SMTP_PASSWORD:
            smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        smtp.send_message(message)
