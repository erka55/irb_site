from .enums import (
    NotificationChannel,
    NotificationType,
)

from .services import NotificationService


class NotificationHandler:
    """
    Event handlers for notification workflows.
    """

    @staticmethod
    def handle_protocol_submitted(event):
        NotificationService.create_notification(
            tenant=event.tenant,
            recipient=event.recipient,
            type=NotificationType.PROTOCOL_SUBMITTED,
            channel=NotificationChannel.IN_APP,
            title="Protocol Submitted",
            message=f"Protocol '{event.protocol_title}' has been submitted.",
            payload={
                "protocol_id": str(event.protocol_id),
            },
        )

    @staticmethod
    def handle_review_assigned(event):
        NotificationService.create_notification(
            tenant=event.tenant,
            recipient=event.reviewer,
            type=NotificationType.REVIEW_ASSIGNED,
            channel=NotificationChannel.IN_APP,
            title="Review Assigned",
            message=f"You have been assigned to review '{event.protocol_title}'.",
            payload={
                "protocol_id": str(event.protocol_id),
            },
        )

    @staticmethod
    def handle_decision_issued(event):
        NotificationService.create_notification(
            tenant=event.tenant,
            recipient=event.recipient,
            type=NotificationType.DECISION_ISSUED,
            channel=NotificationChannel.IN_APP,
            title="Decision Issued",
            message=f"A decision has been issued for '{event.protocol_title}'.",
            payload={
                "protocol_id": str(event.protocol_id),
            },
        )
