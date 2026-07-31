from apps.decision.models import Decision

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
        pass

    @staticmethod
    def handle_review_assigned(event):
        pass

    @staticmethod
    def handle_reviews_completed(event):
        pass

    @staticmethod
    def handle_decision_published(event):

        decision = (
            Decision.objects
            .select_related(
                "tenant",
                "protocol__principal_investigator",
            )
            .filter(
                id=event.payload["decision_id"],
            )
            .first()
        )

        if decision is None:
            return

        NotificationService.create_notification(
            tenant=decision.tenant,
            recipient=decision.protocol.principal_investigator,
            type=NotificationType.DECISION_ISSUED,
            channel=NotificationChannel.IN_APP,
            title="Decision Published",
            message=(
                f"A decision has been published for "
                f"'{decision.protocol.title}'."
            ),
            payload={
                "decision_id": str(decision.id),
                "protocol_id": str(decision.protocol.id),
            },
        )
