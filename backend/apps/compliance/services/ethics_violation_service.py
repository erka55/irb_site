from apps.compliance.models import EthicsViolation


class EthicsViolationService:

    @staticmethod
    def record(
        *,
        tenant,
        protocol,
        violation_type,
        description,
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

        return EthicsViolation.objects.create(
            tenant=tenant,
            protocol=protocol,
            violation_type=violation_type,
            description=description.strip(),
        )
