from .state_machine import ALLOWED_TRANSITIONS


class InvalidTransitionError(Exception):
    pass


class WorkflowEngine:

    @staticmethod
    def transition(current, target):
        allowed = ALLOWED_TRANSITIONS.get(current, set())

        if target not in allowed:
            raise InvalidTransitionError(
                f"Cannot transition from {current} to {target}"
            )

        return target
