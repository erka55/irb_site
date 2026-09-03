from .base import BaseEvent
from common.events.types import EventTypes


class MeetingScheduled(BaseEvent):
    """
    Published when a committee meeting is scheduled.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        meeting_id,
        protocol_id,
    ):
        super().__init__(
            event_type=EventTypes.MEETING_SCHEDULED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "meeting_id": str(meeting_id),
                "protocol_id": str(protocol_id),
            },
        )


class MeetingCompleted(BaseEvent):
    """
    Published when a committee meeting has been completed.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        meeting_id,
    ):
        super().__init__(
            event_type=EventTypes.MEETING_COMPLETED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "meeting_id": str(meeting_id),
            },
        )


class MeetingCancelled(BaseEvent):
    """
    Published when a committee meeting is cancelled.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        meeting_id,
    ):
        super().__init__(
            event_type=EventTypes.MEETING_CANCELLED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "meeting_id": str(meeting_id),
            },
        )
