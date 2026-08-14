from abc import ABC, abstractmethod

from common.events.base import BaseEvent


class EventStoreRepository(ABC):
    """
    Persistence abstraction for immutable domain events.
    """

    @abstractmethod
    def append(self, event: BaseEvent):
        """
        Persist a domain event.
        """
        raise NotImplementedError
