from .base import BaseEvent
from .publisher import EventPublisher
from .registry import registry


class InMemoryEventPublisher(EventPublisher):
    """
    Simple publisher used during development.

    Events may optionally be persisted through an event store
    before registered handlers are executed.
    """

    def publish(
        self,
        event: BaseEvent,
    ) -> None:

        print(
            f"[EVENT] {event.event_type} ({event.event_id})"
        )

        if self.event_store is not None:
            self.event_store.append(event)

        handlers = registry.get_handlers(
            event.event_type
        )

        for handler in handlers:
            handler(event)
