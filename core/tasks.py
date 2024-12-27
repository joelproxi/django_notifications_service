import asyncio
import datetime
import json
import logging
from uuid import uuid4
from celery import shared_task
from django.utils.timezone import datetime
from core.dataclasses import Notification
from core.notification_repository import NotificationRepository
from core.utils import send_email_notification_task

logger = logging.getLogger(__name__)


@shared_task
def process_notification(notification_data):
    """Process notification based on type"""
    try:
        print(type(notification_data))
        print(notification_data)
        # Désérialiser les données de notification si nécessaire
        if isinstance(notification_data, str):
            notification_data = json.loads(notification_data)
            
        notification_type = notification_data.get('notification_type')
        recipient = notification_data.get('recipient')
        message_content = notification_data.get('content')
        service_name = notification_data.get('service_name')
        metadata = notification_data.get('metadata', {})

        # Créer et sauvegarder la notification initiale
        notification = Notification(
            id=uuid4(),
            notification_type=notification_type,
            recipient=recipient,
            content=message_content,
            status='pending',
            service_name=service_name,
            metadata=metadata,
            created_at=notification_data.get('created_at', datetime),
            scheduled_for=datetime.now(),
            sent_at=datetime.now(),
            error_message=str('None')
        )
        
        repo = NotificationRepository()
        saved_notification = asyncio.run(repo.save(notification))
   
        if notification_type == 'email':
            send_email_notification_task(
                recipient,
                message_content)
            print(f"Sent email notification to {recipient}")
        # elif notification_type == 'sms':
        #     send_sms_notification_task.delay(recipient, message_content)
        #     print(f"Sent SMS notification to {recipient}")
        # elif notification_type == 'slack':
        #     send_slack_notification_task.delay(recipient, message_content)
        #     print(f"Sent Slack notification to {recipient}")
        # elif notification_type == 'whatsapp':
        #     send_whatsapp_notification_task.delay(recipient, message_content)
        #     print(f"Sent WhatsApp notification to {recipient}")
        else:
            logger.warning(f"Unknown notification type: {notification_type}")
            print(f"Unknown notification type: {notification_type}")
        print(saved_notification)
        saved_notification.status = 'sent'
        saved_notification.sent_at = datetime.now()
        asyncio.run(repo.update_status(saved_notification))

    except Exception as e:
        logger.error(f"Error processing notification: {e}")
        saved_notification.status = 'failed'
        saved_notification.error_message = str(e)
        asyncio.run(repo.update_status(saved_notification))
        raise