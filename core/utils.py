from typing import Any, Dict
from django.core.mail import send_mail
from django.conf import settings
# from twilio.rest import Client


def send_email_notification_task(recipient: str, content: Dict[str, Any]):
    """Envoie une notification par e-mail."""
    send_mail(
        subject=content.get('subject', 'Notification'),
        message=content.get('body'),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[recipient],
        fail_silently=True,
    )
    print(f"Sent email notification to {recipient}")


def send_sms_notification(phone_number: str, message: str):
    """Envoie une notification par SMS."""
    # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    # client.messages.create(
    #     body=message,
    #     from_=settings.TWILIO_PHONE_NUMBER,
    #     to=phone_number
    # )
    pass


def send_slack_notification(channel: str, message: str):
    """Envoie une notification via Slack."""
    # client = WebClient(token=settings.SLACK_API_TOKEN)
    # client.chat_postMessage(channel=channel, text=message)
    pass


def send_whatsapp_notification(phone_number: str, message: str):
    """Envoie une notification via WhatsApp."""
    # client = WhatsAppClient(settings.WHATSAPP_API_TOKEN)
    # client.send_message(to=phone_number, body=message)
    pass