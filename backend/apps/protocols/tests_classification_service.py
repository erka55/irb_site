from django.test import TestCase
from django.utils import timezone
from datetime import datetime
from unittest.mock import patch


from apps.protocols.enums import RiskLevel, ReviewClassification
from apps.protocols.models import ClassificationAssessment
from apps.protocols.services.classification import ClassificationService


class ClassificationServiceTests(TestCase):

    def setUp(self):
        from apps.protocols.models import Protocol, ProtocolVersion
        from apps.tenants.models import Tenant
        from apps.users.models import User

        self.tenant = Tenant.objects.create(
            code="TEST",
            name="Test Tenant",
        )

        self.user = User.objects.create_user(
            email="reviewer@example.com",
            password="test-password",
        )

        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="Test Protocol",
            protocol_number="TEST-001",
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
                "status": self.protocol.status,
                "risk_level": RiskLevel.MEDIUM,
                "summary": self.protocol.summary,
                "tenant_id": str(self.tenant.id),
                "principal_investigator_id": self.user.id,
                "uses_personal_data": True,
                "data_is_anonymized": True,
                "involves_vulnerable_group": False,
                "is_ai_research": False,
                "is_cyber_research": False,
            },
            created_by=self.user,
        )

    @patch("apps.protocols.services.classification.timezone.now")
    def test_creates_classification_assessment(
        self,
        mock_now,
    ):
        evaluated_at = timezone.make_aware(
            datetime(2026, 9, 15, 10, 0, 0)
        )
        mock_now.return_value = evaluated_at

        assessment = ClassificationService.evaluate(
            protocol_version=self.protocol_version,
            evaluated_by=self.user,
        )

        self.assertIsInstance(
            assessment,
            ClassificationAssessment,
        )

        self.assertEqual(
            assessment.protocol,
            self.protocol,
        )

        self.assertEqual(
            assessment.protocol_version,
            self.protocol_version,
        )

        self.assertEqual(
            assessment.tenant,
            self.tenant,
        )

        self.assertEqual(
            assessment.classification,
            ReviewClassification.SIMPLIFIED,
        )

        self.assertEqual(
            assessment.evaluated_by,
            self.user,
        )

        self.assertEqual(
            assessment.evaluated_at,
            evaluated_at,
        )

        self.assertTrue(assessment.rationale)

    @patch("apps.protocols.services.classification.timezone.now")
    def test_uses_current_protocol_version_snapshot_for_evaluation(
        self,
        mock_now,
    ):
        mock_now.return_value = timezone.make_aware(
            datetime(2026, 9, 15, 10, 0, 0)
        )

        self.protocol_version.snapshot["is_ai_research"] = True
        self.protocol_version.snapshot["uses_personal_data"] = False
        self.protocol_version.snapshot["data_is_anonymized"] = False
        self.protocol_version.snapshot["risk_level"] = RiskLevel.LOW
        self.protocol_version.snapshot["involves_vulnerable_group"] = False
        self.protocol_version.snapshot["is_cyber_research"] = False
        self.protocol_version.save(update_fields=["snapshot"])

        assessment = ClassificationService.evaluate(
            protocol_version=self.protocol_version,
            evaluated_by=self.user,
        )

        self.assertEqual(
            assessment.classification,
            ReviewClassification.FULL,
        )

    def test_does_not_create_assessment_when_classification_is_undetermined(self):
        self.protocol_version.snapshot["uses_personal_data"] = True
        self.protocol_version.snapshot["data_is_anonymized"] = False
        self.protocol_version.snapshot["risk_level"] = RiskLevel.MEDIUM
        self.protocol_version.snapshot["involves_vulnerable_group"] = False
        self.protocol_version.snapshot["is_ai_research"] = False
        self.protocol_version.snapshot["is_cyber_research"] = False
        self.protocol_version.save(update_fields=["snapshot"])

        result = ClassificationService.evaluate(
            protocol_version=self.protocol_version,
            evaluated_by=self.user,
        )

        self.assertIsNone(result)

        self.assertFalse(
            ClassificationAssessment.objects.filter(
                protocol_version=self.protocol_version,
            ).exists()
        )

    @patch(
        "apps.protocols.services.classification.get_event_publisher",
    )
    @patch("apps.protocols.services.classification.timezone.now")
    def test_publishes_classification_assessed_event(
        self,
        mock_now,
        mock_get_event_publisher,
    ):
        evaluated_at = timezone.make_aware(
            datetime(2026, 9, 15, 10, 0, 0)
        )
        mock_now.return_value = evaluated_at

        publisher = mock_get_event_publisher.return_value

        assessment = ClassificationService.evaluate(
            protocol_version=self.protocol_version,
            evaluated_by=self.user,
        )

        publisher.publish.assert_called_once()

        event = publisher.publish.call_args.args[0]

        self.assertEqual(
            event.event_type,
            "classification.assessed",
        )

        self.assertEqual(
            event.tenant_id,
            str(self.tenant.id),
        )

        self.assertEqual(
            event.actor_id,
            str(self.user.id),
        )

        self.assertEqual(
            event.payload["assessment_id"],
            str(assessment.id),
        )

        self.assertEqual(
            event.payload["protocol_id"],
            str(self.protocol.id),
        )

        self.assertEqual(
            event.payload["protocol_version_id"],
            str(self.protocol_version.id),
        )

        self.assertEqual(
            event.payload["classification"],
            ReviewClassification.SIMPLIFIED,
        )
