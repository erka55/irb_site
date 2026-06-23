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
