from uuid import UUID

from apps.audit.services import log_event
from apps.tenants.models import Tenant
from apps.users.models import User


class AuditEventHandler:
    """
    Converts domain events into immutable audit log records.
    """

    @staticmethod
    def handle(event):
        tenant = None
        actor = None

        if event.tenant_id:
            tenant = Tenant.objects.filter(
                id=event.tenant_id
            ).first()

        if event.actor_id:
            actor = User.objects.filter(
                id=event.actor_id
            ).first()

        entity_id = (
            event.payload.get("protocol_id")
            or event.payload.get("decision_id")
            or event.payload.get("meeting_id")
            or event.payload.get("review_id")
            or event.payload.get("progress_report_id")
            or event.payload.get("incident_report_id")
        )

        if entity_id is not None:
            entity_id = UUID(str(entity_id))

        return log_event(
            action=event.event_type,
            entity_type=event.event_type.split(".")[0],
            entity_id=entity_id,
            actor=actor,
            tenant=tenant,
            payload=event.payload,
            event_id=event.event_id,
            occurred_at=event.occurred_at,
        )
