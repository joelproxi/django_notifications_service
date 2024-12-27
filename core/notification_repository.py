from typing import Optional
from uuid import UUID
from core.dataclasses import Notification
from core.models import DjangoNotificationModel


class NotificationRepository:
    def _to_entity(self, model: DjangoNotificationModel) -> Notification:
        return Notification(
            id=model.id,
            notification_type=model.notification_type,
            recipient=model.recipient,
            content=model.content,
            status=model.status,
            service_name=model.service_name,
            metadata=model.metadata,
            created_at=model.created_at,
            scheduled_for=model.scheduled_for,
            sent_at=model.sent_at,
            error_message=model.error_message,
            retry_count=model.retry_count
        )

    async def save(self, notification: Notification) -> Notification:
        print(f"Saving notification {notification}")
        model = await DjangoNotificationModel.objects.acreate(
            id=notification.id,
            notification_type=notification.notification_type,
            recipient=notification.recipient,
            content=notification.content,
            status=notification.status,
            service_name=notification.service_name,
            metadata=notification.metadata,
            scheduled_for=notification.scheduled_for,
            sent_at=notification.sent_at,
            error_message=notification.error_message,
            retry_count=notification.retry_count
        )
        return model

    async def get_by_id(self, notification_id: UUID) -> Optional[Notification]:
        try:
            model = await DjangoNotificationModel.objects.aget(id=notification_id)
            return self._to_entity(model)
        except DjangoNotificationModel.DoesNotExist:
            return None

    async def update_status(self, notification: Notification) -> None:
        try:
            notification_model = await DjangoNotificationModel.objects.aget(id=notification.id)
            notification_model.status = notification.status
            notification_model.sent_at = notification.sent_at
            notification_model.error_message = notification.error_message
            notification_model.retry_count = notification.retry_count
            await notification_model.asave()
        except DjangoNotificationModel.DoesNotExist:
            raise ValueError(f"Notification with id {notification.id} not found")
        except Exception as e:
            raise ValueError(f"Error updating notification status: {str(e)}")