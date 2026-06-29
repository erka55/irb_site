from enum import Enum


class DecisionState(str, Enum):
    DRAFT       = "draft"
    PENDING     = "pending"
    APPROVED    = "approved"
    CONDITIONAL = "conditional"
    REJECTED    = "rejected"
    WITHDRAWN   = "withdrawn"


ALLOWED_TRANSITIONS = {
    DecisionState.DRAFT: {
        DecisionState.PENDING,
    },
    DecisionState.PENDING: {
        DecisionState.APPROVED,
        DecisionState.CONDITIONAL,
        DecisionState.REJECTED,
        DecisionState.WITHDRAWN,
    },
    DecisionState.CONDITIONAL: {
        DecisionState.APPROVED,
        DecisionState.REJECTED,
    },
    DecisionState.APPROVED:  set(),
    DecisionState.REJECTED:  set(),
    DecisionState.WITHDRAWN: set(),
}


def can_transition(current_state: str, target_state: str) -> bool:
    """Check whether a workflow transition is allowed."""
    try:
        current = DecisionState(current_state)
        target = DecisionState(target_state)
    except ValueError:
        return False
    return target in ALLOWED_TRANSITIONS[current]


def validate_transition(current_state: str, target_state: str) -> None:
    """Raise ValueError when an invalid workflow transition is attempted."""
    if not can_transition(current_state, target_state):
        raise ValueError(
            f"Invalid decision transition: {current_state} -> {target_state}"
        )
