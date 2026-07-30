from django.utils import timezone

from .enums import NotificationStatus
from .repository import NotificationRepository
from .selectors import NotificationSelector


class NotificationService:
    """
    Notification business logic.
    """

    @staticmethod
    def create_notification(**kwargs):
        return NotificationRepository.create(**kwargs)

    @staticmethod
    def mark_as_read(notification_id):
        notification = NotificationSelector.get(notification_id)

        if notification is None:
            return None

        notification.status = NotificationStatus.READ
        notification.read_at = timezone.now()

        return NotificationRepository.save(notification)

    @staticmethod
    def dispatch_notification(notification_id):
        notification = NotificationSelector.get(notification_id)

        if notification is None:
            return None

        notification.status = NotificationStatus.SENT
        notification.sent_at = timezone.now()

        return NotificationRepository.save(notification)
