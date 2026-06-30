from .rules import validate_transition


class WorkflowEngine:

    def transition(
        self,
        current,
        target,
    ):
        validate_transition(current, target)

        return target
