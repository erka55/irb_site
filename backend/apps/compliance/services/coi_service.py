from apps.compliance.models import ConflictOfInterestDeclaration
from apps.users.models import Membership


class ConflictOfInterestDeclarationService:

    @staticmethod
    def declare(
        *,
        tenant,
        protocol,
        declarant,
        conflict_types,
        description,
        declared_at,
        signature_reference="",
    ) -> ConflictOfInterestDeclaration:

        if protocol.tenant_id != tenant.id:
            raise ValueError(
                "Protocol belongs to a different tenant."
            )

        if not Membership.objects.filter(
            user_id=declarant.id,
            tenant_id=tenant.id,
            is_active=True,
        ).exists():
            raise ValueError(
                "Declarant does not have an active membership in the tenant."
            )

        if not isinstance(conflict_types, list):
            raise ValueError(
                "conflict_types must be a list."
            )

        if not description or not description.strip():
            raise ValueError(
                "Description is required."
            )

        return ConflictOfInterestDeclaration.objects.create(
            tenant=tenant,
            protocol=protocol,
            declarant=declarant,
            conflict_types=conflict_types,
            description=description.strip(),
            declared_at=declared_at,
            signature_reference=signature_reference,
        )

    @staticmethod
    def has_conflict(
        *,
        protocol,
        declarant,
    ) -> bool:
        return ConflictOfInterestDeclaration.objects.filter(
            tenant_id=protocol.tenant_id,
            protocol_id=protocol.id,
            declarant_id=declarant.id,
        ).exists()
