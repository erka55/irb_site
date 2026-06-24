from apps.reviews.models import (
    Review,
    ReviewStatus,
)


class ReviewAggregationService:

    @staticmethod
    def get_submitted_reviews(protocol_id):
        return Review.objects.filter(
            protocol_id=protocol_id,
            status=ReviewStatus.SUBMITTED,
        )

    @staticmethod
    def calculate_average_score(protocol_id):

        reviews = (
            ReviewAggregationService
            .get_submitted_reviews(protocol_id)
        )

        if not reviews.exists():
            return 0

        total = sum(
            review.score
            for review in reviews
            if review.score is not None
        )

        return total / reviews.count()

    @staticmethod
    def check_quorum(
        protocol_id,
        required_reviews=2,
    ):

        count = (
            ReviewAggregationService
            .get_submitted_reviews(protocol_id)
            .count()
        )

        return count >= required_reviews

    @staticmethod
    def generate_recommendation(
        protocol_id,
    ):

        avg_score = (
            ReviewAggregationService
            .calculate_average_score(
                protocol_id
            )
        )

        if avg_score >= 4:
            return "APPROVE"

        if avg_score >= 3:
            return "APPROVE_WITH_CHANGES"

        return "DEFER"
