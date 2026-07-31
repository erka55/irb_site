from apps.reviews.services.orchestration import ReviewOrchestrationService
from apps.decision.services.orchestration import DecisionOrchestrationService
from apps.notifications.handlers import NotificationHandler

from .registry import registry
from .types import EventTypes


def register_review_handlers():
    registry.register(
        EventTypes.REVIEW_COMPLETED,
        ReviewOrchestrationService.handle_review_completed,
    )


def register_decision_handlers():
    registry.register(
        EventTypes.REVIEWS_COMPLETED,
        DecisionOrchestrationService.handle_reviews_completed,
    )


def register_notification_handlers():
    registry.register(
        EventTypes.DECISION_PUBLISHED,
        NotificationHandler.handle_decision_published,
    )


def register_audit_handlers():
    """
    Audit handlers will be registered here.
    (Future Sprint)
    """
    pass


def register_event_handlers():
    register_review_handlers()
    register_decision_handlers()
    register_notification_handlers()
    register_audit_handlers()
