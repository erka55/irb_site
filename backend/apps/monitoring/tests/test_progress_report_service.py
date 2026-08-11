from datetime import date

from django.test import TestCase
from django.utils import timezone

from apps.monitoring.models import (
    MonitoringPlan,
    MonitoringFrequency,
    ProgressReport,
    ProgressReportStatus,
    ProgressReportType,
)
from apps.monitoring.services.progress_report_service import (
    ProgressReportService,
)
from apps.protocols.enums import RiskLevel
from apps.protocols.models import Protocol
from apps.tenants.models import Tenant
from apps.users.models import User


class ProgressReportServiceTests(TestCase):

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
            protocol_number="TEST-PR-001",
            principal_investigator=cls.user,
            risk_level=RiskLevel.LOW,
        )

        cls.monitoring_plan = MonitoringPlan.objects.create(
            tenant=cls.tenant,
            protocol=cls.protocol,
            frequency=MonitoringFrequency.SIX_MONTHS,
            status="ACTIVE",
            next_due_date=date(2026, 7, 15),
        )

    def create_report(self, status=ProgressReportStatus.DRAFT):
        return ProgressReport.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            monitoring_plan=self.monitoring_plan,
            submitted_by=self.user,
            report_type=ProgressReportType.PERIODIC,
            status=status,
            period_start=date(2026, 1, 1),
            period_end=date(2026, 6, 30),
        )

    def test_submit_draft_report_changes_status_to_submitted(self):
        report = self.create_report()

        result = ProgressReportService.submit_report(report)

        self.assertEqual(
            result.status,
            ProgressReportStatus.SUBMITTED,
        )

    def test_submit_draft_report_sets_submitted_at(self):
        report = self.create_report()

        ProgressReportService.submit_report(report)

        self.assertIsNotNone(report.submitted_at)

    def test_submit_report_persists_changes(self):
        report = self.create_report()

        ProgressReportService.submit_report(report)

        report.refresh_from_db()

        self.assertEqual(
            report.status,
            ProgressReportStatus.SUBMITTED,
        )
        self.assertIsNotNone(report.submitted_at)

    def test_submitting_non_draft_report_raises_error(self):
        report = self.create_report(
            status=ProgressReportStatus.SUBMITTED,
        )

        with self.assertRaises(ValueError):
            ProgressReportService.submit_report(report)

    def test_submit_returns_same_report_instance(self):
        report = self.create_report()

        result = ProgressReportService.submit_report(report)

        self.assertEqual(result.pk, report.pk)
