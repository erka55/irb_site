"""
Decision domain services.
"""
from django.db import transaction
from django.utils import timezone

from apps.audit.models import AuditLog
from ..models.decision import Decision


class DecisionService:
    """
    Service responsible for issuing and publishing IRB decisions.
    """

    @staticmethod
    @transaction.atomic
    def publish_decision(*, decision: Decision, actor) -> Decision:
        if decision.is_published:
            raise ValueError("Decision is already published.")

        decision.is_published = True
        decision.published_at = timezone.now()
        decision.save()

        AuditLog.objects.create(
            tenant=decision.tenant,
            actor=actor,
            action="decision.publish",
            entity_type="Decision",
            entity_id=decision.id,
            payload={
                "decision_type": decision.decision_type,
                "protocol_id": str(decision.protocol_id),
            },
        )
        return decision
