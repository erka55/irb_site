from common.events.memory import InMemoryEventPublisher
from common.events.review import ReviewAssigned

from apps.protocols.models import Protocol
from apps.reviews.models import (
    AssignmentRole,
    Review,
    ReviewAssignment,
    ReviewStatus,
)


class ReviewAssignmentService:

    @staticmethod
    def assign_reviewer(
        protocol_id,
        reviewer_id,
        role=AssignmentRole.PRIMARY,
    ):
        existing = ReviewAssignment.objects.filter(
            protocol_id=protocol_id,
            reviewer_id=reviewer_id,
        ).exists()

        if existing:
            raise ValueError(
                "Reviewer already assigned"
            )

        protocol = Protocol.objects.select_related(
            "tenant"
        ).get(id=protocol_id)

        assignment = ReviewAssignment.objects.create(
            protocol_id=protocol_id,
            reviewer_id=reviewer_id,
            role=role,
        )

        review = Review.objects.create(
            protocol_id=protocol_id,
            reviewer_id=reviewer_id,
            status=ReviewStatus.ASSIGNED,
        )

        publisher = InMemoryEventPublisher()

        publisher.publish(
            ReviewAssigned(
                tenant_id=protocol.tenant_id,
                actor_id=None,
                protocol_id=protocol_id,
                review_id=review.id,
                reviewer_id=reviewer_id,
            )
        )

        return assignment, review
