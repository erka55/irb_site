from datetime import date

from django.test import TestCase

from apps.monitoring.handlers import MonitoringHandler
from apps.monitoring.models import MonitoringFrequency
from apps.protocols.enums import RiskLevel
from apps.protocols.models import Protocol
from apps.tenants.models import Tenant
from apps.users.models import User
from common.events.base import BaseEvent
from common.events.types import EventTypes


class MonitoringHandlerTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(
            code="TEST",
            name="Test Tenant",
            contact_email="test@example.com",
        )

        cls.user = User.objects.create_user(
            email="pi@example.com",
            password="test-password",
        )

        cls.protocol = Protocol.objects.create(
            tenant=cls.tenant,
            title="Test Protocol",
            protocol_number="TEST-MH-001",
            principal_investigator=cls.user,
            risk_level=RiskLevel.HIGH,
        )

    def build_event(self):
        return BaseEvent(
            event_type=EventTypes.DECISION_PUBLISHED,
            tenant_id=str(self.tenant.pk),
            actor_id=str(self.user.pk),
            payload={
                "protocol_id": str(self.protocol.pk),
                "decision_id": "decision-test-id",
            },
        )

    def test_decision_published_creates_monitoring_plan(self):
        event = self.build_event()

        plan = MonitoringHandler.handle_decision_published(event)

        self.assertIsNotNone(plan)
        self.assertEqual(plan.protocol, self.protocol)

    def test_handler_uses_protocol_tenant(self):
        event = self.build_event()

        plan = MonitoringHandler.handle_decision_published(event)

        self.assertEqual(plan.tenant, self.tenant)

    def test_high_risk_protocol_gets_three_month_frequency(self):
        event = self.build_event()

        plan = MonitoringHandler.handle_decision_published(event)

        self.assertEqual(
            plan.frequency,
            MonitoringFrequency.THREE_MONTHS,
        )
