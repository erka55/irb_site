from datetime import datetime
from uuid import UUID

from django.db.models import QuerySet

from .models import AuditLog


class AuditLogQueryService:
    """
    Read-only query service for immutable audit logs.
    """

    @staticmethod
    def list_logs(
        *,
        tenant_id: UUID | str | None = None,
        actor_id: UUID | str | None = None,
        action: str | None = None,
        entity_type: str | None = None,
        entity_id: UUID | str | None = None,
        event_id: UUID | str | None = None,
        occurred_from: datetime | None = None,
        occurred_to: datetime | None = None,
    ) -> QuerySet[AuditLog]:

        queryset = AuditLog.objects.all()

        if tenant_id is not None:
            queryset = queryset.filter(
                tenant_id=tenant_id
            )

        if actor_id is not None:
            queryset = queryset.filter(
                actor_id=actor_id
            )

        if action is not None:
            queryset = queryset.filter(
                action=action
            )

        if entity_type is not None:
            queryset = queryset.filter(
                entity_type=entity_type
            )

        if entity_id is not None:
            queryset = queryset.filter(
                entity_id=entity_id
            )

        if event_id is not None:
            queryset = queryset.filter(
                event_id=event_id
            )

        if occurred_from is not None:
            queryset = queryset.filter(
                occurred_at__gte=occurred_from
            )

        if occurred_to is not None:
            queryset = queryset.filter(
                occurred_at__lte=occurred_to
            )

        return queryset
