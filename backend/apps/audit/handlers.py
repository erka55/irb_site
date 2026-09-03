from uuid import UUID

from apps.audit.services import log_event
from apps.tenants.models import Tenant
from apps.users.models import User
from common.events.types import EventTypes


class AuditEventHandler:
    """
    Converts domain events into immutable audit log records.

    Each event type has an explicit canonical audit entity.
    """

    ENTITY_MAPPING = {
        EventTypes.PROTOCOL_SUBMITTED: (
            "protocol",
            "protocol_id",
        ),
        EventTypes.PROTOCOL_UPDATED: (
            "protocol",
            "protocol_id",
        ),
        EventTypes.PROTOCOL_APPROVED: (
            "protocol",
            "protocol_id",
        ),
        EventTypes.PROTOCOL_REJECTED: (
            "protocol",
            "protocol_id",
        ),
        EventTypes.PROTOCOL_REVISIONS_REQUESTED: (
            "protocol",
            "protocol_id",
        ),
        EventTypes.REVIEW_ASSIGNED: (
            "review",
            "review_id",
        ),
        EventTypes.REVIEW_SUBMITTED: (
            "review",
            "review_id",
        ),
        EventTypes.REVIEW_COMPLETED: (
            "review",
            "review_id",
        ),
        EventTypes.REVIEWS_COMPLETED: (
            "protocol",
            "protocol_id",
        ),
        EventTypes.MEETING_SCHEDULED: (
            "meeting",
            "meeting_id",
        ),
        EventTypes.MEETING_COMPLETED: (
            "meeting",
            "meeting_id",
        ),
        EventTypes.MEETING_CANCELLED: (
            "meeting",
            "meeting_id",
        ),
        EventTypes.DECISION_CREATED: (
            "decision",
            "decision_id",
        ),
        EventTypes.DECISION_LETTER_GENERATED: (
            "decision",
            "decision_id",
        ),
        EventTypes.DECISION_ISSUED: (
            "decision",
            "decision_id",
        ),
        EventTypes.DECISION_PUBLISHED: (
            "decision",
            "decision_id",
        ),
        EventTypes.DECISION_LETTER_ISSUED: (
            "decision",
            "decision_id",
        ),
        EventTypes.PROGRESS_REPORT_SUBMITTED: (
            "progress_report",
            "progress_report_id",
        ),
        EventTypes.INCIDENT_REPORT_SUBMITTED: (
            "incident_report",
            "incident_report_id",
        ),
    }

    @classmethod
    def handle(cls, event):
        if not event.tenant_id:
            raise ValueError("Tenant is required for audit events.")

        tenant = Tenant.objects.filter(
            id=event.tenant_id
        ).first()

        actor = None

        if event.actor_id:
            actor = User.objects.filter(
                id=event.actor_id
            ).first()

        entity_type, entity_field = cls.ENTITY_MAPPING[
            event.event_type
        ]

        entity_id = event.payload.get(entity_field)

        if entity_id is None:
            raise ValueError(
                f"Missing {entity_field} for "
                f"event type {event.event_type}."
            )

        entity_id = UUID(str(entity_id))

        return log_event(
            action=event.event_type,
            entity_type=entity_type,
            entity_id=entity_id,
            actor=actor,
            tenant=tenant,
            payload=event.payload,
            event_id=event.event_id,
            occurred_at=event.occurred_at,
        )
