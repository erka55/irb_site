from uuid import uuid4

from django.test import SimpleTestCase

from common.events.base import BaseEvent
from common.events.memory import InMemoryEventPublisher
from common.events.registry import registry
from apps.audit.handlers import AuditEventHandler
from common.events.bootstrap import register_event_handlers
from common.events.types import EventTypes

class TestEvent(BaseEvent):
    def __init__(self):
        super().__init__(
            event_type="test.event",
            tenant_id=str(uuid4()),
            actor_id=str(uuid4()),
            payload={
                "value": "test",
            },
        )


class InMemoryEventPublisherTests(SimpleTestCase):

    def setUp(self):
        registry._handlers.clear()
        self.publisher = InMemoryEventPublisher()

    def tearDown(self):
        registry._handlers.clear()

    def test_publish_calls_registered_handler(self):
        received = []

        def handler(event):
            received.append(event)

        registry.register(
            "test.event",
            handler,
        )

        event = TestEvent()

        self.publisher.publish(event)

        self.assertEqual(
            received,
            [event],
        )

    def test_publish_calls_all_registered_handlers(self):
        received = []

        def first_handler(event):
            received.append("first")

        def second_handler(event):
            received.append("second")

        registry.register(
            "test.event",
            first_handler,
        )
        registry.register(
            "test.event",
            second_handler,
        )

        self.publisher.publish(TestEvent())

        self.assertEqual(
            received,
            ["first", "second"],
        )

    def test_publish_passes_same_event_instance_to_handlers(self):
        received = []

        def handler(event):
            received.append(event)

        registry.register(
            "test.event",
            handler,
        )

        event = TestEvent()

        self.publisher.publish(event)

        self.assertIs(
            received[0],
            event,
        )

    def test_publish_without_handlers_does_not_raise(self):
        event = TestEvent()

        self.publisher.publish(event)


class AuditEventHandlerCoverageTests(SimpleTestCase):

    AUDIT_EVENT_TYPES = [
        EventTypes.PROTOCOL_SUBMITTED,
        EventTypes.PROTOCOL_UPDATED,
        EventTypes.PROTOCOL_APPROVED,
        EventTypes.PROTOCOL_REJECTED,
        EventTypes.PROTOCOL_REVISIONS_REQUESTED,

        EventTypes.REVIEW_ASSIGNED,
        EventTypes.REVIEW_SUBMITTED,
        EventTypes.REVIEW_COMPLETED,
        EventTypes.REVIEWS_COMPLETED,

        EventTypes.MEETING_SCHEDULED,
        EventTypes.MEETING_COMPLETED,
        EventTypes.MEETING_CANCELLED,

        EventTypes.DECISION_CREATED,
        EventTypes.DECISION_LETTER_GENERATED,
        EventTypes.DECISION_ISSUED,
        EventTypes.DECISION_PUBLISHED,
        EventTypes.DECISION_LETTER_ISSUED,

        EventTypes.PROGRESS_REPORT_SUBMITTED,
        EventTypes.INCIDENT_REPORT_SUBMITTED,
    ]

    def setUp(self):
        registry._handlers.clear()
        register_event_handlers()

    def tearDown(self):
        registry._handlers.clear()

    def test_all_audit_event_types_are_registered(self):
        for event_type in self.AUDIT_EVENT_TYPES:
            handlers = registry.get_handlers(event_type)

            self.assertIn(
                AuditEventHandler.handle,
                handlers,
                msg=(
                    "AuditEventHandler is not registered "
                    f"for event type: {event_type}"
                ),
            )

    def test_audit_handler_is_registered_only_once(self):
        for event_type in self.AUDIT_EVENT_TYPES:
            handlers = registry.get_handlers(event_type)

            self.assertEqual(
                handlers.count(
                    AuditEventHandler.handle,
                ),
                1,
                msg=(
                    "AuditEventHandler is registered more "
                    f"than once for event type: {event_type}"
                ),
            )

    def test_register_event_handlers_is_idempotent(self):
        register_event_handlers()
        register_event_handlers()

        for event_type in self.AUDIT_EVENT_TYPES:
            handlers = registry.get_handlers(event_type)

            self.assertEqual(
                handlers.count(
                    AuditEventHandler.handle,
                ),
                1,
                msg=(
                    "Duplicate AuditEventHandler registration "
                    f"detected for event type: {event_type}"
                ),
            )
