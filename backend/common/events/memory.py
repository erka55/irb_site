from .base import BaseEvent
from .publisher import EventPublisher


class InMemoryEventPublisher(EventPublisher):
    """
    Simple publisher used during development.

    Future implementations may publish to:
    - RabbitMQ
    - Kafka
    - Redis Streams
    """

    def publish(self, event: BaseEvent) -> None:
        print(f"[EVENT] {event.event_type} ({event.event_id})")
