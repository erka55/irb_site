from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.tenants.models import Tenant
from apps.protocols.models import Protocol
from apps.decision.models import Decision
from apps.notifications.models import Notification

from apps.protocols.enums import RiskLevel
from apps.decision.services.decision_service import DecisionService

User = get_user_model()


class DecisionNotificationTest(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="TEST",
            name="Test Tenant",
        )

        self.pi = User.objects.create_user(
            email="pi@test.com",
            password="test123",
        )

        self.chair = User.objects.create_user(
            email="chair@test.com",
            password="test123",
        )

        self.protocol = Protocol.objects.create(
            tenant=self.tenant,
            title="COVID-19 Study",
            protocol_number="P-001",
            principal_investigator=self.pi,
            risk_level=RiskLevel.LOW,
            summary="Test protocol",
        )

        self.decision = Decision.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            decided_by=self.chair,
            decision_type=Decision.DecisionType.APPROVED,
            quorum_met=True,
        )

    def test_publish_decision_creates_notification(self):
        DecisionService.publish_decision(
            decision=self.decision,
            actor=self.chair,
        )

        notification = Notification.objects.filter(
            recipient=self.pi,
        ).first()

        self.assertIsNotNone(notification)

        self.assertEqual(
            notification.recipient,
            self.pi,
        )

        self.assertEqual(
            notification.tenant,
            self.tenant,
        )

        self.assertEqual(
            Notification.objects.count(),
            1,
        )        

        self.assertIn(
            self.protocol.title,
            notification.message,
        )
