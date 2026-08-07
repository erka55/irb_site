from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from .decision import Decision


class PublicationStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    GENERATED = "generated", "Generated"
    PUBLISHED = "published", "Published"


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

    publication_status = models.CharField(
        max_length=20,
        choices=PublicationStatus.choices,
        default=PublicationStatus.DRAFT,
    )

    letter_number = models.CharField(
        max_length=50,
        unique=True,
        null=True,
        blank=True,
    )

    rendered_content = models.TextField(
        blank=True,
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="published_decision_letters",
    )

    class Meta:
        db_table = "decision_letters"
        ordering = ["-created_at"]

    def __str__(self):
        if self.letter_number:
            return f"{self.letter_number} - {self.title}"
        return self.title
