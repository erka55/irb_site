from common.events.registry import registry
from apps.reviews.services.orchestration import (
    ReviewOrchestrationService,
)
from apps.decision.services.orchestration import (
    DecisionOrchestrationService,
)
from common.events.types import EventTypes


def register_event_handlers() -> None:
    """
    Register application event handlers.
    """

    registry.register(
        EventTypes.REVIEW_COMPLETED,
        ReviewOrchestrationService.handle_review_completed,
    )

    registry.register(
        EventTypes.REVIEWS_COMPLETED,
        DecisionOrchestrationService.handle_reviews_completed,
    )
