from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from apps.monitoring.models import (
    IncidentReport,
    IncidentReportStatus,
    IncidentReportType,
    MonitoringFrequency,
    MonitoringPlan,
)
from apps.monitoring.services.incident_report_service import (
    IncidentReportService,
)
from apps.protocols.enums import RiskLevel
from apps.protocols.models import Protocol
from apps.tenants.models import Tenant
from apps.users.models import User


class IncidentReportServiceTests(TestCase):

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
            protocol_number="TEST-IR-001",
            principal_investigator=cls.user,
            risk_level=RiskLevel.HIGH,
        )

        cls.monitoring_plan = MonitoringPlan.objects.create(
            tenant=cls.tenant,
            protocol=cls.protocol,
            frequency=MonitoringFrequency.THREE_MONTHS,
            status="ACTIVE",
            next_due_date=timezone.now().date(),
        )

    def create_report(self, occurred_at):
        return IncidentReport.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            monitoring_plan=self.monitoring_plan,
            reported_by=self.user,
            incident_type=IncidentReportType.PARTICIPANT_SAFETY,
            status=IncidentReportStatus.SUBMITTED,
            occurred_at=occurred_at,
            description="Test incident",
        )

    def test_report_within_48_hours_is_accepted(self):
        occurred_at = timezone.now() - timedelta(hours=24)
        reported_at = occurred_at + timedelta(hours=24)

        report = self.create_report(occurred_at)

        result = IncidentReportService.record_reported_at(
            report,
            reported_at=reported_at,
        )

        self.assertEqual(
            result.reported_at,
            reported_at,
        )

    def test_report_exactly_at_48_hours_is_accepted(self):
        occurred_at = timezone.now() - timedelta(hours=48)
        reported_at = occurred_at + timedelta(hours=48)

        report = self.create_report(occurred_at)

        result = IncidentReportService.record_reported_at(
            report,
            reported_at=reported_at,
        )

        self.assertEqual(
            result.reported_at,
            reported_at,
        )

    def test_report_after_48_hours_is_rejected(self):
        occurred_at = timezone.now() - timedelta(hours=49)
        reported_at = occurred_at + timedelta(hours=49)

        report = self.create_report(occurred_at)

        with self.assertRaises(ValueError):
            IncidentReportService.record_reported_at(
                report,
                reported_at=reported_at,
            )

    def test_reported_time_before_occurred_time_is_rejected(self):
        occurred_at = timezone.now()

        report = self.create_report(occurred_at)

        with self.assertRaises(ValueError):
            IncidentReportService.record_reported_at(
                report,
                reported_at=occurred_at - timedelta(hours=1),
            )

    def test_report_cannot_be_reported_twice(self):
        occurred_at = timezone.now() - timedelta(hours=2)
        reported_at = occurred_at + timedelta(hours=1)

        report = self.create_report(occurred_at)

        IncidentReportService.record_reported_at(
            report,
            reported_at=reported_at,
        )

        report.refresh_from_db()

        with self.assertRaises(ValueError):
            IncidentReportService.record_reported_at(
                report,
                reported_at=occurred_at + timedelta(hours=2),
            )
