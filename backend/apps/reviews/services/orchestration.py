from common.events.base import BaseEvent

from apps.reviews.services.aggregation_service import (
    ReviewAggregationService,
)


class ReviewOrchestrationService:

    @staticmethod
    def handle_review_completed(event: BaseEvent) -> None:

        protocol_id = event.payload["protocol_id"]

        quorum = (
            ReviewAggregationService.check_quorum(
                protocol_id
            )
        )

        recommendation = (
            ReviewAggregationService.generate_recommendation(
                protocol_id
            )
        )

        print(
            f"[ORCHESTRATION] "
            f"quorum={quorum}, "
            f"recommendation={recommendation}"
        )

        # Sprint 5 next step:
        # if quorum:
        #     publish ReviewsCompleted
