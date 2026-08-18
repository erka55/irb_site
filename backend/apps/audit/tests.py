from datetime import UTC, datetime
from uuid import uuid4

from django.test import TestCase

from apps.audit.handlers import AuditEventHandler
from apps.audit.models import AuditLog
from apps.audit.services import log_event
from apps.audit.queries import AuditLogQueryService
from apps.tenants.models import Tenant
from apps.users.models import User
from common.events.protocol import ProtocolSubmitted
from common.event_store.django_repository import (
    DjangoEventStoreRepository,
)
from apps.audit.access import AuditLogAccessService
from apps.core.models import RoleChoices
from apps.users.models import Membership

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

    def test_append_rejects_duplicate_event_id(self):
        protocol_id = uuid4()

        event = ProtocolSubmitted(
            tenant_id=self.tenant.id,
            actor_id=self.user.id,
            protocol_id=protocol_id,
        )

        repository = DjangoEventStoreRepository()

        repository.append(event)

        with self.assertRaises(Exception):
            repository.append(event)
        

class AuditLogQueryServiceTests(TestCase):

    def setUp(self):
        self.tenant_a = Tenant.objects.create(
            code="tenant-a",
            name="Tenant A",
        )

        self.tenant_b = Tenant.objects.create(
            code="tenant-b",
            name="Tenant B",
        )

        self.user_a = User.objects.create_user(
            email="user-a@test.com",
            password="test-password",
        )

        self.user_b = User.objects.create_user(
            email="user-b@test.com",
            password="test-password",
        )

        self.entity_a = uuid4()
        self.entity_b = uuid4()

        self.event_a = uuid4()
        self.event_b = uuid4()

        self.time_a = datetime(
            2026,
            8,
            10,
            10,
            0,
            tzinfo=UTC,
        )

        self.time_b = datetime(
            2026,
            8,
            12,
            10,
            0,
            tzinfo=UTC,
        )

        log_event(
            tenant=self.tenant_a,
            actor=self.user_a,
            action="protocol.submitted",
            entity_type="protocol",
            entity_id=self.entity_a,
            event_id=self.event_a,
            occurred_at=self.time_a,
        )

        log_event(
            tenant=self.tenant_b,
            actor=self.user_b,
            action="decision.published",
            entity_type="decision",
            entity_id=self.entity_b,
            event_id=self.event_b,
            occurred_at=self.time_b,
        )

    def test_list_logs_returns_all_logs(self):
        logs = AuditLogQueryService.list_logs()

        self.assertEqual(logs.count(), 2)

    def test_filter_by_tenant(self):
        logs = AuditLogQueryService.list_logs(
            tenant_id=self.tenant_a.id,
        )

        self.assertEqual(logs.count(), 1)
        self.assertEqual(
            logs.first().tenant,
            self.tenant_a,
        )

    def test_tenant_filter_isolates_other_tenant_logs(self):
        logs = AuditLogQueryService.list_logs(
            tenant_id=self.tenant_a.id,
        )

        self.assertEqual(
            list(logs.values_list("tenant_id", flat=True)),
            [self.tenant_a.id],
        )

    def test_filter_by_actor(self):
        logs = AuditLogQueryService.list_logs(
            actor_id=self.user_b.id,
        )

        self.assertEqual(logs.count(), 1)
        self.assertEqual(
            logs.first().actor,
            self.user_b,
        )

    def test_filter_by_action(self):
        logs = AuditLogQueryService.list_logs(
            action="decision.published",
        )

        self.assertEqual(logs.count(), 1)
        self.assertEqual(
            logs.first().action,
            "decision.published",
        )

    def test_filter_by_entity(self):
        logs = AuditLogQueryService.list_logs(
            entity_type="protocol",
            entity_id=self.entity_a,
        )

        self.assertEqual(logs.count(), 1)
        self.assertEqual(
            logs.first().entity_id,
            self.entity_a,
        )

    def test_filter_by_event_id(self):
        logs = AuditLogQueryService.list_logs(
            event_id=self.event_b,
        )

        self.assertEqual(logs.count(), 1)
        self.assertEqual(
            logs.first().event_id,
            self.event_b,
        )

    def test_filter_by_occurred_at_range(self):
        logs = AuditLogQueryService.list_logs(
            occurred_from=datetime(
                2026,
                8,
                11,
                0,
                0,
                tzinfo=UTC,
            ),
            occurred_to=datetime(
                2026,
                8,
                13,
                0,
                0,
                tzinfo=UTC,
            ),
        )

        self.assertEqual(logs.count(), 1)
        self.assertEqual(
            logs.first().event_id,
            self.event_b,
        )
class AuditLogAccessServiceTests(TestCase):

    def setUp(self):
        self.tenant_a = Tenant.objects.create(
            code="audit-a",
            name="Audit Tenant A",
        )

        self.tenant_b = Tenant.objects.create(
            code="audit-b",
            name="Audit Tenant B",
        )

        self.chair = User.objects.create_user(
            email="chair-a@test.com",
            password="test-password",
        )

        self.reviewer = User.objects.create_user(
            email="reviewer-a@test.com",
            password="test-password",
        )

        self.other_tenant_user = User.objects.create_user(
            email="chair-b@test.com",
            password="test-password",
        )

        Membership.objects.create(
            user=self.chair,
            tenant=self.tenant_a,
            role=RoleChoices.CHAIR,
            is_active=True,
        )

        Membership.objects.create(
            user=self.reviewer,
            tenant=self.tenant_a,
            role=RoleChoices.REVIEWER,
            is_active=True,
        )

        Membership.objects.create(
            user=self.other_tenant_user,
            tenant=self.tenant_b,
            role=RoleChoices.CHAIR,
            is_active=True,
        )

    def test_can_view_for_authorized_role(self):
        self.assertTrue(
            AuditLogAccessService.can_view(
                user_id=self.chair.id,
                tenant_id=self.tenant_a.id,
            )
        )

    def test_cannot_view_without_permission(self):
        self.assertFalse(
            AuditLogAccessService.can_view(
                user_id=self.reviewer.id,
                tenant_id=self.tenant_a.id,
            )
        )

    def test_permission_is_tenant_scoped(self):
        self.assertFalse(
            AuditLogAccessService.can_view(
                user_id=self.chair.id,
                tenant_id=self.tenant_b.id,
            )
        )

    def test_list_logs_allows_authorized_user(self):
        log_event(
            tenant=self.tenant_a,
            actor=self.chair,
            action="protocol.submitted",
            entity_type="protocol",
            entity_id=uuid4(),
        )

        logs = AuditLogAccessService.list_logs(
            user_id=self.chair.id,
            tenant_id=self.tenant_a.id,
        )

        self.assertEqual(
            logs.count(),
            1,
        )

        self.assertEqual(
            logs.first().tenant,
            self.tenant_a,
        )

    def test_list_logs_rejects_unauthorized_user(self):
        log_event(
            tenant=self.tenant_a,
            actor=self.chair,
            action="protocol.submitted",
            entity_type="protocol",
            entity_id=uuid4(),
        )

        with self.assertRaises(PermissionError):
            AuditLogAccessService.list_logs(
                user_id=self.reviewer.id,
                tenant_id=self.tenant_a.id,
            )

    def test_list_logs_cannot_cross_tenant_boundary(self):
        log_event(
            tenant=self.tenant_a,
            actor=self.chair,
            action="protocol.submitted",
            entity_type="protocol",
            entity_id=uuid4(),
        )

        log_event(
            tenant=self.tenant_b,
            actor=self.other_tenant_user,
            action="decision.published",
            entity_type="decision",
            entity_id=uuid4(),
        )

        logs = AuditLogAccessService.list_logs(
            user_id=self.other_tenant_user.id,
            tenant_id=self.tenant_b.id,
        )

        self.assertEqual(
            logs.count(),
            1,
        )

        self.assertEqual(
            logs.first().tenant,
            self.tenant_b,
        )
