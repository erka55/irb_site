from django.utils import timezone
from django.test import TestCase
from datetime import datetime
from uuid import uuid4


from apps.protocols.enums import (
    PreliminaryCheckResult,
    RiskLevel,
    SubmissionStatus,
)
from apps.protocols.models import (
    PreliminaryCheck,
    Protocol,
    ProtocolSubmission,
)
from apps.tenants.models import Tenant
from apps.users.models import User


class PreliminaryCheckModelTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code=f"test-{uuid4().hex[:8]}",
            name="Test Institution",
        )

        self.user = User.objects.create_user(
            email=f"checker-{uuid4().hex[:8]}@example.com",
            password="test-password",
        )

        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="Test Research Protocol",
            protocol_number=f"IRB-{uuid4().hex[:8]}",
            principal_investigator=self.user,
            risk_level=RiskLevel.LOW,
        )

        self.submission = ProtocolSubmission.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            submitted_by=self.user,
            submitted_at=timezone.make_aware(datetime(2026, 9, 15, 9, 0)),
            status=SubmissionStatus.RECEIVED,
        )

    def test_preliminary_check_belongs_to_submission(self):
        preliminary_check = PreliminaryCheck(
            tenant=self.tenant,
            submission=self.submission,
            checked_by=self.user,
            checked_at=datetime(2026, 9, 15, 10, 0),
            result=PreliminaryCheckResult.COMPLETE,
        )

        self.assertEqual(
            preliminary_check.submission_id,
            self.submission.id,
        )

    def test_preliminary_check_records_checker(self):
        preliminary_check = PreliminaryCheck(
            tenant=self.tenant,
            submission=self.submission,
            checked_by=self.user,
            checked_at=datetime(2026, 9, 15, 10, 0),
            result=PreliminaryCheckResult.COMPLETE,
        )

        self.assertEqual(
            preliminary_check.checked_by_id,
            self.user.id,
        )

    def test_preliminary_check_records_checked_at(self):
        checked_at = timezone.make_aware(datetime(2026, 9, 15, 10, 0))

        preliminary_check = PreliminaryCheck(
            tenant=self.tenant,
            submission=self.submission,
            checked_by=self.user,
            checked_at=checked_at,
            result=PreliminaryCheckResult.COMPLETE,
        )

        self.assertEqual(
            preliminary_check.checked_at,
            checked_at,
        )

    def test_complete_result_has_no_missing_documents(self):
        preliminary_check = PreliminaryCheck(
            tenant=self.tenant,
            submission=self.submission,
            checked_by=self.user,
            checked_at=datetime(2026, 9, 15, 10, 0),
            result=PreliminaryCheckResult.COMPLETE,
            missing_document_types=[],
        )

        self.assertEqual(
            preliminary_check.result,
            PreliminaryCheckResult.COMPLETE,
        )
        self.assertEqual(
            preliminary_check.missing_document_types,
            [],
        )

    def test_incomplete_result_records_missing_documents(self):
        missing_documents = [
            "methodology",
            "informed_consent",
        ]

        preliminary_check = PreliminaryCheck(
            tenant=self.tenant,
            submission=self.submission,
            checked_by=self.user,
            checked_at=datetime(2026, 9, 15, 10, 0),
            result=PreliminaryCheckResult.INCOMPLETE,
            missing_document_types=missing_documents,
        )

        self.assertEqual(
            preliminary_check.result,
            PreliminaryCheckResult.INCOMPLETE,
        )
        self.assertEqual(
            preliminary_check.missing_document_types,
            missing_documents,
        )

    def test_incomplete_result_can_have_correction_deadline(self):
        correction_due_at = datetime(2026, 9, 18, 10, 0)

        preliminary_check = PreliminaryCheck(
            tenant=self.tenant,
            submission=self.submission,
            checked_by=self.user,
            checked_at=datetime(2026, 9, 15, 10, 0),
            result=PreliminaryCheckResult.INCOMPLETE,
            correction_due_at=correction_due_at,
        )

        self.assertEqual(
            preliminary_check.result,
            PreliminaryCheckResult.INCOMPLETE,
        )
        self.assertEqual(
            preliminary_check.correction_due_at,
            correction_due_at,
        )

    def test_complete_result_does_not_require_correction_deadline(self):
        preliminary_check = PreliminaryCheck(
            tenant=self.tenant,
            submission=self.submission,
            checked_by=self.user,
            checked_at=datetime(2026, 9, 15, 10, 0),
            result=PreliminaryCheckResult.COMPLETE,
            correction_due_at=None,
        )

        self.assertEqual(
            preliminary_check.result,
            PreliminaryCheckResult.COMPLETE,
        )
        self.assertIsNone(
            preliminary_check.correction_due_at,
        )

    def test_preliminary_check_has_tenant_context(self):
        preliminary_check = PreliminaryCheck(
            tenant=self.tenant,
            submission=self.submission,
            checked_by=self.user,
            checked_at=datetime(2026, 9, 15, 10, 0),
            result=PreliminaryCheckResult.COMPLETE,
        )

        self.assertEqual(
            preliminary_check.tenant_id,
            self.tenant.id,
        )

    def test_missing_documents_are_stored_as_a_snapshot(self):
        missing_documents = [
            "methodology",
            "risk_assessment",
        ]

        preliminary_check = PreliminaryCheck(
            tenant=self.tenant,
            submission=self.submission,
            checked_by=self.user,
            checked_at=datetime(2026, 9, 15, 10, 0),
            result=PreliminaryCheckResult.INCOMPLETE,
            missing_document_types=list(missing_documents),
        )

        self.assertEqual(
            preliminary_check.missing_document_types,
            missing_documents,
        )

    def test_preliminary_check_is_persisted_with_relationships(self):
        checked_at = timezone.make_aware(
            datetime(2026, 9, 15, 10, 0)
        )
        correction_due_at = timezone.make_aware(
            datetime(2026, 9, 29, 10, 0)
        )

        preliminary_check = PreliminaryCheck.objects.create(
            tenant=self.tenant,
            submission=self.submission,
            checked_by=self.user,
            checked_at=checked_at,
            result=PreliminaryCheckResult.INCOMPLETE,
            missing_document_types=[
                "methodology",
                "informed_consent",
            ],
            correction_due_at=correction_due_at,
        )

        saved_check = PreliminaryCheck.objects.get(
            id=preliminary_check.id,
        )

        self.assertEqual(
            saved_check.tenant_id,
            self.tenant.id,
        )
        self.assertEqual(
            saved_check.submission_id,
            self.submission.id,
        )
        self.assertEqual(
            saved_check.checked_by_id,
            self.user.id,
        )
        self.assertEqual(
            saved_check.checked_at,
            checked_at,
        )
        self.assertEqual(
            saved_check.result,
            PreliminaryCheckResult.INCOMPLETE,
        )
        self.assertEqual(
            saved_check.missing_document_types,
            [
                "methodology",
                "informed_consent",
            ],
        )
        self.assertEqual(
            saved_check.correction_due_at,
            correction_due_at,
        )

    def test_preliminary_check_relationships_are_resolved(self):
        preliminary_check = PreliminaryCheck.objects.create(
            tenant=self.tenant,
            submission=self.submission,
            checked_by=self.user,
            checked_at=timezone.make_aware(datetime(2026, 9, 15, 10, 0)),
            result=PreliminaryCheckResult.COMPLETE,
        )

        saved_check = PreliminaryCheck.objects.select_related(
            "tenant",
            "submission",
            "checked_by",
        ).get(id=preliminary_check.id)

        self.assertEqual(
            saved_check.tenant,
            self.tenant,
        )
        self.assertEqual(
            saved_check.submission,
            self.submission,
        )
        self.assertEqual(
            saved_check.checked_by,
            self.user,
        )
