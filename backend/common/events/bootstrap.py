from common.events.registry import registry
from apps.reviews.services.orchestration import (
    ReviewOrchestrationService,
)
from apps.decision.services.orchestration import (
    DecisionOrchestrationService,
)


def register_event_handlers() -> None:
    """
    Register application event handlers.
    """

    registry.register(
        "review.completed",
        ReviewOrchestrationService.handle_review_completed,
    )

    registry.register(
        "reviews.completed",
        DecisionOrchestrationService.handle_reviews_completed,
    )
