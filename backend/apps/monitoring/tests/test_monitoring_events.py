from django.test import SimpleTestCase

from common.events.monitoring import ProgressReportSubmitted
from common.events.types import EventTypes


class ProgressReportSubmittedEventTests(SimpleTestCase):

    def test_event_type(self):
        event = ProgressReportSubmitted(
            tenant_id="tenant-001",
            actor_id="user-001",
            protocol_id="protocol-001",
            progress_report_id="report-001",
        )

        self.assertEqual(
            event.event_type,
            EventTypes.PROGRESS_REPORT_SUBMITTED,
        )

    def test_event_payload(self):
        event = ProgressReportSubmitted(
            tenant_id="tenant-001",
            actor_id="user-001",
            protocol_id="protocol-001",
            progress_report_id="report-001",
        )

        self.assertEqual(
            event.payload["protocol_id"],
            "protocol-001",
        )
        self.assertEqual(
            event.payload["progress_report_id"],
            "report-001",
        )

    def test_event_context(self):
        event = ProgressReportSubmitted(
            tenant_id="tenant-001",
            actor_id="user-001",
            protocol_id="protocol-001",
            progress_report_id="report-001",
        )

        self.assertEqual(event.tenant_id, "tenant-001")
        self.assertEqual(event.actor_id, "user-001")
