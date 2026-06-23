from django.db import models


class AssignmentRole(models.TextChoices):
    PRIMARY = "PRIMARY", "Primary"
    SECONDARY = "SECONDARY", "Secondary"

class ReviewAssignment(models.Model):
    protocol_id = models.UUIDField()

    reviewer_id = models.UUIDField()

    role = models.CharField(
        max_length=20,
        choices=AssignmentRole.choices,
        default=AssignmentRole.PRIMARY,
    )

    assigned_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = "review_assignments"
