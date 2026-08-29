from uuid import uuid4

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.audit.models import AuditLog
from apps.core.models import RoleChoices
from apps.tenants.models import Tenant
from apps.users.models import Membership, User


class AuditLogAPIIntegrationTests(APITestCase):
    def setUp(self):
        self.tenant_a = Tenant.objects.create(
            code="api-a",
            name="Tenant A",
        )

        self.tenant_b = Tenant.objects.create(
            code="api-b",
            name="Tenant B",
        )

        self.user = User.objects.create_user(
            email="audit-viewer@example.com",
            password="test-password",
        )

        self.other_user = User.objects.create_user(
            email="other-user@example.com",
            password="test-password",
        )

        Membership.objects.create(
            user=self.user,
            tenant=self.tenant_a,
            role=RoleChoices.TENANT_ADMIN,
            is_active=True,
        )

        Membership.objects.create(
            user=self.other_user,
            tenant=self.tenant_b,
            role=RoleChoices.TENANT_ADMIN,
            is_active=True,
        )

        self.log_a = AuditLog.objects.create(
            tenant=self.tenant_a,
            actor=self.user,
            event_id=uuid4(),
            action="protocol.submitted",
            entity_type="Protocol",
            entity_id=uuid4(),
            payload={
                "source": "integration-test",
            },
        )

        self.log_b = AuditLog.objects.create(
            tenant=self.tenant_b,
            actor=self.other_user,
            event_id=uuid4(),
            action="protocol.approved",
            entity_type="Protocol",
            entity_id=uuid4(),
            payload={
                "source": "tenant-b",
            },
        )

        self.url = reverse("audit-log-list")

    def _set_tenant(self, tenant):
        self.client.defaults["HTTP_X_TENANT_ID"] = str(
            tenant.id
        )

    def test_list_requires_authentication(self):
        self._set_tenant(self.tenant_a)

        response = self.client.get(
            self.url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_list_requires_tenant_context(self):
        self.client.force_authenticate(
            user=self.user,
        )

        response = self.client.get(
            self.url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_tenant_admin_can_list_own_tenant_logs(self):
        self.client.force_authenticate(
            user=self.user,
        )

        self._set_tenant(self.tenant_a)

        response = self.client.get(
            self.url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        results = response.data

        self.assertEqual(
            len(results),
            1,
        )

        self.assertEqual(
            results[0]["id"],
            str(self.log_a.id),
        )

        self.assertEqual(
            results[0]["tenant"],
            self.tenant_a.id,
        )

    def test_tenant_isolation(self):
        self.client.force_authenticate(
            user=self.user,
        )

        self._set_tenant(self.tenant_a)

        response = self.client.get(
            self.url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        results = response.data

        self.assertEqual(
            len(results),
            1,
        )

        result_ids = {
            item["id"]
            for item in results
        }

        self.assertIn(
            str(self.log_a.id),
            result_ids,
        )

        self.assertNotIn(
            str(self.log_b.id),
            result_ids,
        )

    def test_retrieve_returns_only_own_tenant_log(self):
        self.client.force_authenticate(
            user=self.user,
        )

        self._set_tenant(self.tenant_a)

        url = reverse(
            "audit-log-detail",
            kwargs={
                "pk": self.log_a.id,
            },
        )

        response = self.client.get(
            url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["id"],
            str(self.log_a.id),
        )

        self.assertEqual(
            response.data["tenant"],
            self.tenant_a.id,
        )

    def test_retrieve_cannot_access_other_tenant_log(self):
        self.client.force_authenticate(
            user=self.user,
        )

        self._set_tenant(self.tenant_a)

        url = reverse(
            "audit-log-detail",
            kwargs={
                "pk": self.log_b.id,
            },
        )

        response = self.client.get(
            url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_action_filter(self):
        self.client.force_authenticate(
            user=self.user,
        )

        self._set_tenant(self.tenant_a)

        response = self.client.get(
            self.url,
            {
                "action": "protocol.submitted",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        results = response.data

        self.assertEqual(
            len(results),
            1,
        )

        self.assertEqual(
            results[0]["id"],
            str(self.log_a.id),
        )

        self.assertEqual(
            results[0]["action"],
            "protocol.submitted",
        )

    def test_entity_type_filter(self):
        self.client.force_authenticate(
            user=self.user,
        )

        self._set_tenant(self.tenant_a)

        response = self.client.get(
            self.url,
            {
                "entity_type": "Protocol",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        results = response.data

        self.assertEqual(
            len(results),
            1,
        )

        self.assertEqual(
            results[0]["id"],
            str(self.log_a.id),
        )

        self.assertEqual(
            results[0]["entity_type"],
            "Protocol",
        )

    def test_event_id_filter(self):
        self.client.force_authenticate(
            user=self.user,
        )

        self._set_tenant(self.tenant_a)

        response = self.client.get(
            self.url,
            {
                "event_id": str(self.log_a.event_id),
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        results = response.data

        self.assertEqual(
            len(results),
            1,
        )

        self.assertEqual(
            results[0]["id"],
            str(self.log_a.id),
        )

        self.assertEqual(
            results[0]["event_id"],
            str(self.log_a.event_id),
        )
