from django.test import RequestFactory, TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from apps.core.models import RoleChoices
from apps.tenants.models import Tenant
from apps.users.api_permissions import HasTenantPermission
from apps.users.models import Membership, User
from apps.users.services.permissions import PermissionChoices


class TestPermissionView(APIView):
    required_permission = PermissionChoices.VIEW_PROTOCOL


class AuditPermissionView(APIView):
    required_permission = PermissionChoices.VIEW_AUDIT_LOG


class HasTenantPermissionTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.tenant_a = Tenant.objects.create(
            code="tenant-a",
            name="Tenant A",
        )

        self.tenant_b = Tenant.objects.create(
            code="tenant-b",
            name="Tenant B",
        )

        self.user = User.objects.create_user(
            email="api-permission@test.com",
            password="test-password",
        )

        self.permission = HasTenantPermission()

    def _request(self, user=None, tenant_id=None):
        request = self.factory.get("/api/test/")

        if user is not None:
            request.user = user
        else:
            from django.contrib.auth.models import AnonymousUser

            request.user = AnonymousUser()

        if tenant_id is not None:
            request.tenant_id = tenant_id

        return request

    def test_allows_user_with_required_permission(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        request = self._request(
            user=self.user,
            tenant_id=self.tenant_a.id,
        )

        allowed = self.permission.has_permission(
            request,
            TestPermissionView(),
        )

        self.assertTrue(allowed)

    def test_denies_user_without_required_permission(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        request = self._request(
            user=self.user,
            tenant_id=self.tenant_a.id,
        )

        view = AuditPermissionView()

        allowed = self.permission.has_permission(
            request,
            view,
        )

        self.assertFalse(allowed)

    def test_denies_user_with_inactive_membership(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.REVIEWER,
            is_active=False,
        )

        request = self._request(
            user=self.user,
            tenant_id=self.tenant_a.id,
        )

        allowed = self.permission.has_permission(
            request,
            TestPermissionView(),
        )

        self.assertFalse(allowed)

    def test_denies_user_from_different_tenant(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        request = self._request(
            user=self.user,
            tenant_id=self.tenant_b.id,
        )

        allowed = self.permission.has_permission(
            request,
            TestPermissionView(),
        )

        self.assertFalse(allowed)

    def test_denies_request_without_tenant_context(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        request = self._request(
            user=self.user,
        )

        allowed = self.permission.has_permission(
            request,
            TestPermissionView(),
        )

        self.assertFalse(allowed)

    def test_denies_view_without_required_permission(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        request = self._request(
            user=self.user,
            tenant_id=self.tenant_a.id,
        )

        view = APIView()

        allowed = self.permission.has_permission(
            request,
            view,
        )

        self.assertFalse(allowed)

    def test_denies_anonymous_user(self):
        request = self._request(
            user=None,
            tenant_id=self.tenant_a.id,
        )

        allowed = self.permission.has_permission(
            request,
            TestPermissionView(),
        )

        self.assertFalse(allowed)

    def test_allows_chair_to_view_audit_logs(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.CHAIR,
            is_active=True,
        )

        request = self._request(
            user=self.user,
            tenant_id=self.tenant_a.id,
        )

        allowed = self.permission.has_permission(
            request,
            AuditPermissionView(),
        )

        self.assertTrue(allowed)
