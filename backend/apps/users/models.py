from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import UserManager

from apps.core.models import (
    BaseModel,
    RoleChoices,
)

from apps.tenants.models import Tenant

class User(AbstractUser):

    username = None

    email = models.EmailField(
        unique=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

class Membership(BaseModel):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    role = models.CharField(
        max_length=30,
        choices=RoleChoices.choices,
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        db_table = "memberships"

        constraints = [
            models.UniqueConstraint(
                fields=["user", "tenant", "role"],
                name="unique_user_tenant_role",
            )
        ]

    def __str__(self):
        return (
            f"{self.user.email} - "
            f"{self.tenant.code} - "
            f"{self.role}"
        )
