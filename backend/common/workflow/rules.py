from .state_machine import (
    ALLOWED_TRANSITIONS,
    ProtocolStatus,
)


def can_transition(
    current: ProtocolStatus,
    target: ProtocolStatus,
) -> bool:
    return target in ALLOWED_TRANSITIONS[current]


def validate_transition(
    current: ProtocolStatus,
    target: ProtocolStatus,
) -> None:
    if not can_transition(current, target):
        raise ValueError(
            f"Invalid workflow transition: "
            f"{current} -> {target}"
        )
