from .base import BaseEvent


class EventPublisher:
    """
    Base publisher interface.

    Future implementations:
        - RabbitMQ
        - Kafka
        - Redis Streams
    """

    def publish(self, event: BaseEvent) -> None:
        raise NotImplementedError
