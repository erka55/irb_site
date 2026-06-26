from apps.decision.models import (
    Decision,
    DecisionCondition,
)


class DecisionService:

    @staticmethod
    def create_decision(**data):
        return Decision.objects.create(**data)

    @staticmethod
    def add_condition(
        decision,
        description,
        order=1,
    ):
        return DecisionCondition.objects.create(
            decision=decision,
            description=description,
            order=order,
        )
