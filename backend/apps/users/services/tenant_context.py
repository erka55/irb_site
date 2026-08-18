from uuid import UUID

from apps.users.models import Membership


class TenantContextService:
    """
    Resolves and validates the active tenant context for a user.

    This service only verifies that the user has an active
    membership in the requested tenant.
    Role and permission checks are handled by the
    authorization and permission services.
    """

    @staticmethod
    def resolve(
        *,
        user_id: UUID | str,
        tenant_id: UUID | str,
    ):
        return Membership.objects.get(
            user_id=user_id,
            tenant_id=tenant_id,
            is_active=True,
        )
