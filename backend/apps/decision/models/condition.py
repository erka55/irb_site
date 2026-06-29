from django.db import models

from apps.core.models import BaseModel
from .decision import Decision


class Condition(BaseModel):
    """
    A condition attached to a conditional IRB decision.
    """

    decision = models.ForeignKey(
        Decision,
        on_delete=models.CASCADE,
        related_name="conditions",
    )

    description = models.TextField()

    is_completed = models.BooleanField(default=False)

    class Meta:
        db_table = "decision_conditions"
        ordering = ["created_at"]

    def __str__(self):
        return f"Condition #{self.pk}"
