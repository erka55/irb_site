from dataclasses import dataclass

from apps.protocols.enums import ReviewClassification, RiskLevel


@dataclass(frozen=True)
class ClassificationContext:
    risk_level: RiskLevel
    uses_personal_data: bool
    data_is_anonymized: bool
    involves_vulnerable_group: bool
    is_ai_research: bool
    is_cyber_research: bool


class ClassificationEvaluator:
    @staticmethod
    def evaluate(
        context: ClassificationContext,
    ) -> ReviewClassification | None:

        if context.is_ai_research:
            return ReviewClassification.FULL

        if context.is_cyber_research:
            return ReviewClassification.FULL

        if context.involves_vulnerable_group:
            return ReviewClassification.FULL

        if context.risk_level == RiskLevel.HIGH:
            return ReviewClassification.FULL

        if not context.uses_personal_data:
            return ReviewClassification.EXEMPT

        if (
            context.uses_personal_data
            and context.data_is_anonymized
            and context.risk_level == RiskLevel.MEDIUM
        ):
            return ReviewClassification.SIMPLIFIED

        return None
