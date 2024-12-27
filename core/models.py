from django.db import models


class DjangoNotificationModel(models.Model):
    TYPE_MESSAGE = (
        ('email', 'EMAIL'),
        ('sms', 'SMS'),
        ('push', 'PUSH'),
        ('whatsapp', 'WHATSAPP'),
        ('telegram', 'TELEGRAM'),
        ('slack', 'SLACK'),
        ('webhook', 'WEBHOOK'),
    )
    TYPE_STATUS = (
        ('pending', 'PENDING'),
        ('sent', 'SENT'),
        ('failed', 'FAILED'),
        ('cancelled', 'CANCELLED'),
    )
    id = models.UUIDField(primary_key=True)
    notification_type = models.CharField(
        max_length=50,
        choices=TYPE_MESSAGE,
        default='email')
    status = models.CharField(
        max_length=50,
        choices=TYPE_STATUS,
        default='pending')
    recipient = models.CharField(max_length=255)
    content = models.JSONField()
    metadata = models.JSONField()
    service_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_for = models.DateTimeField(blank=True)
    sent_at = models.DateTimeField(blank=True)
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    