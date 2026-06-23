from django.db import models


class ReviewStatus(models.TextChoices):
    ASSIGNED = "ASSIGNED", "Assigned"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    SUBMITTED = "SUBMITTED", "Submitted"
    OVERDUE = "OVERDUE", "Overdue"

class ReviewRecommendation(models.TextChoices):
    APPROVE = "APPROVE", "Approve"
    APPROVE_WITH_CHANGES = (
        "APPROVE_WITH_CHANGES",
        "Approve With Changes",
    )
    DEFER = "DEFER", "Defer"
    REJECT = "REJECT", "Reject"

class Review(models.Model):
    protocol_id = models.UUIDField()

    reviewer_id = models.UUIDField()

    status = models.CharField(
        max_length=30,
        choices=ReviewStatus.choices,
        default=ReviewStatus.ASSIGNED,
    )

    recommendation = models.CharField(
        max_length=50,
        choices=ReviewRecommendation.choices,
        null=True,
        blank=True,
    )

    score = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True,
    )

    comments = models.TextField(
        blank=True,
        default=""
    )

    due_date = models.DateTimeField()

    submitted_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        db_table = "reviews"
