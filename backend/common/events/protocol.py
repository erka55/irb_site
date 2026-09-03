from .base import BaseEvent
from common.events.types import EventTypes


class ProtocolSubmitted(BaseEvent):
    def __init__(
        self,
        tenant_id,
        actor_id,
        protocol_id,
    ):
        super().__init__(
            event_type=EventTypes.PROTOCOL_SUBMITTED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
            },
        )


class ProtocolApproved(BaseEvent):
    def __init__(
        self,
        tenant_id,
        actor_id,
        protocol_id,
    ):
        super().__init__(
            event_type=EventTypes.PROTOCOL_APPROVED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
            },
        )


class ProtocolRejected(BaseEvent):
    def __init__(
        self,
        tenant_id,
        actor_id,
        protocol_id,
    ):
        super().__init__(
            event_type=EventTypes.PROTOCOL_REJECTED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
            },
        )


class ProtocolRevisionsRequested(BaseEvent):
    def __init__(
        self,
        tenant_id,
        actor_id,
        protocol_id,
    ):
        super().__init__(
            event_type=EventTypes.PROTOCOL_REVISIONS_REQUESTED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
            },
        )
