from uuid import uuid4

from django.test import SimpleTestCase

from common.events.base import BaseEvent
from common.events.memory import InMemoryEventPublisher
from common.events.registry import registry


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
