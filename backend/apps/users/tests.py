from django.test import TestCase

from apps.core.models import RoleChoices
from apps.tenants.models import Tenant
from apps.users.models import Membership, User
from apps.users.services.authorization import AuthorizationService


class AuthorizationServiceTests(TestCase):

    def setUp(self):
        self.tenant_a = Tenant.objects.create(
            code="tenant-a",
            name="Tenant A",
        )

        self.tenant_b = Tenant.objects.create(
            code="tenant-b",
            name="Tenant B",
        )

        self.user = User.objects.create_user(
            email="auth@test.com",
            password="test-password",
        )

    def test_get_active_roles_returns_active_roles(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.CHAIR,
            is_active=True,
        )

        roles = AuthorizationService.get_active_roles(
            user_id=self.user.id,
            tenant_id=self.tenant_a.id,
        )

        self.assertEqual(
            roles,
            {RoleChoices.CHAIR},
        )

    def test_get_active_roles_returns_multiple_roles(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.CHAIR,
            is_active=True,
        )

        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        roles = AuthorizationService.get_active_roles(
            user_id=self.user.id,
            tenant_id=self.tenant_a.id,
        )

        self.assertEqual(
            roles,
            {
                RoleChoices.CHAIR,
                RoleChoices.REVIEWER,
            },
        )

    def test_get_active_roles_excludes_inactive_memberships(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.CHAIR,
            is_active=False,
        )

        roles = AuthorizationService.get_active_roles(
            user_id=self.user.id,
            tenant_id=self.tenant_a.id,
        )

        self.assertEqual(
            roles,
            set(),
        )

    def test_get_active_roles_is_tenant_scoped(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.CHAIR,
            is_active=True,
        )

        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_b,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        roles = AuthorizationService.get_active_roles(
            user_id=self.user.id,
            tenant_id=self.tenant_a.id,
        )

        self.assertEqual(
            roles,
            {RoleChoices.CHAIR},
        )

    def test_get_active_roles_returns_empty_set_without_membership(self):
        roles = AuthorizationService.get_active_roles(
            user_id=self.user.id,
            tenant_id=self.tenant_a.id,
        )

        self.assertEqual(
            roles,
            set(),
        )

    def test_has_role_returns_true_for_active_role(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.CHAIR,
            is_active=True,
        )

        self.assertTrue(
            AuthorizationService.has_role(
                user_id=self.user.id,
                tenant_id=self.tenant_a.id,
                role=RoleChoices.CHAIR,
            )
        )

    def test_has_role_returns_false_for_missing_role(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.CHAIR,
            is_active=True,
        )

        self.assertFalse(
            AuthorizationService.has_role(
                user_id=self.user.id,
                tenant_id=self.tenant_a.id,
                role=RoleChoices.REVIEWER,
            )
        )

    def test_has_role_returns_false_for_inactive_role(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.CHAIR,
            is_active=False,
        )

        self.assertFalse(
            AuthorizationService.has_role(
                user_id=self.user.id,
                tenant_id=self.tenant_a.id,
                role=RoleChoices.CHAIR,
            )
        )

    def test_has_role_does_not_cross_tenant_boundary(self):
        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.CHAIR,
            is_active=True,
        )

        self.assertFalse(
            AuthorizationService.has_role(
                user_id=self.user.id,
                tenant_id=self.tenant_b.id,
                role=RoleChoices.CHAIR,
            )
        )
