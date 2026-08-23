from .base import BaseEvent
from common.event_store.repository import EventStoreRepository


class EventPublisher:
    """
    Base publisher interface.

    A publisher persists the event first and then
    dispatches it to registered handlers.
    """

    def __init__(
        self,
        event_store: EventStoreRepository | None = None,
    ):
        self.event_store = event_store

    def publish(
        self,
        event: BaseEvent,
    ) -> None:
        raise NotImplementedError
