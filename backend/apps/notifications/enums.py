from django.db import models


class NotificationChannel(models.TextChoices):
    IN_APP = "IN_APP", "In-App"
    EMAIL = "EMAIL", "Email"


class NotificationStatus(models.TextChoices):
    PENDING = "PENDING", "Pending"
    SENT = "SENT", "Sent"
    FAILED = "FAILED", "Failed"
    READ = "READ", "Read"


class NotificationType(models.TextChoices):
    PROTOCOL_SUBMITTED = "PROTOCOL_SUBMITTED", "Protocol Submitted"

    REVIEW_ASSIGNED = "REVIEW_ASSIGNED", "Review Assigned"
    REVIEW_REMINDER = "REVIEW_REMINDER", "Review Reminder"
    REVIEW_COMPLETED = "REVIEW_COMPLETED", "Review Completed"

    DECISION_CREATED = "DECISION_CREATED", "Decision Created"
    DECISION_ISSUED = "DECISION_ISSUED", "Decision Issued"

    SYSTEM = "SYSTEM", "System"