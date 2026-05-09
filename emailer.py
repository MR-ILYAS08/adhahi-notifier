import smtplib
from email.mime.text import MIMEText
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM
from logger import log


def send_email(to: str, wilaya_name: str):
    body = f"""Bonjour,

Les quotas Adha sont maintenant disponibles pour la wilaya de {wilaya_name}.

Rendez-vous sur https://adhahi.dz pour réserver votre place.

Cordialement,
Le service de notification Adhahi
"""
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = f"Adhahi disponible – {wilaya_name}"
    msg["From"]    = EMAIL_FROM
    msg["To"]      = to

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        log.info(f"Email sent to {to} for {wilaya_name}")
    except Exception as e:
        log.error(f"Email failed for {to}: {e}")
