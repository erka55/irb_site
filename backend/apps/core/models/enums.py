from django.db import models

class StatusChoices(models.TextChoices):
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    SUSPENDED = "SUSPENDED", "Suspended"

class RoleChoices(models.TextChoices):
    SUPER_ADMIN = "SUPER_ADMIN", "Super Admin"
    TENANT_ADMIN = "TENANT_ADMIN", "Tenant Admin"

    SECRETARY = "SECRETARY", "Secretary"
    CHAIR = "CHAIR", "Chair"
    REVIEWER = "REVIEWER", "Reviewer"
    PI = "PI", "Principal Investigator"
