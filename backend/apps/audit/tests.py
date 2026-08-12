from datetime import UTC, datetime
from uuid import uuid4

from django.test import TestCase

from apps.audit.models import AuditLog
from apps.audit.services import log_event


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
