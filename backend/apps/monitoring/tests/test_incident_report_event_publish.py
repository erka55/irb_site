from datetime import date, datetime, timedelta
from unittest.mock import patch

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
from common.events.types import EventTypes


class IncidentReportEventPublishTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.tenant = Tenant.objects.create(
            code="INC-EVENT",
            name="Incident Event Test Tenant",
            contact_email="incident-event@example.com",
        )

        cls.user = User.objects.create_user(
            email="incident-event@example.com",
            password="test-password",
        )

        cls.protocol = Protocol.objects.create(
            tenant=cls.tenant,
            title="Incident Event Test Protocol",
            protocol_number="INC-EVENT-001",
            principal_investigator=cls.user,
            risk_level=RiskLevel.HIGH,
        )

        cls.monitoring_plan = MonitoringPlan.objects.create(
            tenant=cls.tenant,
            protocol=cls.protocol,
            frequency=MonitoringFrequency.THREE_MONTHS,
            status="ACTIVE",
            next_due_date=date(2026, 12, 31),
        )

    def create_report(self):
        occurred_at = timezone.now() - timedelta(hours=1)

        return IncidentReport.objects.create(
            tenant=self.tenant,
            protocol=self.protocol,
            monitoring_plan=self.monitoring_plan,
            reported_by=self.user,
            incident_type=IncidentReportType.PARTICIPANT_SAFETY,
            status=IncidentReportStatus.SUBMITTED,
            occurred_at=occurred_at,
            description="Test incident report.",
        )

    @patch(
        "apps.monitoring.services.incident_report_service."
        "IncidentReportService.publisher.publish"
    )
    def test_record_reported_at_publishes_event(
        self,
        mock_publish,
    ):
        report = self.create_report()

        reported_at = report.occurred_at + timedelta(hours=1)

        IncidentReportService.record_reported_at(
            report,
            reported_at=reported_at,
        )

        mock_publish.assert_called_once()

        event = mock_publish.call_args.args[0]

        self.assertEqual(
            event.event_type,
            EventTypes.INCIDENT_REPORT_SUBMITTED,
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
            event.payload["incident_report_id"],
            str(report.pk),
        )
