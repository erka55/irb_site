from datetime import date
from unittest.mock import patch

from django.test import TestCase

from apps.monitoring.models import (
    MonitoringFrequency,
    MonitoringPlan,
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
from common.events.types import EventTypes


class ProgressReportEventPublishTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(
            code="EVENT",
            name="Event Test Tenant",
            contact_email="event@example.com",
        )

        cls.user = User.objects.create_user(
            email="event-pi@example.com",
            password="test-password",
        )

        cls.protocol = Protocol.objects.create(
            tenant=cls.tenant,
            title="Event Test Protocol",
            protocol_number="EVENT-PR-001",
            principal_investigator=cls.user,
            risk_level=RiskLevel.LOW,
        )

        cls.monitoring_plan = MonitoringPlan.objects.create(
            tenant=cls.tenant,
            protocol=cls.protocol,
            frequency=MonitoringFrequency.SIX_MONTHS,
            status="ACTIVE",
            next_due_date=date(2026, 12, 31),
        )

    def create_report(self):
        return ProgressReport.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            monitoring_plan=self.monitoring_plan,
            submitted_by=self.user,
            report_type=ProgressReportType.PERIODIC,
            status=ProgressReportStatus.DRAFT,
            period_start=date(2026, 1, 1),
            period_end=date(2026, 6, 30),
        )

    @patch(
        "apps.monitoring.services.progress_report_service."
        "ProgressReportService.publisher.publish"
    )
    def test_submit_report_publishes_event(
        self,
        mock_publish,
    ):
        report = self.create_report()

        ProgressReportService.submit_report(report)

        mock_publish.assert_called_once()

        event = mock_publish.call_args.args[0]

        self.assertEqual(
            event.event_type,
            EventTypes.PROGRESS_REPORT_SUBMITTED,
        )

        self.assertEqual(
            event.tenant_id,
            str(self.tenant.pk),
        )

        self.assertEqual(
            event.actor_id,
            str(self.user.pk),
        )

        self.assertEqual(
            event.payload["protocol_id"],
            str(self.protocol.pk),
        )

        self.assertEqual(
            event.payload["progress_report_id"],
            str(report.pk),
        )
