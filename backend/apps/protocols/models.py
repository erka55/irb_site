from django.db import models

from apps.core.models import BaseModel
from apps.tenants.models import Tenant
from apps.users.models import User

from .enums import (
    PreliminaryCheckResult,
    ProtocolStatus,
    RiskLevel,
    SubmissionStatus,
    SubmissionDocumentType,
)

class Protocol(BaseModel):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name="protocols",
    )

    title = models.CharField(
        max_length=500,
    )

    protocol_number = models.CharField(
        max_length=50,
        unique=True,
    )

    principal_investigator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="investigator_protocols",
    )

    risk_level = models.CharField(
        max_length=20,
        choices=RiskLevel.choices,
    )

    status = models.CharField(
        max_length=30,
        choices=ProtocolStatus.choices,
        default=ProtocolStatus.DRAFT,
    )

    summary = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "protocols"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ProtocolVersion(BaseModel):

    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.CASCADE,
        related_name="versions",
    )

    version_number = models.CharField(
        max_length=20,
    )

    snapshot = models.JSONField()

    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="created_protocol_versions",
    )

    class Meta:
        db_table = "protocol_versions"
        ordering = ["-created_at"]


class ProtocolStatusHistory(BaseModel):

    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.CASCADE,
        related_name="status_history",
    )

    from_status = models.CharField(
        max_length=30,
        blank=True,
    )

    to_status = models.CharField(
        max_length=30,
    )

    changed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="protocol_status_changes",
    )
    
    reason = models.TextField(
        blank=True,
    )

    class Meta:
        db_table = "protocol_status_history"
        ordering = ["-created_at"]

class ProtocolSubmission(BaseModel):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="protocol_submissions",
    )

    protocol = models.ForeignKey(
        Protocol,
        on_delete=models.PROTECT,
        related_name="submissions",
    )

    submitted_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="protocol_submissions",
    )

    submitted_at = models.DateTimeField()

    status = models.CharField(
        max_length=30,
        choices=SubmissionStatus.choices,
        default=SubmissionStatus.RECEIVED,
    )

    incomplete_reason = models.TextField(
        blank=True,
    )

    closed_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "protocol_submissions"
        ordering = ["-submitted_at"]

class SubmissionDocument(BaseModel):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="submission_documents",
    )

    submission = models.ForeignKey(
        ProtocolSubmission,
        on_delete=models.PROTECT,
        related_name="documents",
    )

    document_type = models.CharField(
        max_length=50,
        choices=SubmissionDocumentType.choices,
    )

    file_reference = models.CharField(
        max_length=500,
    )

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="uploaded_submission_documents",
    )

    uploaded_at = models.DateTimeField()

    class Meta:
        db_table = "submission_documents"
        ordering = ["-uploaded_at"]

class PreliminaryCheck(BaseModel):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.PROTECT,
        related_name="preliminary_checks",
    )

    submission = models.ForeignKey(
        ProtocolSubmission,
        on_delete=models.PROTECT,
        related_name="preliminary_checks",
    )

    checked_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="preliminary_checks",
    )

    checked_at = models.DateTimeField()

    result = models.CharField(
        max_length=20,
        choices=PreliminaryCheckResult.choices,
    )

    missing_document_types = models.JSONField(
        default=list,
        blank=True,
    )

    correction_due_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        db_table = "preliminary_checks"
        ordering = ["-checked_at"]
