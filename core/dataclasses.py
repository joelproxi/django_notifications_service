from dataclasses import dataclass
import datetime
from typing import Any, Dict, Optional
from uuid import UUID


@dataclass
class Notification:
    id: UUID
    notification_type: str
    recipient: str
    content: Dict[str, Any]
    status: str
    service_name: str
    metadata: Optional[Dict[str, Any]]
    created_at: datetime
    scheduled_for: Optional[datetime.datetime] = None
    sent_at: Optional[datetime.datetime] = None
    error_message: Optional[str] = None
    retry_count: int = 0
    
 
@dataclass(frozen=True)
class EmailContent:
    subject: str
    body: str
    html_body: Optional[str] = None


@dataclass(frozen=True)
class NotificationMessage:
    type: str
    recipient: str
    content: Dict[str, Any]
    source_service: str
    metadata: Optional[Dict[str, Any]] = None
    scheduled_for: Optional[datetime] = None