from .memory import InMemoryEventPublisher
from common.event_store.django_repository import DjangoEventStoreRepository


def get_event_publisher():
    return InMemoryEventPublisher(
        event_store=DjangoEventStoreRepository(),
    )
