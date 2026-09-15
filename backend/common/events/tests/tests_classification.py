from uuid import UUID

from django.test import SimpleTestCase

from common.events.classification import ClassificationAssessed
from common.events.types import EventTypes


class ClassificationAssessedEventTests(SimpleTestCase):

    def test_event_contains_classification_assessment_context(self):
        event_id = UUID("11111111-1111-1111-1111-111111111111")
        tenant_id = UUID("22222222-2222-2222-2222-222222222222")
        actor_id = UUID("33333333-3333-3333-3333-333333333333")
        protocol_id = UUID("44444444-4444-4444-4444-444444444444")
        protocol_version_id = UUID("55555555-5555-5555-5555-555555555555")
        assessment_id = UUID("66666666-6666-6666-6666-666666666666")

        event = ClassificationAssessed(
            event_id=event_id,
            tenant_id=tenant_id,
            actor_id=actor_id,
            assessment_id=assessment_id,
            protocol_id=protocol_id,
            protocol_version_id=protocol_version_id,
            classification="simplified",
        )

        self.assertEqual(
            event.event_type,
            EventTypes.CLASSIFICATION_ASSESSED,
        )
        self.assertEqual(event.event_id, event_id)
        self.assertEqual(event.tenant_id, tenant_id)
        self.assertEqual(event.actor_id, actor_id)

        self.assertEqual(
            event.payload["assessment_id"],
            str(assessment_id),
        )
        self.assertEqual(
            event.payload["protocol_id"],
            str(protocol_id),
        )
        self.assertEqual(
            event.payload["protocol_version_id"],
            str(protocol_version_id),
        )
        self.assertEqual(
            event.payload["classification"],
            "simplified",
        )

    def test_event_has_expected_event_type(self):
        event = ClassificationAssessed(
            tenant_id=UUID("22222222-2222-2222-2222-222222222222"),
            actor_id=UUID("33333333-3333-3333-3333-333333333333"),
            assessment_id=UUID("66666666-6666-6666-6666-666666666666"),
            protocol_id=UUID("44444444-4444-4444-4444-444444444444"),
            protocol_version_id=UUID("55555555-5555-5555-5555-555555555555"),
            classification="full",
        )

        self.assertEqual(
            event.event_type,
            EventTypes.CLASSIFICATION_ASSESSED,
        )
