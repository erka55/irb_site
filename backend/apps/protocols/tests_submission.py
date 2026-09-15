from datetime import datetime, timezone

from django.test import TestCase

from apps.protocols.enums import (
    ProtocolStatus,
    RiskLevel,
    SubmissionStatus,
)
from apps.protocols.models import Protocol, ProtocolSubmission
from apps.protocols.services.submission import ProtocolSubmissionService
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

    def _create_submission(
        self,
        *,
        status=SubmissionStatus.RECEIVED,
    ):
        return ProtocolSubmission.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            submitted_by=self.user,
            submitted_at=self.submitted_at,
            status=status,
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
        submission = self._create_submission()

        self.assertEqual(submission.tenant, self.tenant)
        self.assertEqual(submission.protocol, self.protocol)
        self.assertEqual(submission.submitted_by, self.user)

    def test_submission_allows_incomplete_reason(self):
        submission = self._create_submission(
            status=SubmissionStatus.INCOMPLETE,
        )

        submission.incomplete_reason = (
            "Missing informed consent document."
        )
        submission.save()

        self.assertEqual(
            submission.status,
            SubmissionStatus.INCOMPLETE,
        )
        self.assertEqual(
            submission.incomplete_reason,
            "Missing informed consent document.",
        )

    def test_submission_closed_at_is_optional(self):
        submission = self._create_submission()

        self.assertIsNone(submission.closed_at)


class ProtocolSubmissionServiceTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="service-tenant",
            name="Service Tenant",
        )

        self.user = User.objects.create_user(
            email="service@test.com",
            password="test-password",
        )

        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="Service Protocol",
            protocol_number="SERVICE-001",
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

    def _create_submission(
        self,
        *,
        status=SubmissionStatus.RECEIVED,
    ):
        return ProtocolSubmission.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            submitted_by=self.user,
            submitted_at=self.submitted_at,
            status=status,
        )

    def test_mark_incomplete_changes_received_to_incomplete(self):
        submission = self._create_submission()

        result = ProtocolSubmissionService.mark_incomplete(
            submission=submission,
            reason="Missing informed consent document.",
        )

        self.assertEqual(
            result.status,
            SubmissionStatus.INCOMPLETE,
        )
        self.assertEqual(
            result.incomplete_reason,
            "Missing informed consent document.",
        )

    def test_mark_incomplete_requires_reason(self):
        submission = self._create_submission()

        with self.assertRaisesMessage(
            ValueError,
            "Incomplete reason is required.",
        ):
            ProtocolSubmissionService.mark_incomplete(
                submission=submission,
                reason="",
            )

    def test_mark_complete_changes_received_to_complete(self):
        submission = self._create_submission()

        result = ProtocolSubmissionService.mark_complete(
            submission=submission,
        )

        self.assertEqual(
            result.status,
            SubmissionStatus.COMPLETE,
        )
        self.assertEqual(
            result.incomplete_reason,
            "",
        )

    def test_resubmit_changes_incomplete_to_received(self):
        submission = self._create_submission(
            status=SubmissionStatus.INCOMPLETE,
        )
        submission.incomplete_reason = (
            "Missing informed consent document."
        )
        submission.save()

        result = ProtocolSubmissionService.resubmit(
            submission=submission,
        )

        self.assertEqual(
            result.status,
            SubmissionStatus.RECEIVED,
        )
        self.assertEqual(
            result.incomplete_reason,
            "",
        )
        self.assertIsNone(result.closed_at)

    def test_close_changes_incomplete_to_closed(self):
        submission = self._create_submission(
            status=SubmissionStatus.INCOMPLETE,
        )

        result = ProtocolSubmissionService.close(
            submission=submission,
        )

        self.assertEqual(
            result.status,
            SubmissionStatus.CLOSED,
        )

    def test_mark_incomplete_rejects_non_received_submission(self):
        submission = self._create_submission(
            status=SubmissionStatus.COMPLETE,
        )

        with self.assertRaisesMessage(
            ValueError,
            "Only received submissions can be marked incomplete.",
        ):
            ProtocolSubmissionService.mark_incomplete(
                submission=submission,
                reason="Missing document.",
            )

    def test_mark_complete_rejects_non_received_submission(self):
        submission = self._create_submission(
            status=SubmissionStatus.INCOMPLETE,
        )

        with self.assertRaisesMessage(
            ValueError,
            "Only received submissions can be marked complete.",
        ):
            ProtocolSubmissionService.mark_complete(
                submission=submission,
            )

    def test_resubmit_rejects_non_incomplete_submission(self):
        submission = self._create_submission()

        with self.assertRaisesMessage(
            ValueError,
            "Only incomplete submissions can be resubmitted.",
        ):
            ProtocolSubmissionService.resubmit(
                submission=submission,
            )

    def test_close_rejects_non_incomplete_submission(self):
        submission = self._create_submission()

        with self.assertRaisesMessage(
            ValueError,
            "Only incomplete submissions can be closed.",
        ):
            ProtocolSubmissionService.close(
                submission=submission,
            )
