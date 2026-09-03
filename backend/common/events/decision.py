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
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
                "decision_id": str(decision_id),
            },
        )


class DecisionLetterGenerated(BaseEvent):
    """
    Published when a decision letter is generated.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        protocol_id,
        decision_id,
        letter_id,
    ):
        super().__init__(
            event_type=EventTypes.DECISION_LETTER_GENERATED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
                "decision_id": str(decision_id),
                "letter_id": str(letter_id),
            },
        )


class DecisionPublished(BaseEvent):
    """
    Published when a decision is officially published.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        protocol_id,
        decision_id,
    ):
        super().__init__(
            event_type=EventTypes.DECISION_PUBLISHED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
                "decision_id": str(decision_id),
            },
        )


class DecisionLetterIssued(BaseEvent):
    """
    Published when a decision letter is officially issued.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        protocol_id,
        decision_id,
        letter_id,
    ):
        super().__init__(
            event_type=EventTypes.DECISION_LETTER_ISSUED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
                "decision_id": str(decision_id),
                "letter_id": str(letter_id),
            },
        )
