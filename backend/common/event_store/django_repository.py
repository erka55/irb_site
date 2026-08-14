from apps.audit.handlers import AuditEventHandler
from apps.audit.models import AuditLog

from common.events.base import BaseEvent
from common.event_store.repository import EventStoreRepository


class DjangoEventStoreRepository(EventStoreRepository):
    """
    Django ORM implementation of the event store.

    Events are persisted through the immutable AuditLog model.
    """

    def append(self, event: BaseEvent) -> AuditLog:
        return AuditEventHandler.handle(event)
