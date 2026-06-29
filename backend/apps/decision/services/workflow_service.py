"""
Decision domain services.
"""
from django.db import transaction

from ..workflow import validate_transition
from ..rules import (
    validate_review_completed,
    validate_committee_completed,
    validate_quorum_met,
)


class DecisionWorkflowService:
    """
    Service responsible for validating and executing
    decision workflow transitions.
    """

    @staticmethod
    def validate_transition(
        *,
        current_state: str,
        target_state: str,
        review_completed: bool,
        committee_completed: bool,
        quorum_met: bool,
    ) -> None:
        validate_transition(current_state, target_state)
        validate_review_completed(review_completed)
        validate_committee_completed(committee_completed)
        validate_quorum_met(quorum_met)

    @staticmethod
    @transaction.atomic
    def execute_transition(
        *,
        decision,
        target_state: str,
        review_completed: bool,
        committee_completed: bool,
        quorum_met: bool,
    ):
        DecisionWorkflowService.validate_transition(
            current_state=decision.status,
            target_state=target_state,
            review_completed=review_completed,
            committee_completed=committee_completed,
            quorum_met=quorum_met,
        )
        decision.status = target_state
        decision.save(update_fields=["status", "updated_at"])
        return decision
