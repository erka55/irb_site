from django.db import models

from apps.core.models import BaseModel
from apps.protocols.models import Protocol
from apps.tenants.models import Tenant
from apps.users.models import User


class ConflictOfInterestDeclaration(BaseModel):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="conflict_of_interest_declarations",
    )
    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.PROTECT,
        related_name="conflict_of_interest_declarations",
    )
    declarant = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="conflict_of_interest_declarations",
    )
    conflict_types = models.JSONField(
        default=list,
        blank=True,
    )
    description = models.TextField()
    declared_at = models.DateTimeField()
    signature_reference = models.CharField(
        max_length=500,
        blank=True,
    )

    class Meta:
        db_table = "conflict_of_interest_declarations"
        ordering = ["-declared_at"]
