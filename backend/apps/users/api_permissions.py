from rest_framework.permissions import BasePermission

from apps.users.services.permissions import PermissionService
from apps.users.services.tenant_context import TenantContextService


class HasTenantPermission(BasePermission):
    """
    DRF permission boundary for tenant-scoped permissions.

    A view may define a get_required_permission() method for
    action-specific permissions.

    If the method is not defined, the view may provide a static
    required_permission attribute.

    Tenant context is resolved before checking the permission.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        tenant_id = getattr(
            request,
            "tenant_id",
            None,
        )

        get_required_permission = getattr(
            view,
            "get_required_permission",
            None,
        )

        if callable(get_required_permission):
            required_permission = get_required_permission()
        else:
            required_permission = getattr(
                view,
                "required_permission",
                None,
            )

        if tenant_id is None or required_permission is None:
            return False

        try:
            TenantContextService.resolve(
                user_id=user.id,
                tenant_id=tenant_id,
            )
        except Exception:
            return False

        return PermissionService.has_permission(
            user_id=user.id,
            tenant_id=tenant_id,
            permission=required_permission,
        )
