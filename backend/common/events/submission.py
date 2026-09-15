from .base import BaseEvent
from common.events.types import EventTypes


class SubmissionResubmitted(BaseEvent):
    def __init__(
        self,
        tenant_id,
        actor_id,
        submission_id,
        protocol_id,
    ):
        super().__init__(
            event_type=EventTypes.SUBMISSION_RESUBMITTED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "submission_id": str(submission_id),
                "protocol_id": str(protocol_id),
            },
        )
