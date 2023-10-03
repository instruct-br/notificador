import logging
import requests
from requests.exceptions import ConnectTimeout
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from app.config import SENDGRID_API_KEY, SMTP_REMETENTE

async def enviar_email(notificacao):
    try:
        result = False
        message = Mail(
            from_email=SMTP_REMETENTE,
            to_emails=notificacao["email"],
            subject=notificacao["titulo"],
            html_content=format_to_html(notificacao["mensagem"]),
        )
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        logging.info(f"HTTP Status response from SendGrid: {response.status_code}")
        result = response.status_code in [200,202]
    except Exception as e:
        logging.error(e)
        result = False
    finally:
        return (result, notificacao.get("_id"))


def format_to_html(mensagem):
    return f"<p>{mensagem}</p>"

async def notificar_webhook(notificacao):
    try:
        result = False
        webhook_url = notificacao["webhook"]
        text_to_send = f"{notificacao['titulo']}\n\n{notificacao['mensagem']}"
        response = requests.post(webhook_url, json={"text": text_to_send}, timeout=5)
        result = response.status_code == 200
    except ConnectTimeout:
        logging.warning("Could not process webhook request. Connection time out.")
    finally:
        return (result, notificacao.get("_id"))