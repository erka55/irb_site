from django.db import models


class DecisionType(models.TextChoices):
    APPROVED = "approved", "Approved"

    APPROVED_WITH_CONDITIONS = (
        "approved_with_conditions",
        "Approved With Conditions",
    )

    REVISION_REQUIRED = (
        "revision_required",
        "Revision Required",
    )

    REJECTED = "rejected", "Rejected"


class LetterStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    FINAL = "final", "Final"
