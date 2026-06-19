from django.db import models

from apps.core.models import BaseModel, StatusChoices


class Tenant(BaseModel):
    """
    Institution / organization.
    """

    code = models.SlugField(
        unique=True,
        max_length=50,
    )

    name = models.CharField(
        max_length=255,
    )

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )

    contact_email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=50,
        blank=True,
    )

    class Meta:
        db_table = "tenants"
        ordering = ["name"]

    def __str__(self):
        return self.name
