from datetime import datetime
from uuid import uuid4

from django.test import TestCase
from django.utils import timezone

from apps.protocols.enums import (
    PreliminaryCheckResult,
    RiskLevel,
    SubmissionDocumentType,
    SubmissionStatus,
)
from apps.protocols.models import (
    PreliminaryCheck,
    Protocol,
    ProtocolSubmission,
    SubmissionDocument,
)
from apps.protocols.rules.completeness import (
    SubmissionCompletenessContext,
)
from apps.protocols.services.preliminary_check import (
    PreliminaryCheckService,
)
from apps.protocols.services.submission import ProtocolSubmissionService
from apps.tenants.models import Tenant
from apps.users.models import User


class PreliminaryCheckServiceTests(TestCase):

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
            submitted_at=timezone.make_aware(
                datetime(2026, 9, 15, 9, 0)
            ),
            status=SubmissionStatus.RECEIVED,
        )

        self.checked_at = timezone.make_aware(
            datetime(2026, 9, 15, 10, 0)
        )

        self.context = SubmissionCompletenessContext()

    def _upload_required_documents(self):
        required_document_types = [
            SubmissionDocumentType.RESEARCH_INTRODUCTION,
            SubmissionDocumentType.METHODOLOGY,
            SubmissionDocumentType.RISK_ASSESSMENT,
            SubmissionDocumentType.INFORMED_CONSENT,
            SubmissionDocumentType.DATA_PROTECTION_PLAN,
            SubmissionDocumentType.PI_SIGNATURE,
        ]

        for document_type in required_document_types:
            SubmissionDocument.objects.create(
                tenant=self.tenant,
                submission=self.submission,
                document_type=document_type,
                file_reference=f"files/{document_type.value}.pdf",
                uploaded_by=self.user,
                uploaded_at=self.checked_at,
            )

    def test_complete_submission_creates_complete_preliminary_check(self):
        self._upload_required_documents()

        preliminary_check = PreliminaryCheckService.check(
            submission=self.submission,
            checked_by=self.user,
            checked_at=self.checked_at,
            context=self.context,
        )

        self.assertEqual(
            preliminary_check.result,
            PreliminaryCheckResult.COMPLETE,
        )
        self.assertEqual(
            preliminary_check.missing_document_types,
            [],
        )
        self.assertIsNone(
            preliminary_check.correction_due_at,
        )

        self.submission.refresh_from_db()

        self.assertEqual(
            self.submission.status,
            SubmissionStatus.COMPLETE,
        )

    def test_incomplete_submission_creates_incomplete_preliminary_check(self):
        SubmissionDocument.objects.create(
            tenant=self.tenant,
            submission=self.submission,
            document_type=SubmissionDocumentType.RESEARCH_INTRODUCTION,
            file_reference="files/research_introduction.pdf",
            uploaded_by=self.user,
            uploaded_at=self.checked_at,
        )

        preliminary_check = PreliminaryCheckService.check(
            submission=self.submission,
            checked_by=self.user,
            checked_at=self.checked_at,
            context=self.context,
        )

        self.assertEqual(
            preliminary_check.result,
            PreliminaryCheckResult.INCOMPLETE,
        )

        self.assertEqual(
            set(preliminary_check.missing_document_types),
            {
                SubmissionDocumentType.METHODOLOGY.value,
                SubmissionDocumentType.RISK_ASSESSMENT.value,
                SubmissionDocumentType.INFORMED_CONSENT.value,
                SubmissionDocumentType.DATA_PROTECTION_PLAN.value,
                SubmissionDocumentType.PI_SIGNATURE.value,
            },
        )

        self.assertIsNotNone(
            preliminary_check.correction_due_at,
        )

        self.submission.refresh_from_db()

        self.assertEqual(
            self.submission.status,
            SubmissionStatus.INCOMPLETE,
        )

    def test_incomplete_submission_records_reason(self):
        preliminary_check = PreliminaryCheckService.check(
            submission=self.submission,
            checked_by=self.user,
            checked_at=self.checked_at,
            context=self.context,
        )

        self.assertEqual(
            preliminary_check.result,
            PreliminaryCheckResult.INCOMPLETE,
        )

        self.submission.refresh_from_db()

        self.assertEqual(
            self.submission.status,
            SubmissionStatus.INCOMPLETE,
        )
        self.assertEqual(
            self.submission.incomplete_reason,
            "Missing required submission documents.",
        )

    def test_questionnaire_context_adds_questionnaire_requirement(self):
        self._upload_required_documents()

        context = SubmissionCompletenessContext(
            uses_questionnaire_or_interview=True,
        )

        preliminary_check = PreliminaryCheckService.check(
            submission=self.submission,
            checked_by=self.user,
            checked_at=self.checked_at,
            context=context,
        )

        self.assertEqual(
            preliminary_check.result,
            PreliminaryCheckResult.INCOMPLETE,
        )
        self.assertEqual(
            preliminary_check.missing_document_types,
            [SubmissionDocumentType.QUESTIONNAIRE.value],
        )

    def test_questionnaire_context_allows_complete_submission_when_uploaded(self):
        self._upload_required_documents()

        SubmissionDocument.objects.create(
            tenant=self.tenant,
            submission=self.submission,
            document_type=SubmissionDocumentType.QUESTIONNAIRE,
            file_reference="files/questionnaire.pdf",
            uploaded_by=self.user,
            uploaded_at=self.checked_at,
        )

        context = SubmissionCompletenessContext(
            uses_questionnaire_or_interview=True,
        )

        preliminary_check = PreliminaryCheckService.check(
            submission=self.submission,
            checked_by=self.user,
            checked_at=self.checked_at,
            context=context,
        )

        self.assertEqual(
            preliminary_check.result,
            PreliminaryCheckResult.COMPLETE,
        )

    def test_ai_cyber_context_adds_ai_cyber_requirement(self):
        self._upload_required_documents()

        context = SubmissionCompletenessContext(
            is_ai_or_cyber_research=True,
        )

        preliminary_check = PreliminaryCheckService.check(
            submission=self.submission,
            checked_by=self.user,
            checked_at=self.checked_at,
            context=context,
        )

        self.assertEqual(
            preliminary_check.result,
            PreliminaryCheckResult.INCOMPLETE,
        )
        self.assertEqual(
            preliminary_check.missing_document_types,
            [SubmissionDocumentType.AI_CYBER_ASSESSMENT.value],
        )

    def test_ai_cyber_context_allows_complete_submission_when_uploaded(self):
        self._upload_required_documents()

        SubmissionDocument.objects.create(
            tenant=self.tenant,
            submission=self.submission,
            document_type=SubmissionDocumentType.AI_CYBER_ASSESSMENT,
            file_reference="files/ai_cyber_assessment.pdf",
            uploaded_by=self.user,
            uploaded_at=self.checked_at,
        )

        context = SubmissionCompletenessContext(
            is_ai_or_cyber_research=True,
        )

        preliminary_check = PreliminaryCheckService.check(
            submission=self.submission,
            checked_by=self.user,
            checked_at=self.checked_at,
            context=context,
        )

        self.assertEqual(
            preliminary_check.result,
            PreliminaryCheckResult.COMPLETE,
        )

    def test_resubmitted_submission_can_undergo_new_preliminary_check(self):
        ProtocolSubmissionService.mark_incomplete(
            self.submission,
            reason="Missing required submission documents.",
        )

        ProtocolSubmissionService.resubmit(
            self.submission,
            resubmitted_by=self.user,
        )

        self.submission.refresh_from_db()

        self.assertEqual(
            self.submission.status,
            SubmissionStatus.RECEIVED,
        )

        checked_at = timezone.make_aware(
            datetime(2026, 9, 15, 10, 0),
        )

        preliminary_check = PreliminaryCheckService.check(
            submission=self.submission,
            checked_by=self.user,
            checked_at=checked_at,
            context=SubmissionCompletenessContext(),
        )

        self.assertIsNotNone(preliminary_check)
        self.assertEqual(
            preliminary_check.submission,
            self.submission,
        )

    def test_non_received_submission_cannot_be_checked(self):
        self.submission.status = SubmissionStatus.COMPLETE
        self.submission.save(update_fields=["status"])

        with self.assertRaisesMessage(
            ValueError,
            "Only received submissions can undergo a preliminary check.",
        ):
            PreliminaryCheckService.check(
                submission=self.submission,
                checked_by=self.user,
                checked_at=self.checked_at,
                context=self.context,
            )

        self.assertEqual(
            PreliminaryCheck.objects.count(),
            0,
        )

    def test_preliminary_check_uses_submission_tenant(self):
        preliminary_check = PreliminaryCheckService.check(
            submission=self.submission,
            checked_by=self.user,
            checked_at=self.checked_at,
            context=self.context,
        )

        self.assertEqual(
            preliminary_check.tenant_id,
            self.submission.tenant_id,
        )

    def test_preliminary_check_records_checker_and_timestamp(self):
        preliminary_check = PreliminaryCheckService.check(
            submission=self.submission,
            checked_by=self.user,
            checked_at=self.checked_at,
            context=self.context,
        )

        self.assertEqual(
            preliminary_check.checked_by_id,
            self.user.id,
        )
        self.assertEqual(
            preliminary_check.checked_at,
            self.checked_at,
        )

    def test_incomplete_submission_gets_correction_deadline(self):
        preliminary_check = PreliminaryCheckService.check(
            submission=self.submission,
            checked_by=self.user,
            checked_at=self.checked_at,
            context=self.context,
        )

        self.assertIsNotNone(
            preliminary_check.correction_due_at,
        )

        self.assertEqual(
            preliminary_check.correction_due_at.date(),
            datetime(2026, 9, 29).date(),
        )

    def test_preliminary_check_rolls_back_on_failure(self):
        self._upload_required_documents()

        original_create = PreliminaryCheck.objects.create

        def failing_create(*args, **kwargs):
            raise RuntimeError("Simulated preliminary check failure")

        PreliminaryCheck.objects.create = failing_create

        try:
            with self.assertRaisesMessage(
                RuntimeError,
                "Simulated preliminary check failure",
            ):
                PreliminaryCheckService.check(
                    submission=self.submission,
                    checked_by=self.user,
                    checked_at=self.checked_at,
                    context=self.context,
                )
        finally:
            PreliminaryCheck.objects.create = original_create

        self.submission.refresh_from_db()

        self.assertEqual(
            self.submission.status,
            SubmissionStatus.RECEIVED,
        )

        self.assertEqual(
            PreliminaryCheck.objects.count(),
            0,
        )

    def test_resubmission_preserves_previous_preliminary_check(self):
        first_check = PreliminaryCheckService.check(
            submission=self.submission,
            checked_by=self.user,
            checked_at=self.checked_at,
            context=self.context,
        )

        self.assertEqual(
            first_check.result,
            PreliminaryCheckResult.INCOMPLETE,
        )

        ProtocolSubmissionService.resubmit(
            self.submission,
            resubmitted_by=self.user,
        )

        self.submission.refresh_from_db()

        second_checked_at = timezone.make_aware(
            datetime(2026, 9, 25, 10, 0),
        )

        second_check = PreliminaryCheckService.check(
            submission=self.submission,
            checked_by=self.user,
            checked_at=second_checked_at,
            context=self.context,
        )

        self.assertEqual(
            second_check.result,
            PreliminaryCheckResult.INCOMPLETE,
        )

        self.assertNotEqual(
            first_check.pk,
            second_check.pk,
        )

        self.assertEqual(
            PreliminaryCheck.objects.filter(
                submission=self.submission,
            ).count(),
            2,
        )

        first_check.refresh_from_db()

        self.assertEqual(
            first_check.result,
            PreliminaryCheckResult.INCOMPLETE,
        )

        self.assertEqual(
            first_check.checked_at,
            self.checked_at,
        )
