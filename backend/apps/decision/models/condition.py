from django.db import models

from .decision import Decision


class Condition(models.Model):
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

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Condition #{self.pk}"
