from uuid import uuid4

from django.test import TestCase

from apps.audit.models import AuditLog
from apps.audit.queries import AuditLogQueryService
from apps.tenants.models import Tenant
from apps.users.models import User
from common.events.factory import get_event_publisher
from common.events.protocol import ProtocolSubmitted


class EventStoreQueryIntegrationTests(TestCase):

    def setUp(self):
        self.tenant = Tenant.objects.create(
            name="Event Store Query Tenant",
        )

        self.actor = User.objects.create_user(
            email=f"event-query-{uuid4()}@example.com",
            password="test-password",
        )

        self.protocol_id = uuid4()

    def test_published_event_can_be_found_by_event_id(self):
        publisher = get_event_publisher()

        event = ProtocolSubmitted(
            tenant_id=self.tenant.id,
            actor_id=str(self.actor.id),
            protocol_id=self.protocol_id,
        )

        publisher.publish(event)

        audit_log = AuditLog.objects.get(
            event_id=event.event_id,
        )

        logs = AuditLogQueryService.list_logs(
            tenant_id=self.tenant.id,
            event_id=event.event_id,
        )

        self.assertEqual(
            logs.count(),
            1,
        )

        result = logs.get()

        self.assertEqual(
            result.id,
            audit_log.id,
        )

        self.assertEqual(
            str(result.event_id),
            event.event_id,
        )

        self.assertEqual(
            result.occurred_at,
            event.occurred_at,
        )

        self.assertEqual(
            result.action,
            event.event_type,
        )

        self.assertEqual(
            result.entity_type,
            "protocol",
        )

        self.assertEqual(
            result.entity_id,
            self.protocol_id,
        )

        self.assertEqual(
            result.tenant_id,
            self.tenant.id,
        )

        self.assertEqual(
            result.actor_id,
            self.actor.id,
        )

        self.assertEqual(
            result.payload,
            event.payload,
        )
