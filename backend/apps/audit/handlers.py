from uuid import UUID

from apps.audit.services import log_event
from apps.protocols.models import ClassificationAssessment, Protocol
from apps.protocols.models import ProtocolSubmission
from apps.reviews.models import Review
from apps.meetings.models import Meeting
from apps.decision.models import Decision
from apps.monitoring.models import ProgressReport, IncidentReport
from apps.compliance.models import (
    ConflictOfInterestRecusal,
    MeetingMinutesRecusal,
)
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
        EventTypes.SUBMISSION_RESUBMITTED: (
            "submission",
            "submission_id",
        ),
        EventTypes.CLASSIFICATION_ASSESSED: (
            "classification_assessment",
            "assessment_id",
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
        EventTypes.CONFLICT_OF_INTEREST_RECUSED: (
            "conflict_of_interest_recusal",
            "recusal_id",
        ),
        EventTypes.CONFLICT_OF_INTEREST_MINUTES_RECORDED: (
            "meeting_minutes_recusal",
            "minutes_recusal_id",
        ),
    }

    ENTITY_MODELS = {
        "protocol": Protocol,
        "submission": ProtocolSubmission,
        "classification_assessment": ClassificationAssessment,
        "review": Review,
        "meeting": Meeting,
        "decision": Decision,
        "progress_report": ProgressReport,
        "incident_report": IncidentReport,
        "conflict_of_interest_recusal": ConflictOfInterestRecusal,
        "meeting_minutes_recusal": MeetingMinutesRecusal,
    }

    @classmethod
    def _validate_entity_tenant(cls, *, entity_type, entity_id, tenant):
        model = cls.ENTITY_MODELS[entity_type]

        entity = model.objects.filter(
            id=entity_id
        ).first()

        if entity is None:
            raise ValueError(
                f"{entity_type} not found: {entity_id}"
            )

        if entity.tenant_id != tenant.id:
            raise ValueError(
                f"{entity_type} belongs to a different tenant."
            )

        return entity

    @classmethod
    def handle(cls, event):
        if not event.tenant_id:
            raise ValueError("Tenant is required for audit events.")

        tenant = Tenant.objects.filter(
            id=event.tenant_id
        ).first()

        if tenant is None:
            raise ValueError(
                f"Tenant not found: {event.tenant_id}"
            )

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

        cls._validate_entity_tenant(
            entity_type=entity_type,
            entity_id=entity_id,
            tenant=tenant,
        )

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
