from datetime import date

from dateutil.relativedelta import relativedelta

from apps.monitoring.models import (
    MonitoringFrequency,
    MonitoringPlan,
    MonitoringPlanStatus,
)
from apps.protocols.enums import RiskLevel
from apps.protocols.models import Protocol


class MonitoringPlanService:

    @staticmethod
    def determine_frequency(protocol: Protocol) -> str:
        if protocol.risk_level == RiskLevel.HIGH:
            return MonitoringFrequency.THREE_MONTHS

        return MonitoringFrequency.SIX_MONTHS

    @staticmethod
    def calculate_next_due_date(
        start_date: date,
        frequency: str,
    ) -> date:
        if frequency == MonitoringFrequency.THREE_MONTHS:
            return start_date + relativedelta(months=3)

        if frequency == MonitoringFrequency.SIX_MONTHS:
            return start_date + relativedelta(months=6)

        raise ValueError(
            f"Unsupported monitoring frequency: {frequency}"
        )

    @classmethod
    def create_plan(
        cls,
        protocol: Protocol,
        start_date: date,
    ) -> MonitoringPlan:
        frequency = cls.determine_frequency(protocol)

        next_due_date = cls.calculate_next_due_date(
            start_date=start_date,
            frequency=frequency,
        )

        return MonitoringPlan.objects.create(
            tenant=protocol.tenant,
            protocol=protocol,
            frequency=frequency,
            status=MonitoringPlanStatus.ACTIVE,
            next_due_date=next_due_date,
        )
