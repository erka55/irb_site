from django.db import models

from .decision import Decision


class Letter(models.Model):
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

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
