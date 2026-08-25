from django.test import SimpleTestCase

from common.events.factory import get_event_publisher
from common.events.memory import InMemoryEventPublisher
from common.event_store.django_repository import DjangoEventStoreRepository


class EventPublisherFactoryTests(SimpleTestCase):

    def test_returns_in_memory_event_publisher(self):
        publisher = get_event_publisher()

        self.assertIsInstance(
            publisher,
            InMemoryEventPublisher,
        )

    def test_configures_django_event_store(self):
        publisher = get_event_publisher()

        self.assertIsInstance(
            publisher.event_store,
            DjangoEventStoreRepository,
        )
