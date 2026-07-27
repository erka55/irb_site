from common.events.memory import InMemoryEventPublisher
from common.events.review import ReviewsCompleted

from apps.reviews.services.aggregation_service import (
    ReviewAggregationService,
)
from common.events.base import BaseEvent

class ReviewOrchestrationService:

    @staticmethod
    def handle_review_completed(event: BaseEvent) -> None:

        protocol_id = event.payload["protocol_id"]

        quorum = (
            ReviewAggregationService.check_quorum(
                protocol_id
            )
        )

        if not quorum:
            print(
                "[ORCHESTRATION] "
                "Waiting for remaining reviews."
            )
            return

        recommendation = (
            ReviewAggregationService.generate_recommendation(
                protocol_id
            )
        )

        print(
            "[ORCHESTRATION] "
            f"Recommendation={recommendation}"
        )

        publisher = InMemoryEventPublisher()

        publisher.publish(
            ReviewsCompleted(
                tenant_id=event.tenant_id,
                actor_id=event.actor_id,
                protocol_id=protocol_id,
            )
        )
