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

    def get(self, event_id: str) -> AuditLog:
        return AuditLog.objects.get(
            event_id=event_id,
        )

    def exists(self, event_id: str) -> bool:
        return AuditLog.objects.filter(
            event_id=event_id,
        ).exists()
