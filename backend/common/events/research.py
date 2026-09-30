from .base import BaseEvent
from common.events.types import EventTypes


class ResearchCompleted(BaseEvent):
    """
    Published when research completion is formally recorded.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        protocol_id,
        research_completion_id,
    ):
        super().__init__(
            event_type=EventTypes.RESEARCH_COMPLETED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
                "research_completion_id": str(research_completion_id),
            },
        )
