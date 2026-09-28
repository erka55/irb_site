from uuid import uuid4

from django.test import TestCase

from common.events.compliance import EthicsViolationRecorded
from common.events.types import EventTypes


class EthicsViolationRecordedTests(TestCase):

    def test_event_contains_expected_data(self):
        tenant_id = uuid4()
        actor_id = uuid4()
        violation_id = uuid4()
        protocol_id = uuid4()

        event = EthicsViolationRecorded(
            tenant_id=tenant_id,
            actor_id=actor_id,
            violation_id=violation_id,
            protocol_id=protocol_id,
            violation_type="DATA_FALSIFICATION",
        )

        self.assertEqual(
            event.event_type,
            EventTypes.ETHICS_VIOLATION_RECORDED,
        )
        self.assertEqual(event.tenant_id, str(tenant_id))
        self.assertEqual(event.actor_id, str(actor_id))

        self.assertEqual(
            event.payload["violation_id"],
            str(violation_id),
        )
        self.assertEqual(
            event.payload["protocol_id"],
            str(protocol_id),
        )
        self.assertEqual(
            event.payload["violation_type"],
            "DATA_FALSIFICATION",
        )
