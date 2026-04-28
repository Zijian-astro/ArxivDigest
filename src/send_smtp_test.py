from datetime import datetime

from dotenv import load_dotenv

from smtp_mailer import load_smtp_settings, send_email


if __name__ == "__main__":
    load_dotenv()
    settings = load_smtp_settings()
    if not settings:
        raise RuntimeError(
            "SMTP settings incomplete. Set TO_EMAIL plus MAIL_USERNAME and MAIL_PASSWORD "
            "in .env, or set MAIL_CONNECTION."
        )

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_email(
        subject="ArxivDigest SMTP test",
        html_body=f"<p>SMTP is configured correctly.</p><p>Sent at {now}</p>",
        text_body=f"SMTP is configured correctly. Sent at {now}",
        settings=settings,
    )
    print(f"SMTP test email sent to {settings.to_email}")
