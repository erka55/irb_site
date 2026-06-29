from django.db import models

from apps.core.models import BaseModel
from .decision import Decision


class Letter(BaseModel):
    """
    Official IRB decision letter.
    """

    decision = models.ForeignKey(
        Decision,
        on_delete=models.CASCADE,
        related_name="letters",
    )

    title = models.CharField(max_length=255)

    content = models.TextField()

    class Meta:
        db_table = "decision_letters"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
