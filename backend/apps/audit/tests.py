from datetime import UTC, datetime
from uuid import uuid4

from django.test import TestCase

from apps.audit.handlers import AuditEventHandler
from apps.audit.models import AuditLog
from apps.audit.services import log_event
from apps.tenants.models import Tenant
from apps.users.models import User
from common.events.protocol import ProtocolSubmitted
from common.event_store.django_repository import (
    DjangoEventStoreRepository,
)


class AuditLogTests(TestCase):

    def test_log_event_creates_audit_log(self):
        entity_id = uuid4()

        log = log_event(
            action="decision.published",
            entity_type="Decision",
            entity_id=entity_id,
            payload={
                "decision_type": "APPROVED",
            },
        )

        self.assertEqual(
            log.action,
            "decision.published",
        )
        self.assertEqual(
            log.entity_type,
            "Decision",
        )
        self.assertEqual(
            log.entity_id,
            entity_id,
        )
        self.assertEqual(
            log.payload["decision_type"],
            "APPROVED",
        )

    def test_log_event_stores_event_metadata(self):
        entity_id = uuid4()
        event_id = uuid4()
        occurred_at = datetime(
            2026,
            8,
            12,
            10,
            30,
            tzinfo=UTC,
        )

        log = log_event(
            action="decision.published",
            entity_type="Decision",
            entity_id=entity_id,
            event_id=event_id,
            occurred_at=occurred_at,
        )

        self.assertEqual(
            log.event_id,
            event_id,
        )
        self.assertEqual(
            log.occurred_at,
            occurred_at,
        )

    def test_event_id_must_be_unique(self):
        event_id = uuid4()

        log_event(
            action="decision.published",
            entity_type="Decision",
            entity_id=uuid4(),
            event_id=event_id,
        )

        with self.assertRaises(Exception):
            log_event(
                action="decision.published",
                entity_type="Decision",
                entity_id=uuid4(),
                event_id=event_id,
            )

    def test_audit_log_cannot_be_updated(self):
        log = AuditLog.objects.create(
            action="decision.published",
            entity_type="Decision",
            entity_id=uuid4(),
        )

        log.action = "decision.modified"

        with self.assertRaises(ValueError):
            log.save()

    def test_audit_log_cannot_be_deleted(self):
        log = AuditLog.objects.create(
            action="decision.published",
            entity_type="Decision",
            entity_id=uuid4(),
        )

        with self.assertRaises(ValueError):
            log.delete()

    def test_audit_log_has_no_soft_delete_api(self):
        log = AuditLog.objects.create(
            action="decision.published",
            entity_type="Decision",
            entity_id=uuid4(),
        )

        self.assertFalse(
            hasattr(log, "soft_delete")
        )


class AuditEventHandlerTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="test-tenant",
            name="Test Tenant",
        )

        self.user = User.objects.create_user(
            email="audit@test.com",
            password="test-password",
        )

    def test_handle_creates_audit_log(self):
        protocol_id = uuid4()

        event = ProtocolSubmitted(
            tenant_id=self.tenant.id,
            actor_id=self.user.id,
            protocol_id=protocol_id,
        )

        log = AuditEventHandler.handle(event)

        self.assertIsInstance(log, AuditLog)
        self.assertEqual(
            log.action,
            "protocol.submitted",
        )
        self.assertEqual(
            log.entity_type,
            "protocol",
        )
        self.assertEqual(
            log.entity_id,
            protocol_id,
        )

    def test_handle_preserves_event_metadata(self):
        protocol_id = uuid4()
        event_id = str(uuid4())
        occurred_at = datetime(
            2026,
            8,
            13,
            12,
            30,
            tzinfo=UTC,
        )

        event = ProtocolSubmitted(
            tenant_id=self.tenant.id,
            actor_id=self.user.id,
            protocol_id=protocol_id,
        )

        event.event_id = event_id
        event.occurred_at = occurred_at

        log = AuditEventHandler.handle(event)

        self.assertEqual(
            log.event_id,
            event_id,
        )
        self.assertEqual(
            log.occurred_at,
            occurred_at,
        )

    def test_handle_preserves_actor_tenant_and_payload(self):
        protocol_id = uuid4()

        event = ProtocolSubmitted(
            tenant_id=self.tenant.id,
            actor_id=self.user.id,
            protocol_id=protocol_id,
        )

        log = AuditEventHandler.handle(event)

        self.assertEqual(
            log.tenant,
            self.tenant,
        )
        self.assertEqual(
            log.actor,
            self.user,
        )
        self.assertEqual(
            log.payload,
            {
                "protocol_id": str(protocol_id),
            },
        )

class DjangoEventStoreRepositoryTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            code="event-store-tenant",
            name="Event Store Tenant",
        )

        self.user = User.objects.create_user(
            email="event-store@test.com",
            password="test-password",
        )

    def test_append_persists_event(self):
        protocol_id = uuid4()

        event = ProtocolSubmitted(
            tenant_id=self.tenant.id,
            actor_id=self.user.id,
            protocol_id=protocol_id,
        )

        repository = DjangoEventStoreRepository()

        log = repository.append(event)

        self.assertIsInstance(log, AuditLog)

        self.assertEqual(
            log.event_id,
            event.event_id,
        )

        self.assertEqual(
            log.occurred_at,
            event.occurred_at,
        )

        self.assertEqual(
            log.tenant,
            self.tenant,
        )

        self.assertEqual(
            log.actor,
            self.user,
        )

        self.assertEqual(
            log.entity_id,
            protocol_id,
        )

        self.assertEqual(
            log.payload,
            event.payload,
        )

    def test_append_preserves_event_metadata(self):
        protocol_id = uuid4()

        event = ProtocolSubmitted(
            tenant_id=self.tenant.id,
            actor_id=self.user.id,
            protocol_id=protocol_id,
        )

        repository = DjangoEventStoreRepository()

        log = repository.append(event)

        self.assertEqual(
            log.event_id,
            event.event_id,
        )

        self.assertEqual(
            log.occurred_at,
            event.occurred_at,
        )
