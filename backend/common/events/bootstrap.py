from apps.reviews.services.orchestration import ReviewOrchestrationService
from apps.decision.services.orchestration import DecisionOrchestrationService
from apps.notifications.handlers import NotificationHandler
from apps.meetings.handlers import MeetingHandler
from apps.monitoring.handlers import MonitoringHandler
from apps.audit.handlers import AuditEventHandler

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


def register_monitoring_handlers():
    registry.register(
        EventTypes.DECISION_PUBLISHED,
        MonitoringHandler.handle_decision_published,
    )


def register_audit_handlers():
    audit_event_types = [
        EventTypes.PROTOCOL_SUBMITTED,
        EventTypes.PROTOCOL_UPDATED,
        EventTypes.PROTOCOL_APPROVED,
        EventTypes.PROTOCOL_REJECTED,
        EventTypes.PROTOCOL_REVISIONS_REQUESTED,

        EventTypes.REVIEW_ASSIGNED,
        EventTypes.REVIEW_SUBMITTED,
        EventTypes.REVIEW_COMPLETED,
        EventTypes.REVIEWS_COMPLETED,

        EventTypes.MEETING_SCHEDULED,
        EventTypes.MEETING_COMPLETED,
        EventTypes.MEETING_CANCELLED,

        EventTypes.DECISION_CREATED,
        EventTypes.DECISION_LETTER_GENERATED,
        EventTypes.DECISION_ISSUED,
        EventTypes.DECISION_PUBLISHED,
        EventTypes.DECISION_LETTER_ISSUED,

        EventTypes.PROGRESS_REPORT_SUBMITTED,
        EventTypes.INCIDENT_REPORT_SUBMITTED,
    ]

    for event_type in audit_event_types:
        registry.register(
            event_type,
            AuditEventHandler.handle,
        )


def register_meeting_handlers():
    registry.register(
        EventTypes.MEETING_COMPLETED,
        MeetingHandler.handle_meeting_completed,
    )

    registry.register(
        EventTypes.MEETING_CANCELLED,
        MeetingHandler.handle_meeting_cancelled,
    )


def register_event_handlers():
    register_review_handlers()
    register_decision_handlers()
    register_notification_handlers()
    register_monitoring_handlers()
    register_audit_handlers()
    register_meeting_handlers()
