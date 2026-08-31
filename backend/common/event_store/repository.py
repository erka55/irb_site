from abc import ABC, abstractmethod
from uuid import UUID

from common.events.base import BaseEvent


class EventStoreRepository(ABC):
    """
    Persistence abstraction for immutable domain events.
    """

    @abstractmethod
    def append(self, event: BaseEvent):
        """
        Persist a domain event and return the persisted record.
        """
        raise NotImplementedError

    @abstractmethod
    def get(self, event_id: UUID | str):
        """
        Retrieve a persisted event by its event identity.
        """
        raise NotImplementedError

    @abstractmethod
    def exists(self, event_id: UUID | str) -> bool:
        """
        Check whether an event with the given identity exists.
        """
        raise NotImplementedError
