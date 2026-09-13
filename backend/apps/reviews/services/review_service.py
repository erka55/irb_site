from common.events.factory import get_event_publisher
from common.events.review import ReviewCompleted
from django.utils import timezone

from apps.protocols.models import Protocol
from apps.reviews.models import (
    Review,
    ReviewStatus,
)


class ReviewService:

    @staticmethod
    def get_protocol_reviews(protocol_id):
        return Review.objects.filter(
            protocol_id=protocol_id
        )

    @staticmethod
    def get_reviewer_reviews(reviewer_id):
        return Review.objects.filter(
            reviewer_id=reviewer_id
        )

    @staticmethod
    def submit_review(
        review,
        recommendation,
        score,
        comments,
    ):

        # Rule 1
        if review.status == ReviewStatus.SUBMITTED:
            raise ValueError(
                "Review already submitted"
            )

        # Rule 2
        if score < 1 or score > 5:
            raise ValueError(
                "Score must be between 1 and 5"
            )

        review.recommendation = recommendation
        review.score = score
        review.comments = comments

        review.status = ReviewStatus.SUBMITTED
        review.submitted_at = timezone.now()

        review.save()

        protocol = Protocol.objects.select_related(
            "tenant"
        ).get(id=review.protocol_id)

        publisher = get_event_publisher()

        publisher.publish(
            ReviewCompleted(
                tenant_id=protocol.tenant_id,
                actor_id=str(review.reviewer_id),
                protocol_id=review.protocol_id,
                review_id=review.id,
                reviewer_id=review.reviewer_id,
            )
        )

        return review

    @staticmethod
    def get_pending_reviews(reviewer_id):
        return Review.objects.filter(
            reviewer_id=reviewer_id,
            status=ReviewStatus.ASSIGNED,
        )

    @staticmethod
    def get_submitted_reviews(reviewer_id):
        return Review.objects.filter(
            reviewer_id=reviewer_id,
            status=ReviewStatus.SUBMITTED,
        )

    @staticmethod
    def get_review(review_id):
        return Review.objects.get(
            id=review_id
        )
