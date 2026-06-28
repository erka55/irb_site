"""
Decision business rules.

These rules validate whether a decision is eligible
to move through the workflow.
"""


def validate_review_completed(review_completed: bool) -> None:
    if not review_completed:
        raise ValueError("Review process is not completed.")


def validate_committee_completed(committee_completed: bool) -> None:
    if not committee_completed:
        raise ValueError("Committee review is not completed.")


def validate_quorum_met(quorum_met: bool) -> None:
    if not quorum_met:
        raise ValueError("Committee quorum has not been met.")
