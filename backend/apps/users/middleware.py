from uuid import UUID


class TenantContextMiddleware:
    """
    Resolves the requested tenant from the X-Tenant-ID header.

    The middleware only extracts and validates the tenant identifier.
    Membership and permission validation remain the responsibility of
    TenantContextService and permission classes.
    """

    HEADER_NAME = "HTTP_X_TENANT_ID"

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_id = request.META.get(self.HEADER_NAME)

        request.tenant_id = None

        if tenant_id:
            try:
                request.tenant_id = UUID(tenant_id)
            except (TypeError, ValueError):
                request.tenant_id = None

        return self.get_response(request)
