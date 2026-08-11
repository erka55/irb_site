from django.test import SimpleTestCase

from common.events.incident import IncidentReportSubmitted
from common.events.types import EventTypes


class IncidentReportSubmittedEventTests(SimpleTestCase):

    def test_event_type(self):
        event = IncidentReportSubmitted(
            tenant_id="tenant-001",
            actor_id="user-001",
            protocol_id="protocol-001",
            incident_report_id="incident-001",
        )

        self.assertEqual(
            event.event_type,
            EventTypes.INCIDENT_REPORT_SUBMITTED,
        )

    def test_event_payload(self):
        event = IncidentReportSubmitted(
            tenant_id="tenant-001",
            actor_id="user-001",
            protocol_id="protocol-001",
            incident_report_id="incident-001",
        )

        self.assertEqual(
            event.payload["protocol_id"],
            "protocol-001",
        )
        self.assertEqual(
            event.payload["incident_report_id"],
            "incident-001",
        )

    def test_event_context(self):
        event = IncidentReportSubmitted(
            tenant_id="tenant-001",
            actor_id="user-001",
            protocol_id="protocol-001",
            incident_report_id="incident-001",
        )

        self.assertEqual(event.tenant_id, "tenant-001")
        self.assertEqual(event.actor_id, "user-001")
