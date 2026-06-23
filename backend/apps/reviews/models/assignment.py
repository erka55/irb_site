from django.db import models


class AssignmentRole(models.TextChoices):
    PRIMARY = "PRIMARY", "Primary"
    SECONDARY = "SECONDARY", "Secondary"
