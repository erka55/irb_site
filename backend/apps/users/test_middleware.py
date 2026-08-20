from uuid import UUID

from django.test import RequestFactory, SimpleTestCase

from apps.users.middleware import TenantContextMiddleware


class TenantContextMiddlewareTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.get_response = lambda request: request

        self.middleware = TenantContextMiddleware(
            self.get_response,
        )

        self.tenant_id = UUID(
            "12345678-1234-5678-1234-567812345678"
        )

    def test_resolves_tenant_id_from_header(self):
        request = self.factory.get(
            "/api/test/",
            HTTP_X_TENANT_ID=str(self.tenant_id),
        )

        response = self.middleware(request)

        self.assertEqual(
            response.tenant_id,
            self.tenant_id,
        )

    def test_missing_tenant_header_sets_none(self):
        request = self.factory.get(
            "/api/test/",
        )

        response = self.middleware(request)

        self.assertIsNone(
            response.tenant_id,
        )

    def test_invalid_tenant_id_sets_none(self):
        request = self.factory.get(
            "/api/test/",
            HTTP_X_TENANT_ID="not-a-uuid",
        )

        response = self.middleware(request)

        self.assertIsNone(
            response.tenant_id,
        )

    def test_empty_tenant_header_sets_none(self):
        request = self.factory.get(
            "/api/test/",
            HTTP_X_TENANT_ID="",
        )

        response = self.middleware(request)

        self.assertIsNone(
            response.tenant_id,
        )
