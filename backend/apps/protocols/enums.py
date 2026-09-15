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


class PreliminaryCheckResult(models.TextChoices):
    INCOMPLETE = "incomplete", "Incomplete"
    COMPLETE = "complete", "Complete"


class SubmissionDocumentType(models.TextChoices):
    RESEARCH_INTRODUCTION = "research_introduction", "Research Introduction"
    METHODOLOGY = "methodology", "Methodology"
    RISK_ASSESSMENT = "risk_assessment", "Risk Assessment"
    INFORMED_CONSENT = "informed_consent", "Informed Consent"
    QUESTIONNAIRE = "questionnaire", "Questionnaire"
    DATA_PROTECTION_PLAN = "data_protection_plan", "Data Protection Plan"
    AI_CYBER_ASSESSMENT = "ai_cyber_assessment", "AI/Cyber Assessment"
    PI_SIGNATURE = "pi_signature", "PI Signature"
    OTHER = "other", "Other"
