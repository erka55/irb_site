from datetime import datetime, timezone

from django.test import TestCase

from apps.protocols.enums import SubmissionStatus
from apps.protocols.models import Protocol, ProtocolSubmission
from apps.protocols.enums import ProtocolStatus, RiskLevel
from apps.tenants.models import Tenant
from apps.users.models import User


class ProtocolSubmissionModelTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="submission-tenant",
            name="Submission Tenant",
        )

        self.user = User.objects.create_user(
            email="submission@test.com",
            password="test-password",
        )

        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="Submission Protocol",
            protocol_number="SUBMISSION-001",
            principal_investigator=self.user,
            risk_level=RiskLevel.LOW,
            status=ProtocolStatus.DRAFT,
        )

        self.submitted_at = datetime(
            2026,
            9,
            15,
            1,
            0,
            tzinfo=timezone.utc,
        )

    def test_submission_defaults_to_received(self):
        submission = ProtocolSubmission.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            submitted_by=self.user,
            submitted_at=self.submitted_at,
        )

        self.assertEqual(
            submission.status,
            SubmissionStatus.RECEIVED,
        )

    def test_submission_preserves_tenant_protocol_and_submitter(self):
        submission = ProtocolSubmission.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            submitted_by=self.user,
            submitted_at=self.submitted_at,
        )

        self.assertEqual(submission.tenant, self.tenant)
        self.assertEqual(submission.protocol, self.protocol)
        self.assertEqual(submission.submitted_by, self.user)

    def test_submission_allows_incomplete_reason(self):
        submission = ProtocolSubmission.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            submitted_by=self.user,
            submitted_at=self.submitted_at,
            status=SubmissionStatus.INCOMPLETE,
            incomplete_reason="Missing informed consent document.",
        )

        self.assertEqual(
            submission.status,
            SubmissionStatus.INCOMPLETE,
        )
        self.assertEqual(
            submission.incomplete_reason,
            "Missing informed consent document.",
        )

    def test_submission_closed_at_is_optional(self):
        submission = ProtocolSubmission.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            submitted_by=self.user,
            submitted_at=self.submitted_at,
        )

        self.assertIsNone(submission.closed_at)
