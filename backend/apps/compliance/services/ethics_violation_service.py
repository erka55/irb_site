from apps.compliance.models import EthicsViolation
from common.events.compliance import EthicsViolationRecorded
from common.events.factory import get_event_publisher


class EthicsViolationService:

    @staticmethod
    def record(
        *,
        tenant,
        protocol,
        violation_type,
        description,
        actor_id,
    ) -> EthicsViolation:

        if protocol.tenant_id != tenant.id:
            raise ValueError(
                "Protocol belongs to a different tenant."
            )

        valid_types = {
            choice
            for choice, _ in EthicsViolation.ViolationType.choices
        }

        if violation_type not in valid_types:
            raise ValueError(
                "Invalid ethics violation type."
            )

        if not description or not description.strip():
            raise ValueError(
                "Description is required."
            )

        violation = EthicsViolation.objects.create(
            tenant=tenant,
            protocol=protocol,
            violation_type=violation_type,
            description=description.strip(),
        )

        publisher = get_event_publisher()

        publisher.publish(
            EthicsViolationRecorded(
                tenant_id=tenant.id,
                actor_id=actor_id,
                violation_id=violation.id,
                protocol_id=protocol.id,
                violation_type=violation.violation_type,
            )
        )

        return violation
