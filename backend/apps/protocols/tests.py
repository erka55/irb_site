from rest_framework.test import APITestCase

from apps.core.models import RoleChoices
from apps.protocols.enums import ProtocolStatus, RiskLevel
from apps.protocols.models import Protocol
from apps.tenants.models import Tenant
from apps.users.models import Membership, User


class ProtocolAPIPermissionTests(APITestCase):

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
            email="protocol-api@test.com",
            password="test-password",
        )

        self.other_user = User.objects.create_user(
            email="other@test.com",
            password="test-password",
        )

        self.protocol_a = Protocol.objects.create(
            tenant=self.tenant_a,
            title="Protocol A",
            protocol_number="PROTO-A-001",
            principal_investigator=self.user,
            risk_level=RiskLevel.LOW,
            status=ProtocolStatus.DRAFT,
        )

        self.protocol_b = Protocol.objects.create(
            tenant=self.tenant_b,
            title="Protocol B",
            protocol_number="PROTO-B-001",
            principal_investigator=self.other_user,
            risk_level=RiskLevel.LOW,
            status=ProtocolStatus.DRAFT,
        )

    def _authenticate(self, user=None):
        self.client.force_authenticate(
            user=user or self.user,
        )

    def _add_membership(
        self,
        *,
        tenant,
        role,
        user=None,
        is_active=True,
    ):
        return Membership.objects.create(
            user=user or self.user,
            tenant=tenant,
            role=role,
            is_active=is_active,
        )

    def test_anonymous_user_cannot_list_protocols(self):
        response = self.client.get(
            "/api/protocols/",
            HTTP_X_TENANT_ID=str(self.tenant_a.id),
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_user_without_membership_cannot_list_protocols(self):
        self._authenticate()

        response = self.client.get(
            "/api/protocols/",
            HTTP_X_TENANT_ID=str(self.tenant_a.id),
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_reviewer_can_list_protocols_in_own_tenant(self):
        self._add_membership(
            tenant=self.tenant_a,
            role=RoleChoices.REVIEWER,
        )

        self._authenticate()

        response = self.client.get(
            "/api/protocols/",
            HTTP_X_TENANT_ID=str(self.tenant_a.id),
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        returned_ids = {
            item["id"]
            for item in response.data
        }

        self.assertIn(
            str(self.protocol_a.id),
            returned_ids,
        )

        self.assertNotIn(
            str(self.protocol_b.id),
            returned_ids,
        )

    def test_user_cannot_list_protocols_from_different_tenant(self):
        self._add_membership(
            tenant=self.tenant_a,
            role=RoleChoices.REVIEWER,
        )

        self._authenticate()

        response = self.client.get(
            "/api/protocols/",
            HTTP_X_TENANT_ID=str(self.tenant_b.id),
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_inactive_membership_cannot_list_protocols(self):
        self._add_membership(
            tenant=self.tenant_a,
            role=RoleChoices.REVIEWER,
            is_active=False,
        )

        self._authenticate()

        response = self.client.get(
            "/api/protocols/",
            HTTP_X_TENANT_ID=str(self.tenant_a.id),
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_reviewer_cannot_create_protocol_without_edit_permission(self):
        self._add_membership(
            tenant=self.tenant_a,
            role=RoleChoices.REVIEWER,
        )

        self._authenticate()

        response = self.client.post(
            "/api/protocols/",
            {
                "tenant": str(self.tenant_a.id),
                "title": "New Protocol",
                "protocol_number": "PROTO-NEW-001",
                "principal_investigator": str(self.user.id),
                "risk_level": RiskLevel.LOW,
                "summary": "Test protocol",
            },
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant_a.id),
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_pi_can_create_protocol_with_edit_permission(self):
        self._add_membership(
            tenant=self.tenant_a,
            role=RoleChoices.PI,
        )

        self._authenticate()

        response = self.client.post(
            "/api/protocols/",
            {
                "tenant": str(self.tenant_a.id),
                "title": "New Protocol",
                "protocol_number": "PROTO-NEW-002",
                "principal_investigator": str(self.user.id),
                "risk_level": RiskLevel.LOW,
                "summary": "Test protocol",
            },
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant_a.id),
        )

        self.assertEqual(
            response.status_code,
            201,
        )

        self.assertTrue(
            Protocol.objects.filter(
                protocol_number="PROTO-NEW-002",
                tenant=self.tenant_a,
            ).exists()
        )

    def test_chair_cannot_create_protocol_for_different_tenant(self):
        self._add_membership(
            tenant=self.tenant_a,
            role=RoleChoices.CHAIR,
        )

        self._authenticate()

        response = self.client.post(
            "/api/protocols/",
            {
                "tenant": str(self.tenant_b.id),
                "title": "Cross Tenant Protocol",
                "protocol_number": "PROTO-CROSS-001",
                "principal_investigator": str(self.user.id),
                "risk_level": RiskLevel.LOW,
                "summary": "Cross tenant test",
            },
            format="json",
            HTTP_X_TENANT_ID=str(self.tenant_a.id),
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.assertFalse(
            Protocol.objects.filter(
                protocol_number="PROTO-CROSS-001",
            ).exists()
        )
