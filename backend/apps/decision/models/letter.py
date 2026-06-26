from django.db import models

from apps.core.models import BaseModel
from apps.users.models import User

from apps.decision.enums import LetterStatus


class DecisionLetter(BaseModel):

    decision = models.ForeignKey(
        "decision.Decision",
        on_delete=models.CASCADE,
        related_name="letters",
    )

    version = models.PositiveIntegerField(
        default=1,
    )

    status = models.CharField(
        max_length=20,
        choices=LetterStatus.choices,
        default=LetterStatus.DRAFT,
    )

    generated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    generated_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="generated_decision_letters",
    )

    file_path = models.CharField(
        max_length=500,
        blank=True,
    )

    class Meta:
        db_table = "decision_letters"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Decision Letter "
            f"v{self.version}"
        )
