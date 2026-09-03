from .base import BaseEvent
from common.events.types import EventTypes


class IncidentReportSubmitted(BaseEvent):
    """
    Published when an incident report is submitted.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        protocol_id,
        incident_report_id,
    ):
        super().__init__(
            event_type=EventTypes.INCIDENT_REPORT_SUBMITTED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
                "incident_report_id": str(incident_report_id),
            },
        )
