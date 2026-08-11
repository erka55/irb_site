from .base import BaseEvent
from common.events.types import EventTypes


class ProgressReportSubmitted(BaseEvent):
    """
    Published when a progress report is submitted.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        protocol_id,
        progress_report_id,
    ):
        super().__init__(
            event_type=EventTypes.PROGRESS_REPORT_SUBMITTED,
            tenant_id=str(tenant_id),
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
                "progress_report_id": str(progress_report_id),
            },
        )
