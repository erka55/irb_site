from .base import BaseEvent
from common.events.types import EventTypes

class DecisionCreated(BaseEvent):
    """
    Published when a draft decision is created.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        protocol_id,
        decision_id,
    ):
        super().__init__(
            event_type=EventTypes.DECISION_CREATED,
            tenant_id=str(tenant_id),
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
                "decision_id": str(decision_id),
            },
        )
