from datetime import UTC, datetime
from uuid import uuid4

from django.test import TestCase

from apps.audit.models import AuditLog
from apps.tenants.models import Tenant
from apps.users.models import User
from common.events.base import BaseEvent
from common.event_store import DjangoEventStoreRepository


class TestEvent(BaseEvent):
    def __init__(
        self,
        *,
        tenant_id,
        actor_id,
        protocol_id,
    ):
        super().__init__(
            event_type="protocol.submitted",
            tenant_id=str(tenant_id),
            actor_id=str(actor_id),
            payload={
                "protocol_id": str(protocol_id),
            },
        )


class DjangoEventStoreRepositoryTests(TestCase):

    def setUp(self):
        self.repository = DjangoEventStoreRepository()

        self.tenant = Tenant.objects.create(
            name="Test Tenant",
        )

        self.actor = User.objects.create_user(
            email=f"event-store-{uuid4()}@example.com",
            password="test-password",
        )

        self.protocol_id = uuid4()

    def test_append_persists_event_as_audit_log(self):
        event = TestEvent(
            tenant_id=self.tenant.id,
            actor_id=self.actor.id,
            protocol_id=self.protocol_id,
        )

        audit_log = self.repository.append(event)

        self.assertIsInstance(
            audit_log,
            AuditLog,
        )

        self.assertEqual(
            audit_log.event_id,
            event.event_id,
        )

        self.assertEqual(
            audit_log.occurred_at,
            event.occurred_at,
        )

        self.assertEqual(
            audit_log.tenant_id,
            self.tenant.id,
        )

        self.assertEqual(
            audit_log.actor_id,
            self.actor.id,
        )

        self.assertEqual(
            audit_log.action,
            event.event_type,
        )

        self.assertEqual(
            audit_log.entity_type,
            "protocol",
        )

        self.assertEqual(
            audit_log.entity_id,
            self.protocol_id,
        )

        self.assertEqual(
            audit_log.payload,
            event.payload,
        )

    def test_append_persists_same_event_identity(self):
        event_id = str(uuid4())
        occurred_at = datetime(
            2026,
            8,
            23,
            10,
            30,
            tzinfo=UTC,
        )

        event = TestEvent(
            tenant_id=self.tenant.id,
            actor_id=self.actor.id,
            protocol_id=self.protocol_id,
        )

        event.event_id = event_id
        event.occurred_at = occurred_at

        audit_log = self.repository.append(event)

        self.assertEqual(
            audit_log.event_id,
            event_id,
        )

        self.assertEqual(
            audit_log.occurred_at,
            occurred_at,
        )

    def test_append_returns_persisted_audit_log(self):
        event = TestEvent(
            tenant_id=self.tenant.id,
            actor_id=self.actor.id,
            protocol_id=self.protocol_id,
        )

        audit_log = self.repository.append(event)

        self.assertTrue(
            AuditLog.objects.filter(
                pk=audit_log.pk,
            ).exists()
        )

    def test_duplicate_event_id_is_rejected(self):
        event_id = str(uuid4())

        first_event = TestEvent(
            tenant_id=self.tenant.id,
            actor_id=self.actor.id,
            protocol_id=self.protocol_id,
        )
        first_event.event_id = event_id

        self.repository.append(first_event)

        second_event = TestEvent(
            tenant_id=self.tenant.id,
            actor_id=self.actor.id,
            protocol_id=uuid4(),
        )
        second_event.event_id = event_id

        with self.assertRaises(Exception):
            self.repository.append(second_event)
