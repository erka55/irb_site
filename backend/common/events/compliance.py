from .base import BaseEvent
from common.events.types import EventTypes


class ConflictOfInterestRecused(BaseEvent):
    """
    Published when a participant is recused from an agenda
    because of a conflict of interest.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        recusal_id,
        declaration_id,
        agenda_id,
        participant_id,
    ):
        super().__init__(
            event_type=EventTypes.CONFLICT_OF_INTEREST_RECUSED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "recusal_id": str(recusal_id),
                "declaration_id": str(declaration_id),
                "agenda_id": str(agenda_id),
                "participant_id": str(participant_id),
            },
        )

class EthicsViolationRecorded(BaseEvent):
    """
    Published when an ethics violation is recorded
    against a research protocol.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        violation_id,
        protocol_id,
        violation_type,
    ):
        super().__init__(
            event_type=EventTypes.ETHICS_VIOLATION_RECORDED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "violation_id": str(violation_id),
                "protocol_id": str(protocol_id),
                "violation_type": violation_type,
            },
        )
