from datetime import datetime
from uuid import uuid4

from django.test import TestCase
from django.utils import timezone

from apps.protocols.enums import (
    ReviewClassification,
    RiskLevel,
)
from apps.protocols.models import (
    ClassificationAssessment,
    Protocol,
    ProtocolVersion,
)
from apps.tenants.models import Tenant
from apps.users.models import User


class ClassificationAssessmentModelTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code=f"test-{uuid4().hex[:8]}",
            name="Test Institution",
        )

        self.user = User.objects.create_user(
            email=f"researcher-{uuid4().hex[:8]}@example.com",
            password="test-password",
        )

        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="Test Research Protocol",
            protocol_number=f"IRB-{uuid4().hex[:8]}",
            principal_investigator=self.user,
            risk_level=RiskLevel.MEDIUM,
        )

        self.protocol_version = ProtocolVersion.objects.create(
            protocol=self.protocol,
            version_number="v1",
            snapshot={
                "id": str(self.protocol.id),
                "title": self.protocol.title,
                "protocol_number": self.protocol.protocol_number,
                "risk_level": self.protocol.risk_level,
                "classification_inputs": {
                    "uses_personal_data": True,
                    "data_is_anonymized": True,
                    "involves_vulnerable_group": False,
                    "is_ai_research": False,
                    "is_cyber_research": False,
                },
            },
            created_by=self.user,
        )

    def test_classification_assessment_belongs_to_protocol(self):
        assessment = ClassificationAssessment(
            tenant=self.tenant,
            protocol=self.protocol,
            protocol_version=self.protocol_version,
            classification=ReviewClassification.SIMPLIFIED,
            evaluated_at=timezone.make_aware(
                datetime(2026, 9, 15, 10, 0)
            ),
            evaluated_by=self.user,
            rationale="Medium-risk research using anonymized personal data.",
        )

        self.assertEqual(
            assessment.protocol_id,
            self.protocol.id,
        )

    def test_classification_assessment_belongs_to_protocol_version(self):
        assessment = ClassificationAssessment(
            tenant=self.tenant,
            protocol=self.protocol,
            protocol_version=self.protocol_version,
            classification=ReviewClassification.SIMPLIFIED,
            evaluated_at=timezone.make_aware(
                datetime(2026, 9, 15, 10, 0)
            ),
            evaluated_by=self.user,
            rationale="Medium-risk research using anonymized personal data.",
        )

        self.assertEqual(
            assessment.protocol_version_id,
            self.protocol_version.id,
        )

    def test_classification_assessment_records_tenant(self):
        assessment = ClassificationAssessment(
            tenant=self.tenant,
            protocol=self.protocol,
            protocol_version=self.protocol_version,
            classification=ReviewClassification.SIMPLIFIED,
            evaluated_at=timezone.make_aware(
                datetime(2026, 9, 15, 10, 0)
            ),
            evaluated_by=self.user,
            rationale="Medium-risk research using anonymized personal data.",
        )

        self.assertEqual(
            assessment.tenant_id,
            self.tenant.id,
        )

    def test_classification_assessment_records_evaluator(self):
        assessment = ClassificationAssessment(
            tenant=self.tenant,
            protocol=self.protocol,
            protocol_version=self.protocol_version,
            classification=ReviewClassification.SIMPLIFIED,
            evaluated_at=timezone.make_aware(
                datetime(2026, 9, 15, 10, 0)
            ),
            evaluated_by=self.user,
            rationale="Medium-risk research using anonymized personal data.",
        )

        self.assertEqual(
            assessment.evaluated_by_id,
            self.user.id,
        )

    def test_classification_assessment_records_evaluated_at(self):
        evaluated_at = timezone.make_aware(
            datetime(2026, 9, 15, 10, 0)
        )

        assessment = ClassificationAssessment(
            tenant=self.tenant,
            protocol=self.protocol,
            protocol_version=self.protocol_version,
            classification=ReviewClassification.SIMPLIFIED,
            evaluated_at=evaluated_at,
            evaluated_by=self.user,
            rationale="Medium-risk research using anonymized personal data.",
        )

        self.assertEqual(
            assessment.evaluated_at,
            evaluated_at,
        )

    def test_classification_assessment_records_rationale(self):
        rationale = (
            "Medium-risk research using anonymized personal data."
        )

        assessment = ClassificationAssessment(
            tenant=self.tenant,
            protocol=self.protocol,
            protocol_version=self.protocol_version,
            classification=ReviewClassification.SIMPLIFIED,
            evaluated_at=timezone.make_aware(
                datetime(2026, 9, 15, 10, 0)
            ),
            evaluated_by=self.user,
            rationale=rationale,
        )

        self.assertEqual(
            assessment.rationale,
            rationale,
        )

    def test_classification_assessment_supports_exempt_classification(self):
        assessment = ClassificationAssessment(
            tenant=self.tenant,
            protocol=self.protocol,
            protocol_version=self.protocol_version,
            classification=ReviewClassification.EXEMPT,
            evaluated_at=timezone.make_aware(
                datetime(2026, 9, 15, 10, 0)
            ),
            evaluated_by=self.user,
            rationale="No personal data is involved.",
        )

        self.assertEqual(
            assessment.classification,
            ReviewClassification.EXEMPT,
        )

    def test_classification_assessment_supports_simplified_classification(self):
        assessment = ClassificationAssessment(
            tenant=self.tenant,
            protocol=self.protocol,
            protocol_version=self.protocol_version,
            classification=ReviewClassification.SIMPLIFIED,
            evaluated_at=timezone.make_aware(
                datetime(2026, 9, 15, 10, 0)
            ),
            evaluated_by=self.user,
            rationale="Medium-risk research uses anonymized personal data.",
        )

        self.assertEqual(
            assessment.classification,
            ReviewClassification.SIMPLIFIED,
        )

    def test_classification_assessment_supports_full_classification(self):
        assessment = ClassificationAssessment(
            tenant=self.tenant,
            protocol=self.protocol,
            protocol_version=self.protocol_version,
            classification=ReviewClassification.FULL,
            evaluated_at=timezone.make_aware(
                datetime(2026, 9, 15, 10, 0)
            ),
            evaluated_by=self.user,
            rationale="The research involves a vulnerable group.",
        )

        self.assertEqual(
            assessment.classification,
            ReviewClassification.FULL,
        )

    def test_evaluated_by_can_be_null(self):
        assessment = ClassificationAssessment(
            tenant=self.tenant,
            protocol=self.protocol,
            protocol_version=self.protocol_version,
            classification=ReviewClassification.FULL,
            evaluated_at=timezone.make_aware(
                datetime(2026, 9, 15, 10, 0)
            ),
            evaluated_by=None,
            rationale="Classification was determined automatically.",
        )

        self.assertIsNone(
            assessment.evaluated_by,
        )

    def test_classification_assessment_is_persisted_with_relationships(self):
        evaluated_at = timezone.make_aware(
            datetime(2026, 9, 15, 10, 0)
        )

        assessment = ClassificationAssessment.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            protocol_version=self.protocol_version,
            classification=ReviewClassification.SIMPLIFIED,
            evaluated_at=evaluated_at,
            evaluated_by=self.user,
            rationale="Medium-risk research using anonymized personal data.",
        )

        saved_assessment = ClassificationAssessment.objects.get(
            id=assessment.id,
        )

        self.assertEqual(
            saved_assessment.tenant_id,
            self.tenant.id,
        )
        self.assertEqual(
            saved_assessment.protocol_id,
            self.protocol.id,
        )
        self.assertEqual(
            saved_assessment.protocol_version_id,
            self.protocol_version.id,
        )
        self.assertEqual(
            saved_assessment.classification,
            ReviewClassification.SIMPLIFIED,
        )
        self.assertEqual(
            saved_assessment.evaluated_at,
            evaluated_at,
        )
        self.assertEqual(
            saved_assessment.evaluated_by_id,
            self.user.id,
        )
        self.assertEqual(
            saved_assessment.rationale,
            "Medium-risk research using anonymized personal data.",
        )

    def test_classification_assessment_relationships_are_resolved(self):
        assessment = ClassificationAssessment.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            protocol_version=self.protocol_version,
            classification=ReviewClassification.FULL,
            evaluated_at=timezone.make_aware(
                datetime(2026, 9, 15, 10, 0)
            ),
            evaluated_by=self.user,
            rationale="The research involves a vulnerable group.",
        )

        saved_assessment = (
            ClassificationAssessment.objects.select_related(
                "tenant",
                "protocol",
                "protocol_version",
                "evaluated_by",
            ).get(id=assessment.id)
        )

        self.assertEqual(
            saved_assessment.tenant,
            self.tenant,
        )
        self.assertEqual(
            saved_assessment.protocol,
            self.protocol,
        )
        self.assertEqual(
            saved_assessment.protocol_version,
            self.protocol_version,
        )
        self.assertEqual(
            saved_assessment.evaluated_by,
            self.user,
        )

    def test_multiple_assessments_can_exist_for_same_protocol_version(self):
        evaluated_at_1 = timezone.make_aware(
            datetime(2026, 9, 15, 10, 0)
        )
        evaluated_at_2 = timezone.make_aware(
            datetime(2026, 9, 15, 11, 0)
        )

        ClassificationAssessment.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            protocol_version=self.protocol_version,
            classification=ReviewClassification.SIMPLIFIED,
            evaluated_at=evaluated_at_1,
            evaluated_by=self.user,
            rationale="Initial classification assessment.",
        )

        ClassificationAssessment.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            protocol_version=self.protocol_version,
            classification=ReviewClassification.FULL,
            evaluated_at=evaluated_at_2,
            evaluated_by=self.user,
            rationale="Classification was reassessed.",
        )

        self.assertEqual(
            ClassificationAssessment.objects.filter(
                protocol_version=self.protocol_version,
            ).count(),
            2,
        )
