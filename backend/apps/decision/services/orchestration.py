from common.events.base import BaseEvent

from apps.decision.services.decision_service import (
    DecisionService,
)


class DecisionOrchestrationService:
    """
    Coordinates decision workflow after reviews
    have been completed.
    """

    @staticmethod
    def handle_reviews_completed(
        event: BaseEvent,
    ) -> None:

        protocol_id = event.payload["protocol_id"]

        decision = DecisionService.create_draft(
            protocol_id=protocol_id,
        )

        print(
            f"[ORCHESTRATION] "
            f"Draft decision created: {decision.id}"
        )
