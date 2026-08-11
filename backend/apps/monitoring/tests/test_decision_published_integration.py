from django.test import TestCase

from apps.decision.models.decision import Decision
from apps.decision.models.letter import (
    Letter,
    PublicationStatus,
)
from apps.decision.services.publication_service import (
    DecisionPublicationService,
)
from apps.monitoring.models import (
    MonitoringFrequency,
    MonitoringPlan,
)
from apps.protocols.enums import RiskLevel
from apps.protocols.models import Protocol
from apps.tenants.models import Tenant
from apps.users.models import User
from common.events.bootstrap import register_event_handlers


class DecisionPublishedMonitoringIntegrationTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(
            code="TEST",
            name="Test Tenant",
            contact_email="test@example.com",
        )

        cls.user = User.objects.create_user(
            email="chair@example.com",
            password="test-password",
        )

        cls.protocol = Protocol.objects.create(
            tenant=cls.tenant,
            title="Integration Test Protocol",
            protocol_number="TEST-DP-001",
            principal_investigator=cls.user,
            risk_level=RiskLevel.HIGH,
        )

    def create_decision(self):
        return Decision.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            decided_by=self.user,
            decision_type=Decision.DecisionType.APPROVED,
            quorum_met=True,
        )

    def create_generated_letter(self, decision):
        return Letter.objects.create(
            decision=decision,
            title="IRB Decision Letter",
            content="Approved.",
            rendered_content="Approved.",
            publication_status=PublicationStatus.GENERATED,
        )

    def test_decision_published_creates_monitoring_plan(self):
        register_event_handlers()

        decision = self.create_decision()
        letter = self.create_generated_letter(decision)

        DecisionPublicationService.publish(
            decision=decision,
            published_by=self.user,
        )

        plan = MonitoringPlan.objects.get(
            protocol=self.protocol,
        )

        self.assertEqual(
            plan.protocol,
            self.protocol,
        )
        self.assertEqual(
            plan.tenant,
            self.tenant,
        )
        self.assertEqual(
            plan.frequency,
            MonitoringFrequency.THREE_MONTHS,
        )

    def test_decision_publication_publishes_letter(self):
        register_event_handlers()

        decision = self.create_decision()
        letter = self.create_generated_letter(decision)

        result = DecisionPublicationService.publish(
            decision=decision,
            published_by=self.user,
        )

        result.refresh_from_db()

        self.assertEqual(
            result.pk,
            letter.pk,
        )
        self.assertEqual(
            result.publication_status,
            PublicationStatus.PUBLISHED,
        )
        self.assertIsNotNone(
            result.published_at,
        )
        self.assertEqual(
            result.published_by,
            self.user,
        )

    def test_decision_publication_creates_only_one_monitoring_plan(self):
        register_event_handlers()

        decision = self.create_decision()
        self.create_generated_letter(decision)

        DecisionPublicationService.publish(
            decision=decision,
            published_by=self.user,
        )

        self.assertEqual(
            MonitoringPlan.objects.filter(
                protocol=self.protocol,
            ).count(),
            1,
        )
