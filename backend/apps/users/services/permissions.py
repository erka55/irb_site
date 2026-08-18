from uuid import UUID

from apps.core.models import RoleChoices
from apps.users.services.authorization import AuthorizationService


class PermissionChoices:
    VIEW_PROTOCOL = "protocol.view"
    EDIT_PROTOCOL = "protocol.edit"

    SUBMIT_REVIEW = "review.submit"
    ASSIGN_REVIEW = "review.assign"

    VIEW_DECISION = "decision.view"
    ISSUE_DECISION = "decision.issue"

    VIEW_AUDIT_LOG = "audit.view"


ROLE_PERMISSIONS = {
    RoleChoices.SUPER_ADMIN: {
        PermissionChoices.VIEW_PROTOCOL,
        PermissionChoices.EDIT_PROTOCOL,
        PermissionChoices.SUBMIT_REVIEW,
        PermissionChoices.ASSIGN_REVIEW,
        PermissionChoices.VIEW_DECISION,
        PermissionChoices.ISSUE_DECISION,
        PermissionChoices.VIEW_AUDIT_LOG,
    },
    RoleChoices.TENANT_ADMIN: {
        PermissionChoices.VIEW_PROTOCOL,
        PermissionChoices.EDIT_PROTOCOL,
        PermissionChoices.VIEW_DECISION,
        PermissionChoices.VIEW_AUDIT_LOG,
    },
    RoleChoices.SECRETARY: {
        PermissionChoices.VIEW_PROTOCOL,
        PermissionChoices.VIEW_DECISION,
    },
    RoleChoices.CHAIR: {
        PermissionChoices.VIEW_PROTOCOL,
        PermissionChoices.VIEW_DECISION,
        PermissionChoices.ISSUE_DECISION,
        PermissionChoices.VIEW_AUDIT_LOG,
    },
    RoleChoices.REVIEWER: {
        PermissionChoices.VIEW_PROTOCOL,
        PermissionChoices.SUBMIT_REVIEW,
    },
    RoleChoices.PI: {
        PermissionChoices.VIEW_PROTOCOL,
        PermissionChoices.EDIT_PROTOCOL,
    },
}


class PermissionService:
    """
    Resolves permissions from active tenant-scoped roles.

    Resource-specific authorization is intentionally
    outside this service for now.
    """

    @staticmethod
    def get_permissions(
        *,
        user_id: UUID | str,
        tenant_id: UUID | str,
    ) -> set[str]:
        roles = AuthorizationService.get_active_roles(
            user_id=user_id,
            tenant_id=tenant_id,
        )

        permissions = set()

        for role in roles:
            permissions.update(
                ROLE_PERMISSIONS.get(role, set())
            )

        return permissions

    @staticmethod
    def has_permission(
        *,
        user_id: UUID | str,
        tenant_id: UUID | str,
        permission: str,
    ) -> bool:
        return permission in PermissionService.get_permissions(
            user_id=user_id,
            tenant_id=tenant_id,
        )
