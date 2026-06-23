from apps.reviews.models import Review


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
    def submit_review(review):
        review.status = "SUBMITTED"
        review.save()

        return review
