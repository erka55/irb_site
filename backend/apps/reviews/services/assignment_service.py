from apps.reviews.models import (
    Review,
    ReviewAssignment,
    AssignmentRole,
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

        # TODO:
        # publish ReviewAssigned event

        return assignment, review
