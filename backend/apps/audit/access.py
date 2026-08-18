from uuid import UUID

from apps.audit.queries import AuditLogQueryService
from apps.users.services.permissions import (
    PermissionChoices,
    PermissionService,
)


class AuditLogAccessService:
    """
    Authorization boundary for audit log access.

    Audit log queries remain read-only and are delegated to
    AuditLogQueryService after permission validation.
    """

    @staticmethod
    def can_view(
        *,
        user_id: UUID | str,
        tenant_id: UUID | str,
    ) -> bool:
        return PermissionService.has_permission(
            user_id=user_id,
            tenant_id=tenant_id,
            permission=PermissionChoices.VIEW_AUDIT_LOG,
        )

    @staticmethod
    def list_logs(
        *,
        user_id: UUID | str,
        tenant_id: UUID | str,
        actor_id: UUID | str | None = None,
        action: str | None = None,
        entity_type: str | None = None,
        entity_id: UUID | str | None = None,
        event_id: UUID | str | None = None,
        occurred_from=None,
        occurred_to=None,
    ):
        if not AuditLogAccessService.can_view(
            user_id=user_id,
            tenant_id=tenant_id,
        ):
            raise PermissionError(
                "User does not have permission to view audit logs."
            )

        return AuditLogQueryService.list_logs(
            tenant_id=tenant_id,
            actor_id=actor_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            event_id=event_id,
            occurred_from=occurred_from,
            occurred_to=occurred_to,
        )
