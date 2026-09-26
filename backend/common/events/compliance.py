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
