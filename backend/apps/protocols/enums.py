from django.db import models

class RiskLevel(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"


class ProtocolStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SUBMITTED = "submitted", "Submitted"
    UNDER_REVIEW = "under_review", "Under Review"
    APPROVED = "approved", "Approved"
    REJECTED = "rejected", "Rejected"
    REVISIONS_REQUIRED = "revisions_required", "Revisions Required"
    ARCHIVED = "archived", "Archived"

class SubmissionStatus(models.TextChoices):
    RECEIVED = "received", "Received"
    INCOMPLETE = "incomplete", "Incomplete"
    COMPLETE = "complete", "Complete"
    CLOSED = "closed", "Closed"
