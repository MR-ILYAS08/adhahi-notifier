import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, EMAIL_FROM
from logger import log


def send_email(to: str, wilaya_name: str):
    msg = MIMEMultipart("alternative")
    msg["Subject"]  = f"Adhahi – Quotas disponibles à {wilaya_name}"
    msg["From"]     = f"Adhahi Notifier <admin@adhahi.org>"
    msg["To"]       = to
    msg["Reply-To"] = EMAIL_FROM
    msg["X-Mailer"] = "Adhahi Notifier v1.0"

    body_text = f"""Bonjour,

Les quotas Adha sont maintenant disponibles pour la wilaya de {wilaya_name}.

Réservez votre place sur : https://adhahi.dz

---
Ceci est un email automatique envoyé une seule fois.
Vous ne recevrez plus aucun message de notre part.

Cet email a été envoyé car vous vous êtes inscrit sur adhahi.org.
Pour toute question : admin@adhahi.org
"""

    body_html = f"""
<html>
  <body style="font-family: Arial, sans-serif; color: #1a1a1a; max-width: 480px; margin: auto; padding: 24px;">

    <h2 style="color: #1a6b3c;">Quotas Adha disponibles – {wilaya_name}</h2>

    <p>Bonjour,</p>
    <p>Les quotas Adha sont maintenant ouverts pour la wilaya de <strong>{wilaya_name}</strong>.</p>

    <a href="https://adhahi.dz" style="
      display: inline-block;
      background: #1a6b3c;
      color: white;
      padding: 12px 24px;
      border-radius: 4px;
      text-decoration: none;
      margin: 16px 0;
      font-size: 15px;
    ">Réserver sur adhahi.dz</a>

    <hr style="border: none; border-top: 1px solid #eee; margin-top: 32px;"/>

    <p style="font-size: 12px; color: #999; line-height: 1.6;">
    Ceci est un email automatique envoyé <strong>une seule fois</strong>.<br/>
      Vous ne recevrez plus aucun message de notre part.<br/><br/>
      Cet email a été envoyé car vous vous êtes inscrit sur
      <a href="https://adhahi.org" style="color: #999;">adhahi.org</a>.<br/>
      Pour toute question : <a href="mailto:admin@adhahi.org" style="color: #999;">admin@adhahi.org</a>
    </p>

  </body>
</html>
"""

    msg.attach(MIMEText(body_text, "plain", "utf-8"))
    msg.attach(MIMEText(body_html, "html",  "utf-8"))

    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        log.info(f"Email sent to {to} for {wilaya_name}")
    except Exception as e:
        log.error(f"Email failed for {to}: {e}")
