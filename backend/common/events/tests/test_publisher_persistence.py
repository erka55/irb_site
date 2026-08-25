from uuid import uuid4

from django.test import TestCase

from apps.audit.models import AuditLog
from apps.tenants.models import Tenant
from apps.users.models import User
from common.events.protocol import ProtocolSubmitted
from common.events.factory import get_event_publisher


class EventPublisherPersistenceTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Publisher Test Tenant",
        )

        self.actor = User.objects.create_user(
            email=f"publisher-{uuid4()}@example.com",
            password="test-password",
        )

        self.protocol_id = uuid4()

    def test_publish_persists_event_as_audit_log(self):
        publisher = get_event_publisher()

        event = ProtocolSubmitted(
            tenant_id=self.tenant.id,
            actor_id=str(self.actor.id),
            protocol_id=self.protocol_id,
        )

        publisher.publish(event)

        logs = AuditLog.objects.filter(
            event_id=event.event_id,
        )

        self.assertEqual(
            logs.count(),
            1,
        )

        audit_log = logs.get()

        self.assertEqual(
            str(audit_log.event_id),
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
