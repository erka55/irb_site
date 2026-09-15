from apps.protocols.enums import RiskLevel
from apps.protocols.rules.classification import ClassificationContext


class ClassificationContextFactory:

    @staticmethod
    def from_snapshot(snapshot: dict) -> ClassificationContext:
        return ClassificationContext(
            risk_level=RiskLevel(snapshot["risk_level"]),
            uses_personal_data=snapshot["uses_personal_data"],
            data_is_anonymized=snapshot["data_is_anonymized"],
            involves_vulnerable_group=snapshot["involves_vulnerable_group"],
            is_ai_research=snapshot["is_ai_research"],
            is_cyber_research=snapshot["is_cyber_research"],
        )
