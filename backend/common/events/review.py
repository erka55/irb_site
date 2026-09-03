from .base import BaseEvent
from common.events.types import EventTypes

class ReviewAssigned(BaseEvent):
    """
    Published when a reviewer is assigned to a protocol.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        protocol_id,
        review_id,
        reviewer_id,
    ):
        super().__init__(
            event_type=EventTypes.REVIEW_ASSIGNED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
                "review_id": str(review_id),
                "reviewer_id": str(reviewer_id),
            },
        )

class ReviewCompleted(BaseEvent):
    """
    Published when an individual review is submitted.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        protocol_id,
        review_id,
        reviewer_id,
    ):
        super().__init__(
            event_type=EventTypes.REVIEW_COMPLETED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
                "review_id": str(review_id),
                "reviewer_id": str(reviewer_id),
            },
        )


class ReviewsCompleted(BaseEvent):
    """
    Published when all required reviews for a protocol
    have been completed.
    """

    def __init__(
        self,
        tenant_id,
        actor_id,
        protocol_id,
    ):
        super().__init__(
            event_type=EventTypes.REVIEWS_COMPLETED,
            tenant_id=str(tenant_id) if tenant_id else None,
            actor_id=str(actor_id) if actor_id else None,
            payload={
                "protocol_id": str(protocol_id),
            },
        )
