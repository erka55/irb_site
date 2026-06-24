from django.utils import timezone

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

        # TODO:
        # publish ReviewSubmitted event

        review.save()

        return review
