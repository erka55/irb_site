from uuid import UUID

from apps.users.models import Membership


class AuthorizationService:
    """
    Resolves active roles for a user within a tenant.

    This service does not define resource-specific permissions.
    """

    @staticmethod
    def get_active_roles(
        *,
        user_id: UUID | str,
        tenant_id: UUID | str,
    ) -> set[str]:
        return set(
            Membership.objects.filter(
                user_id=user_id,
                tenant_id=tenant_id,
                is_active=True,
            ).values_list(
                "role",
                flat=True,
            )
        )

    @staticmethod
    def has_role(
        *,
        user_id: UUID | str,
        tenant_id: UUID | str,
        role: str,
    ) -> bool:
        return role in AuthorizationService.get_active_roles(
            user_id=user_id,
            tenant_id=tenant_id,
        )
