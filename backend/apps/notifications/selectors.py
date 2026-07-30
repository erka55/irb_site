from django.contrib.auth import get_user_model

from .enums import NotificationStatus
from .models import Notification

User = get_user_model()


class NotificationSelector:
    """
    Read-only queries for notifications.
    """

    @staticmethod
    def get(notification_id):
        return (
            Notification.objects.filter(
                id=notification_id,
                is_deleted=False,
            )
            .select_related("tenant", "recipient")
            .first()
        )

    @staticmethod
    def list_for_user(user: User):
        return (
            Notification.objects.filter(
                recipient=user,
                is_deleted=False,
            )
            .select_related("tenant")
            .order_by("-created_at")
        )

    @staticmethod
    def list_unread_for_user(user: User):
        return (
            Notification.objects.filter(
                recipient=user,
                status=NotificationStatus.PENDING,
                is_deleted=False,
            )
            .select_related("tenant")
            .order_by("-created_at")
        )

    @staticmethod
    def unread_count(user: User):
        return Notification.objects.filter(
            recipient=user,
            status=NotificationStatus.PENDING,
            is_deleted=False,
        ).count()
