"""
Decision domain services.
"""
from django.db import transaction
from django.utils import timezone

from apps.audit.models import AuditLog
from ..models.decision import Decision
from apps.protocols.models import Protocol
from apps.users.models import Membership
from apps.core.models import RoleChoices

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

    @staticmethod
    @transaction.atomic
    def create_draft(*, protocol_id) -> Decision:
        """
        Create an unpublished draft decision after
        review quorum has been reached.
        """

        protocol = Protocol.objects.select_related(
            "tenant"
        ).get(id=protocol_id)

        chair = (
            Membership.objects
            .select_related("user")
            .get(
                tenant=protocol.tenant,
                role=RoleChoices.CHAIR,
                is_active=True,
            )
            .user
        )

        decision = Decision.objects.create(
            tenant=protocol.tenant,
            protocol=protocol,
            decided_by=chair,
            decision_type=Decision.DecisionType.CONDITIONAL_APPROVAL,
            quorum_met=True,
            is_published=False,
        )

        AuditLog.objects.create(
            tenant=protocol.tenant,
            actor=chair,
            action="decision.create_draft",
            entity_type="Decision",
            entity_id=decision.id,
            payload={
                "protocol_id": str(protocol.id),
            },
        )

        return decision
