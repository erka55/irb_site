from datetime import date

from django.test import TestCase

from apps.monitoring.models import (
    MonitoringFrequency,
    MonitoringPlanStatus,
)
from apps.monitoring.services.monitoring_plan_service import (
    MonitoringPlanService,
)
from apps.protocols.enums import RiskLevel
from apps.protocols.models import Protocol
from apps.tenants.models import Tenant
from apps.users.models import User


class MonitoringPlanServiceTests(TestCase):

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

    def create_protocol(self, risk_level):
        return Protocol.objects.create(
            tenant=self.tenant,
            title="Test Protocol",
            protocol_number=f"TEST-{risk_level}",
            principal_investigator=self.user,
            risk_level=risk_level,
        )

    def test_high_risk_protocol_uses_three_month_frequency(self):
        protocol = self.create_protocol(RiskLevel.HIGH)

        frequency = MonitoringPlanService.determine_frequency(protocol)

        self.assertEqual(
            frequency,
            MonitoringFrequency.THREE_MONTHS,
        )

    def test_non_high_risk_protocol_uses_six_month_frequency(self):
        protocol = self.create_protocol(RiskLevel.LOW)

        frequency = MonitoringPlanService.determine_frequency(protocol)

        self.assertEqual(
            frequency,
            MonitoringFrequency.SIX_MONTHS,
        )

    def test_calculates_three_month_due_date(self):
        start_date = date(2026, 1, 15)

        due_date = MonitoringPlanService.calculate_next_due_date(
            start_date=start_date,
            frequency=MonitoringFrequency.THREE_MONTHS,
        )

        self.assertEqual(
            due_date,
            date(2026, 4, 15),
        )

    def test_calculates_six_month_due_date(self):
        start_date = date(2026, 1, 15)

        due_date = MonitoringPlanService.calculate_next_due_date(
            start_date=start_date,
            frequency=MonitoringFrequency.SIX_MONTHS,
        )

        self.assertEqual(
            due_date,
            date(2026, 7, 15),
        )

    def test_create_plan_creates_active_monitoring_plan(self):
        protocol = self.create_protocol(RiskLevel.HIGH)
        start_date = date(2026, 1, 15)

        plan = MonitoringPlanService.create_plan(
            protocol=protocol,
            start_date=start_date,
        )

        self.assertEqual(plan.tenant, self.tenant)
        self.assertEqual(plan.protocol, protocol)
        self.assertEqual(
            plan.frequency,
            MonitoringFrequency.THREE_MONTHS,
        )
        self.assertEqual(
            plan.status,
            MonitoringPlanStatus.ACTIVE,
        )
        self.assertEqual(
            plan.next_due_date,
            date(2026, 4, 15),
        )
