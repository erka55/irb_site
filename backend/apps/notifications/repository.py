from .models import Notification


class NotificationRepository:
    """
    Repository for Notification persistence operations.
    """

    @staticmethod
    def create(**kwargs) -> Notification:
        """
        Create a new notification.
        """
        return Notification.objects.create(**kwargs)

    @staticmethod
    def save(notification: Notification) -> Notification:
        """
        Save notification changes.
        """
        notification.save()
        return notification
