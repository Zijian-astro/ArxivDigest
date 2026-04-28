import os
import smtplib
import ssl
from dataclasses import dataclass
from email.message import EmailMessage
from urllib.parse import unquote, urlparse


PLACEHOLDER_ENV_VALUES = {
    "",
    "your_api_key",
    "your_deepseek_api_key",
    "your_openai_api_key",
    "your_email",
    "your_gmail_app_password",
}


def get_configured_env(name):
    value = os.environ.get(name, "").strip()
    if value in PLACEHOLDER_ENV_VALUES or value.startswith("your_"):
        return None
    return value


@dataclass
class SmtpSettings:
    host: str
    port: int
    username: str
    password: str
    from_email: str
    to_email: str
    starttls: bool = True
    ssl: bool = False


def _settings_from_connection_url(connection_url, to_email):
    parsed = urlparse(connection_url)
    if parsed.scheme not in {"smtp", "smtp+starttls", "smtps"}:
        raise RuntimeError(
            "MAIL_CONNECTION must start with smtp://, smtp+starttls://, or smtps://"
        )
    if not parsed.hostname:
        raise RuntimeError("MAIL_CONNECTION is missing the SMTP host")
    if not parsed.username or not parsed.password:
        raise RuntimeError("MAIL_CONNECTION must include username and password")

    username = unquote(parsed.username)
    password = unquote(parsed.password)
    port = parsed.port or (465 if parsed.scheme == "smtps" else 587)
    return SmtpSettings(
        host=parsed.hostname,
        port=port,
        username=username,
        password=password,
        from_email=get_configured_env("FROM_EMAIL") or username,
        to_email=to_email,
        starttls=parsed.scheme == "smtp+starttls",
        ssl=parsed.scheme == "smtps",
    )


def load_smtp_settings():
    to_email = get_configured_env("TO_EMAIL")
    if not to_email:
        return None

    connection_url = get_configured_env("MAIL_CONNECTION")
    if connection_url:
        return _settings_from_connection_url(connection_url, to_email)

    username = get_configured_env("MAIL_USERNAME")
    password = get_configured_env("MAIL_PASSWORD")
    if not username or not password:
        return None

    return SmtpSettings(
        host=get_configured_env("MAIL_HOST") or "smtp.gmail.com",
        port=int(get_configured_env("MAIL_PORT") or "587"),
        username=username,
        password=password,
        from_email=get_configured_env("FROM_EMAIL") or username,
        to_email=to_email,
        starttls=(get_configured_env("MAIL_STARTTLS") or "true").lower() != "false",
        ssl=(get_configured_env("MAIL_SSL") or "false").lower() == "true",
    )


def send_email(subject, html_body, text_body=None, settings=None):
    settings = settings or load_smtp_settings()
    if not settings:
        raise RuntimeError(
            "SMTP settings incomplete. Set TO_EMAIL plus MAIL_USERNAME and MAIL_PASSWORD, "
            "or set MAIL_CONNECTION."
        )

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = settings.from_email
    message["To"] = settings.to_email
    message.set_content(text_body or "This email contains an HTML arXiv digest.")
    message.add_alternative(html_body, subtype="html")

    if settings.ssl:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(settings.host, settings.port, context=context) as server:
            server.login(settings.username, settings.password)
            server.send_message(message)
    else:
        with smtplib.SMTP(settings.host, settings.port) as server:
            server.ehlo()
            if settings.starttls:
                context = ssl.create_default_context()
                server.starttls(context=context)
                server.ehlo()
            server.login(settings.username, settings.password)
            server.send_message(message)
