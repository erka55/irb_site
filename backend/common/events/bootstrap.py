from common.events.registry import registry
from apps.reviews.services.orchestration import (
    ReviewOrchestrationService,
)


def register_event_handlers() -> None:
    """
    Register application event handlers.
    """

    registry.register(
        "review.completed",
        ReviewOrchestrationService.handle_review_completed,
    )
